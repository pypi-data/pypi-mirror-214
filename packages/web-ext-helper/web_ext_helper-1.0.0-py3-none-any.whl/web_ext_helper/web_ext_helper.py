import os
import json
import shutil
import typer
import zipfile
from PIL import Image


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def error(message: str):
    typer.echo(f"{bcolors.FAIL}Error: {message}{bcolors.ENDC}", err=True)
    raise typer.Exit(1)


app = typer.Typer()
typer.clear()

try:
    with open("manifest.json", "r") as manifest_file:
        manifest_data = json.load(manifest_file)

    name = manifest_data["name"].lower()
    version = manifest_data["version"]
except FileNotFoundError:
    name = None
    version = None


@app.command(help="Build the extension", name="build")
def __build__(
    name: str = typer.Option(None, "--name", "-n", help="Name of the build"),
    version: str = typer.Option(
        version,
        "--version",
        "-v",
        help="Specify the version of the extension",
    ),
    new_version: bool = typer.Option(
        False,
        "--new-version",
        "-nv",
        help="Create a new version of the extension",
    ),
    clean: bool = typer.Option(False, "--clean", "-c", help="Clean the builds folder"),
):
    if not os.path.exists("manifest.json"):
        error("manifest.json not found")
        raise typer.Exit(1)

    if version is not None and new_version:
        error("Cannot specify both version and new-version")
        raise typer.Exit(1)

    if name is None:

        def __get_zip_name__(version: str, new_version: bool = False) -> str:
            def update_manifest(version: str):
                with open("manifest.json", "r") as manifest:
                    manifest_data = json.load(manifest)

                with open("manifest.json", "w") as manifest:
                    manifest_data["version"] = version
                    json.dump(manifest_data, manifest, indent=2)

            def get_new_version(version: str) -> str:
                major, minor, patch = version.split(".")
                patch = int(patch)
                minor = int(minor)
                major = int(major)

                if patch == 9:
                    patch = 0
                    minor += 1
                else:
                    patch += 1

                if minor == 9:
                    minor = 0
                    major += 1

                return f"{major}.{minor}.{patch}"

            if new_version:
                version = get_new_version(version)
                update_manifest(version)

            return f"{name}-{version}.zip"

        name = __get_zip_name__(version, new_version)

    if clean:
        shutil.rmtree("builds")
        shutil.rmtree("__pycache__")
        os.mkdir("builds")

    def write_dir(build, dirname):
        for filename in os.listdir(dirname):
            if filename != name:
                if os.path.isfile(os.path.join(dirname, filename)):
                    build.write(os.path.join(dirname, filename))
                else:
                    write_dir(build, os.path.join(dirname, filename))

    with zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED) as build:
        for filename in os.listdir("."):
            if filename != name and (os.path.isfile(filename) or filename == "assets"):
                if os.path.isfile(filename):
                    build.write(filename)
                else:
                    write_dir(build, filename)

    shutil.move(name, os.path.join("builds", name))


@app.command(help="Create a manifest.json file for the extension", name="manifest")
def __manifest__(
    create: bool = typer.Option(
        False, "--create", "-c", help="Create a new manifest.json file"
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-o", help="Overwrite the manifest.json file"
    ),
):
    if create:
        if os.path.exists("manifest.json") and not overwrite:
            error("manifest.json already exists")
            raise typer.Exit(1)

        def ask_for_input(
            is_validation,
            name,
            version,
            description,
            permissions,
            logo,
            browser_action_title,
            strict_min_version,
            app_id,
        ):
            typer.clear()
            name = typer.prompt("Name of the extension (required)", default=name)
            version = typer.prompt(
                "Version of the extension",
                default=version if is_validation else "1.0.0",
            )
            if len(version.split(".")) != 3:
                error("Version must follow the pattern major.minor.patch")
                raise typer.Exit(1)
            description = typer.prompt(
                "Description of the extension (required)", default=description
            )
            permissions = typer.prompt(
                "Permissions of the extension (separated by ',')",
                default=", ".join(permissions) if is_validation else "",
                show_default=True,
            )
            permissions = (
                list(map(lambda x: x.strip(), permissions.split(",")))
                if permissions != ""
                else []
            )
            logo = typer.prompt(
                "Path to logo of the extension (leave blank for none)",
                default=(logo if logo is not None else "") if is_validation else "",
                show_default=False if not is_validation else True,
            )
            if logo == "":
                logo = None
            else:
                if not os.path.exists(logo):
                    error("Logo not found")
                    raise typer.Exit(1)

                try:
                    Image.open(logo)
                except:
                    error("Invalid image")
                    raise typer.Exit(1)
            browser_action_title = typer.prompt(
                "Title of the browser action",
                default=browser_action_title if is_validation else name,
            )
            strict_min_version = typer.prompt(
                "Strict minimum version of Firefox",
                default=strict_min_version if is_validation else 48.0,
                type=float,
            )
            app_id = typer.prompt("App ID of the extension (required)", default=app_id)

            if not typer.confirm(
                f"""
Name: {name}
Version: {version}
Description: {description}
Permissions: {permissions}
Logo: {logo}
Browser action title: {browser_action_title}
Strict minimum version: {strict_min_version}
App ID: {app_id}
""",
                default=True,
            ):
                return ask_for_input(
                    True,
                    name,
                    version,
                    description,
                    permissions,
                    logo,
                    browser_action_title,
                    strict_min_version,
                    app_id,
                )

            if name == "" or description == "" or app_id == "":
                error("Name, description and app ID are required")
                raise typer.Exit(1)

            if logo != None and not os.path.exists(logo):
                error("Logo not found")
                raise typer.Exit(1)

            if logo is not None:
                logo_size = Image.open(logo).size
            else:
                logo_size = (32, 32)

            manifest = {
                "manifest_version": 2,
                "name": name,
                "version": version,
                "description": description,
                "permissions": permissions,
                "background": {"scripts": ["background.js"]},
                "browser_action": {
                    "default_icon": {logo_size[0]: logo},
                    "default_title": browser_action_title,
                }
                if logo is not None
                else {
                    "default_title": browser_action_title,
                },
                "browser_specific_settings": {
                    "gecko": {"id": app_id, "strict_min_version": strict_min_version}
                },
            }

            with open("manifest.json", "w") as manifest_file:
                json.dump(manifest, manifest_file, indent=2)

            typer.echo(f"{bcolors.OKGREEN}Created manifest.json{bcolors.ENDC}")

        ask_for_input(False, None, None, None, None, None, None, None, None)

    else:
        if not os.path.exists("manifest.json"):
            error("manifest.json not found")
            raise typer.Exit(1)

        with open("manifest.json", "r") as manifest_file:
            manifest_data = json.load(manifest_file)

        logo_data = manifest_data["browser_action"].get("default_icon", None)
        if logo_data is not None:
            logo_path = list(logo_data.values())[0]
            logo_size = list(logo_data.keys())[0]
        else:
            logo_path = None
            logo_size = None

        typer.echo(
            f"""
Name: {manifest_data["name"]}
Version: {manifest_data["version"]}
Description: {manifest_data["description"]}
Permissions: {manifest_data["permissions"]}
Logo: {logo_path}
Logo size: {logo_size} px
Browser action title: {manifest_data["browser_action"]["default_title"]}
Strict minimum version: {manifest_data["browser_specific_settings"]["gecko"]["strict_min_version"]}
App ID: {manifest_data["browser_specific_settings"]["gecko"]["id"]}
"""
        )


if __name__ == "__main__":
    app()
