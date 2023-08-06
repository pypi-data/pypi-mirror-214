import json
import logging
import os
import shutil
import subprocess
import tempfile

import requests

from .config import get_graph_dir, is_graph_enabled
from .docker import is_docker, get_omni_image

#from .graph import load_triples
from git import Repo
from omnibenchmark.utils.build_omni_object import get_omni_object_from_yaml
from omnibenchmark.renku_commands.general import renku_save
from renku.command.graph import export_graph_command

# TODO(btraven): we could move these dirs into a omnibench tmp folder
GRAPH_HOST_PATH = "/tmp/omni-graphs"
GRAPH_CONT_PATH = "/graph"
GRAPH_JSON = "graph.jsonl"
GRAPH_PATH_ENV = "OMNICLI_GRAPH_PATH"

def run(docker_image=None, sparql=None, dirty=False):

    if docker_image is None:
        # If no image is passed explicitely, we use the image naming convention
        # that the user should have built by running `omni_cli docker build`.
        # We could check if that image exists in the local docker registry, and fail early
        # if not found.
        docker_image = get_omni_image()

    if is_docker():
        return run_from_docker(export=True, dirty=dirty)
    else:
        print("> running in host...")
        shutil.rmtree(GRAPH_HOST_PATH, ignore_errors=True)
        os.makedirs(GRAPH_HOST_PATH, exist_ok=True)

        out = run_from_host_in_docker(docker_image, dirty=dirty)
        if is_graph_enabled():
            load_graph()
        if sparql is not None:
            upload_graph(sparql)
        return out

def run_from_docker(full=True, export=False, dirty=False):
    print(f"> running in docker. export={export} dirty={dirty}")
    print("> cwd:", os.getcwd())
    p = subprocess.run(["git", "lfs", "install", "--local"])
    print(p.stdout)

    oo = get_omni_object_from_yaml('src/config.yaml')
    oo.create_dataset()
    oo.run_renku()
    print("renku run done")
    oo.update_result_dataset()

    if dirty:
        # When we receive the dirty flag, we expect the following conditions to be met:
        # 1. the original repo is exposed in ../orig
        # 2. we have permissions to write to ../orig
        print("> copying dirty data dir to original repo")
        # TODO check if repo is mounted
        shutil.copytree('./data', '../orig/data', dirs_exist_ok=True)
        # The end result after this action is that we keep the renku_run commits in the current dir
        # but we just copy a "dirty" data repo to the ../orig folder.
        # We assume that ../orig has been mounted by docker as a rw volume.

    if export:
        return export_graph(full=True)

def run_from_host_in_docker(docker_image, dirty):
    is_dirty = 1 if dirty else 0
    if dirty:
        cmd = [
                "docker", "run",
                "--rm", "-v", f"{GRAPH_HOST_PATH}:{GRAPH_CONT_PATH}",
                "-e", f"OMNICLI_GRAPH_PATH={GRAPH_CONT_PATH}",
                "-v", ".:/home/rstudio/orig", # FIXME hardcoded user!!
                "-e", f"OMNICLI_DIRTY={is_dirty}",
                docker_image
        ]
    else:
        cmd = [
                "docker", "run",
                "--rm", "-v", f"{GRAPH_HOST_PATH}:{GRAPH_CONT_PATH}",
                "-v", ".:/home/rstudio/work", # FIXME hardcoded user!!
                "-e", f"OMNICLI_GRAPH_PATH={GRAPH_CONT_PATH}",
                "-e", f"OMNICLI_DIRTY={is_dirty}",
                docker_image
        ]
    print(cmd)
    p = subprocess.run(cmd)
    return p.stdout

def export_graph(full=True):
    if full:
        revision = None

    _format = "jsonld"
    strict = True

    result = (
        export_graph_command()
        .build()
        .execute(format=_format, strict=strict, revision_or_range=revision)
    )

    result = result.output.as_jsonld_string(2)
    output_dir = get_graph_output_dir()

    if output_dir:
        with open(os.path.join(output_dir, GRAPH_JSON), 'w') as f:
            f.write(result)
        return "ok"
    else:
        return result

def upload_graph(sparql):
    print("NOT IMPLEMENTED: upload graph to endpoint:", sparql)

def get_graph_output_dir():
    return os.environ.get(GRAPH_PATH_ENV, None)

def load_graph():
    _upload_to_local_graph()

def _upload_to_local_graph():
    from rdflib import Graph
    g = Graph()
    g.parse(f"file://{GRAPH_HOST_PATH}/{GRAPH_JSON}", format="json-ld")

    graph_len = len(list(g.triples((None, None, None))))
    print("> Got", graph_len, "triples")

    insert(g)


# TODO: refactor with methods in epoch (dedup)

from SPARQLWrapper import SPARQLWrapper, JSON, POST

def insert(g):
    # TODO: can use itertools to lazy evaluate the generator
    triples = list(g.triples((None, None, None)))

    while len(triples) > 0:
        batch, triples = triples[:100], triples[100:]
        updatequery = "\n".join([f"PREFIX {prefix}: {ns.n3()}" for prefix, ns in g.namespaces()])
        updatequery += f"\nINSERT DATA {{"
        updatequery += " .\n".join([f"\t\t{s.n3()} {p.n3()} {o.n3()}" for (s, p, o) in batch])
        updatequery += f" . \n\n}}\n"
        insert_triples(updatequery)

LOCAL_ENDPOINT = "http://localhost:7878/update"

def insert_triples(queryString):
    sparql = SPARQLWrapper(LOCAL_ENDPOINT)
    sparql.setQuery(queryString)
    sparql.setMethod(POST)
    ret = sparql.queryAndConvert()
