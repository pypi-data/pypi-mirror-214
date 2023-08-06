from pathlib import Path
from typing import List, Union


def upath(
    path: str,
):
    if isinstance(path, str) and path.startswith("~"):
        path = str(Path.home()) + path[1:]
    if isinstance(path, str) and path.startswith("."):
        path = str(Path.cwd()) + path[1:]
    return path


def subprocess_run(
    script: Union[str, List[str]],
    verbose: bool = True,
):
    if verbose:
        print(r">>> ", script)

        from time import sleep

        sleep(0.2)

    import subprocess

    shell = isinstance(script, str)
    return subprocess.run(script, shell=shell)
