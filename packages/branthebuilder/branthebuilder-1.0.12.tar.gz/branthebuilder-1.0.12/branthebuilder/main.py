import datetime as dt
import json
import os
import re
import sys
from functools import reduce
from pathlib import Path
from shutil import rmtree
from subprocess import check_call, check_output
from warnings import warn

import typer
import yaml
from cookiecutter.main import cookiecutter

from .nb_scripts import get_nb_scripts, get_notebooks, nb_dir
from .vars import CFF_PATH, DOC_DIR, ORCID_DIC_ENV, README_PATH, cc_repo, conf

app = typer.Typer()

osc_path = Path(".github", "workflows", "compatibility_test.yml")
ghw_path = osc_path.parent.parent


class SetupException(Exception):
    pass


@app.command()
def lint(line_len: int = None, full: bool = False):
    ll = line_len or conf.line_len
    target = "." if full else conf.module_path
    _no_tb_call(["black", target, "-l", ll])
    _no_tb_call(["isort", target, "--profile", "black", "-l", ll])
    _no_tb_call(["flake8", target, "--max-line-length", ll])


@app.command()
def init(
    input: bool = True,
    docs: bool = False,
    notebooks: bool = False,
    actions: bool = False,
    single_file: bool = False,
    git: bool = True,
    os_compatibility: bool = False,
):
    res_dir = cookiecutter(cc_repo, no_input=not input)
    os.chdir(res_dir)
    _cleanup(docs, actions, notebooks, single_file, os_compatibility)
    if not git:
        return
    for cmd in [
        ["init"],
        ["add", "*"],
        ["commit", "-m", "init"],
        ["branch", "template"],
    ]:
        check_call(["git", *cmd])


@app.command()
def update_boilerplate(merge: bool = False):
    author_base = conf.project_conf["authors"][0]
    if isinstance(author_base, dict):
        name = author_base["name"]
        email = author_base["email"]
        url = conf.project_conf["urls"]["Homepage"]
        pykey = "requires-python"
        description = conf.module.__doc__
    else:
        warn("legacy pyproject.toml! fill in email and delete some files")
        name = author_base
        email = "FILL@ME"
        url = conf.project_conf["url"]
        pykey = "python"
        description = conf.project_conf["description"]

    cc_context = {
        "full_name": name,
        "email": email,
        "github_user": url.split("/")[-2],
        "project_name": conf.name,
        "description": description,
        "python_version": conf.project_conf[pykey][2:],
    }

    branch = _get_branch()
    check_call(["git", "checkout", "template"])
    cookiecutter(
        cc_repo,
        no_input=True,
        extra_context=cc_context,
        output_dir="..",
        overwrite_if_exists=True,
    )

    single = conf.module_path.endswith(".py")
    _cleanup(
        DOC_DIR.exists(), ghw_path.exists(), nb_dir.exists(), single, osc_path.exists()
    )
    adds = check_output(["git", "add", "*"]).strip()
    if adds:
        check_call(["git", "commit", "-m", "update-boilerplate"])
    if merge:
        check_call(["git", "checkout", branch])
        check_call(["git", "merge", "template", "--no-edit"])


@app.command()
def test(html: bool = False, v: bool = False, notebooks: bool = True, cov: bool = True):
    lint()
    test_paths = [conf.module_path]
    test_notebook_path = Path("test_nb_integrations.py")
    if notebooks:
        test_notebook_path.write_text("\n\n".join(get_nb_scripts()))
        test_paths.append(test_notebook_path.as_posix())
    comm = ["python", "-m", "pytest", *test_paths, "--doctest-modules"]
    if cov:
        form = "html" if html else "xml"
        comm += [f"--cov={conf.name}", f"--cov-report={form}"]
    if v:
        comm.append("-s")
    try:
        _no_tb_call(comm)
    finally:
        test_notebook_path.unlink(missing_ok=True)


@app.command()
def build_docs():
    rmtree(DOC_DIR / "api", ignore_errors=True)
    rmtree(DOC_DIR / "notebooks", ignore_errors=True)

    _nbs = [*map(str, get_notebooks())]
    if _nbs:
        out = f"--output-dir={DOC_DIR}/notebooks"
        check_call(["jupyter", "nbconvert", *_nbs, "--to", "rst", out])
    check_call(["sphinx-build", DOC_DIR.as_posix(), f"{DOC_DIR}/_build"])


@app.command()
def tag(msg: str):
    branch = _get_branch()
    if branch != "main":
        raise SetupException(f"only main branch can be tagged - {branch}")

    tag_version = f"v{conf.version}"
    tags = check_output(["git", "tag"]).split()
    if tag_version in tags:
        raise SetupException(f"{tag_version} version already tagged")
    if DOC_DIR.exists():
        note_rst = f"{tag_version}\n---------------------\n\n" + msg
        (DOC_DIR / "release_notes" / f"{tag_version}.rst").write_text(note_rst)
        build_docs()
        check_call(["git", "add", "docs"])
        check_call(["git", "commit", "-m", f"docs for {tag_version}"])
    _mod_cff({"version": conf.version, "date-released": dt.date.today()}, tag_version)
    check_call(["git", "tag", "-a", tag_version, "-m", msg])
    check_call(["git", "push"])
    check_call(["git", "push", "origin", tag_version])


@app.command()
def init_cff(
    msg: str = "If you use this software, please cite it as below.",
    license: str = "MIT",
):
    license = "MIT"
    cff_version: str = "1.2.0"
    url = conf.project_conf["urls"]["Homepage"]
    cff_dic = {
        "cff-version": cff_version,
        "message": msg,
        "url": url,
        "authors": [],
        "title": "/".join(url.split("/")[-2:]),
        "license": license,
        "keywords": conf.project_conf.get("keywords", []),
        "type": "software",  # / dataset
    }

    orcid_dic = json.loads(os.environ.get(ORCID_DIC_ENV, "{}"))
    for author in conf.project_conf["authors"]:
        names = author["name"].split()
        adic = {"family-names": names[-1], "given-names": " ".join(names[:-1])}
        orcid = orcid_dic.get(author["name"])
        if orcid:
            adic["orcid"] = orcid
        cff_dic["authors"].append(adic)

    _dump_cff(cff_dic)


@app.command()
def add_zenodo_concept_doi(doi: int):
    full_doi = f"10.5281/zenodo.{doi}"
    fstr = "[![DOI](https://zenodo.org/badge/doi/{}.svg)](https://doi.org/{})"
    z_find = re.compile(escape(fstr, "()[]!").format(".*", ".*")).findall
    lines = list(filter(lambda li: not z_find(li), README_PATH.read_text().split("\n")))
    _mod_cff({"doi": full_doi})
    lines.insert(2, fstr.format(full_doi, full_doi))
    README_PATH.write_text("\n".join(lines))


def _get_branch():
    comm = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    return check_output(comm).strip().decode("utf-8")


def _cleanup(leave_docs, leave_actions, leave_notebooks, single_file, os_compatibility):
    if not leave_docs:
        rmtree(DOC_DIR)
        Path(".readthedocs.yml").unlink()
    if not leave_actions:
        rmtree(ghw_path)
    elif not os_compatibility:
        osc_path.unlink()
    if not leave_notebooks:
        rmtree(nb_dir)
    if single_file:
        pack_dir = Path(conf.name)
        init_str = (pack_dir / "__init__.py").read_text()
        rmtree(pack_dir)
        Path(f"{conf.name}.py").write_text(init_str)


def escape(s, chars) -> str:
    return reduce(lambda le, ri: le.replace(ri, f"\\{ri}"), chars, s)


def _no_tb_call(args):
    try:
        check_call(args)
    except Exception:
        sys.exit(1)


def _mod_cff(mod_dic: dict, msg: str = None):
    if not CFF_PATH.exists():
        return

    cff_dic = yaml.safe_load(CFF_PATH.read_text())
    _dump_cff(cff_dic | mod_dic)
    if msg:
        check_call(["git", "add", CFF_PATH.as_posix()])
        check_call(["git", "commit", "-m", f"update cff {msg}"])


def _dump_cff(dic):
    CFF_PATH.write_text(yaml.safe_dump(dic, allow_unicode=True, sort_keys=False))
