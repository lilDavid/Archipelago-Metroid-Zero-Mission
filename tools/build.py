#!/usr/bin/env python3

from argparse import ArgumentParser
import json
import os
from pathlib import Path
import shutil
import sys
import zipfile


WORLD_NAME = "mzm"

WORLD_PATH = Path(__file__).parents[1]
BUILD_PATH = WORLD_PATH / "build"


FILES = [
    "LICENSE",
    "patcher",
    "*.py",
]

EXCLUDE = [
    "**/__pycache__",
    "**/__MACOSX",
    "**/.DS_STORE",
    "patcher/data/**/*.png",
    "patcher/data/**/*.md",
]


def clean_build_path(path: Path):
    assert path == BUILD_PATH or BUILD_PATH in path.parents, path
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


def get_files():
    files: set[Path] = set()
    for pattern in FILES:
        for path in WORLD_PATH.glob(pattern):
            if path.is_dir():
                files.update(path.rglob("*"))
            else:
                files.add(path)
    for pattern in EXCLUDE:
        for path in WORLD_PATH.glob(pattern):
            if path.is_dir():
                files.difference_update(path.rglob("*"))
            try:
                files.remove(path)
            except KeyError:
                pass
    return files


def build_apworld():
    from worlds.Files import APWorldContainer

    with open(WORLD_PATH / "archipelago.json", "r", encoding="utf-8") as file:
        manifest: dict = json.load(file)
    zip_path = BUILD_PATH / f"{WORLD_NAME}.apworld"
    container = APWorldContainer(str(zip_path))
    container.game = manifest["game"]
    manifest.update(container.get_manifest())

    BUILD_PATH.mkdir(parents=True, exist_ok=True)
    zip_path = BUILD_PATH / f"{WORLD_NAME}.apworld"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as apworld:
        for path in get_files():
            relative_path = f"{WORLD_NAME}/{path.relative_to(WORLD_PATH)}"
            apworld.write(path, relative_path)
        apworld.writestr(f"{WORLD_NAME}/archipelago.json", json.dumps(manifest))


def generate_template():
    import Options
    import Utils

    templates = (BUILD_PATH / "templates")
    templates.mkdir(parents=True, exist_ok=True)
    Options.generate_yaml_templates(templates, generate_hidden=False)
    with open(WORLD_PATH / "archipelago.json", "r", encoding="utf-8") as file:
        game: str = json.load(file)["game"]
    template = templates / f"{Utils.get_file_safe_name(game)}.yaml"
    template.rename(BUILD_PATH / f"{template.name.replace(' ', '_')}")
    clean_build_path(templates)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", default=None, help="Path to your Archipelago source code")
    args = parser.parse_args()

    ap_path = args.path or os.getenv("AP_SOURCE_PATH") or os.getenv("AP_PATH") or os.getcwd()
    sys.path.append(ap_path)

    clean_build_path(BUILD_PATH)
    build_apworld()
    generate_template()
