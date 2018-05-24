#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

original_version = {
    "filepath": os.path.join(BASEDIR, "pymarketcap", "__init__.py"),
    "regex": r'__version__\s=\s"(.+?)"\n'
}

new_version_targets = [
    original_version,
    {
        "filepath": os.path.join(BASEDIR, "setup.py"),
        "regex": r'version="(.+?)",'
    },
    {
        "filepath": os.path.join(BASEDIR, "pymarketcap", "curl.pyx"),
        "regex": r'\*user_agent\s=\s"pymarketcap\s(.+)"'
    },
    {
        "filepath": os.path.join(BASEDIR, "doc", "conf.py"),
        "regex": r'release\s=\s"(.+)"'
    }
]

def extract_original_version():
    """Extract original version from source file"""
    with open(original_version["filepath"], "r") as original_file:
        original_file_content = original_file.read()
    response = re.search(original_version["regex"], original_file_content)
    major, minor, micro = response.groups()[0].split(".")
    return dict(  # We need 1.23.000 no 1.23.0
        major={"num": int(major), "raw": major},
        minor={"num": int(minor), "raw": minor},
        micro={"num": int(micro), "raw": micro}
    )

def write_new_version_on_targets(new_version):
    """Write new version in some files"""
    for target in new_version_targets:
        with open(target["filepath"], "r") as target_file:
            target_content = target_file.read()
            replacement = re.search(target["regex"],
                                    target_content).groups()[0]
        with open(target["filepath"], "w") as target_file:
            target_file.write(target_content.replace(replacement, new_version))
    return new_version

def get_version_type():
    """Get version type passed to script"""
    parser = argparse.ArgumentParser(description="Software versioner script.")
    versioning_types = ["major", "minor", "micro",
                        "unmajor", "unminor", "unmicro"]
    parser.add_argument("version", help="Select type of versioning: \
        %r" % versioning_types)
    args = parser.parse_args()
    if args.version not in versioning_types:
        raise ValueError("You need to select one valid versioning type: \
            %r" % versioning_types)
    return args.version

def reset_smaller_versions(version, version_type):
    """For example, versioning minor, you need to reset
    to 0 other types of versions: 1.3.127 -> 1.4.0"""
    version["micro"]["raw"] = "0" * len(version["micro"]["raw"])
    if version_type  == "major":
        version["minor"]["raw"] = "0" * len(version["minor"]["raw"])
    return version

def main():
    version = extract_original_version()
    version_type = get_version_type()

    def update_version(version, version_type, new_version_type):
        version[version_type]["raw"] = ( len(version[version_type]["raw"]) \
            - len(str(version[version_type]["num"])) ) * "0"  + str(new_version_type)
        version[version_type]["num"] = new_version_type

    if "un" in version_type:
        version_type = re.sub("un", "", version_type)
        if version[version_type]["num"] > 0:  # Prevent -1 version
            new_version_type = version[version_type]["num"] - 1
            update_version(version, version_type, new_version_type)
    else:
        new_version_type = version[version_type]["num"] + 1
        update_version(version, version_type, new_version_type)
        # Reset smaller versions
        if version_type in ["major", "minor"]:
            version = reset_smaller_versions(version,
                                             version_type)

    new_version = ".".join([
        str(version["major"]["raw"]),
        str(version["minor"]["raw"]),
        str(version["micro"]["raw"])
    ])
    return write_new_version_on_targets(new_version)

if __name__ == "__main__":
    print(main())
