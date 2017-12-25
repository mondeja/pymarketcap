#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Dentro de un sistema de versionado necesitamos básicamente 2 nodos:
# La versión original (una línea en un archivo) y la versión de salida,
# la cual debe replicarse en varios archivos.
# El proceso de extraer y depositar las versiones lo podemos hacer
# fácilmente con lectura/escritura de archivos mediante expresiones regulares:

import os
import re

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

original_version = {
    "filepath": os.path.join(BASEDIR, "pymarketcap", "__init__.py"),
    "regex": r'__version__\s=\s"(.+?)"\n'
}

new_version_targets = [
    {
        "filepath": os.path.join(BASEDIR, "pymarketcap", "__init__.py"),
        "regex": r'__version__\s=\s"(.+?)"\n'
    },
    {
        "filepath": os.path.join(BASEDIR, "setup.py"),
        "regex": r"version\s=\s'(.+?)',"
    }
]


def extract_original_version():
    """Extract original version from source file"""
    with open(original_version["filepath"], "r") as original_file:
        original_file_content = original_file.read()
    response = re.search(original_version["regex"], original_file_content)
    return response.groups()[0].split(".")

def write_new_version_on_targets(new_version):
    """Write new version in some files"""
    for target in new_version_targets:
        with open(target["filepath"], "r") as target_file:
            target_content = target_file.read()
            replacement = re.search(target["regex"],
                                    target_content).groups()[0]
        with open(target["filepath"], "w") as target_file:
            target_file.write(target_content.replace(replacement, new_version))

def main():
    version, release, patch = extract_original_version()
    patch = int(patch)
    patch += 1
    new_version = ".".join([version, release, str(patch)])
    write_new_version_on_targets(new_version)
    return new_version

if __name__ == "__main__":
    print(main())
