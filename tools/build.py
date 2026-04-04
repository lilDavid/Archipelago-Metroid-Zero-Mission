#!/usr/bin/env python3

from argparse import ArgumentParser
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


WORLD_NAME = "mzm"
WORLD_PATH = Path(__file__).parents[1]
with open(WORLD_PATH / "archipelago.json", "r", encoding="utf-8") as file:
    GAME_NAME: str = json.load(file)["game"]

BUILD_PATH = WORLD_PATH / "build"
ap_path: Path


def clean_build_path():
    BUILD_PATH.mkdir(exist_ok=True)
    for child in BUILD_PATH.iterdir():
        shutil.rmtree(child, ignore_errors=True)


def call_ap_component(component: str, *args: str):
    cmd = [sys.executable, "Launcher.py", component]
    if args:
        cmd += ["--", *args]
    subprocess.check_call(cmd, cwd=ap_path)


def build_apworld():
    call_ap_component("Build APWorlds", GAME_NAME)
    apworld_name = f"{WORLD_NAME}.apworld"
    shutil.copy(ap_path.joinpath("build", "apworlds", apworld_name), BUILD_PATH / apworld_name)


def get_file_safe_name(name: str) -> str:
    return "".join(c for c in name if c not in '<>:"/\\|?*')


def generate_template():
    call_ap_component("Generate Template Options", "--skip_open_folder")
    template_name = f"{get_file_safe_name(GAME_NAME)}.yaml"
    shutil.copy(ap_path.joinpath("Players", "Templates", template_name), BUILD_PATH / template_name.replace(" ", "_"))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", default=None, help="Path to your Archipelago source code")
    args = parser.parse_args()

    ap_path = Path(args.path or os.getenv("AP_SOURCE_PATH") or os.getenv("AP_PATH") or os.getcwd())

    clean_build_path()
    build_apworld()
    generate_template()
