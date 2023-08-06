__ext_version__ = "1.0.9"

import os
import json
import shutil
import typer
import zipfile
import rich.progress
import requests as req
import subprocess as sp
from PIL import Image
from dotenv import load_dotenv
from appdirs import user_cache_dir

try:
    from .functions import error, generate_jwt
    from .classes import bcolors
except ImportError:
    from functions import error, generate_jwt
    from classes import bcolors

cached_app_build_dir = os.path.join(user_cache_dir("web-ext-helper", False), "build")
cached_app_data_env_dir = os.path.join(
    user_cache_dir("web-ext-helper", False), "data", ".env"
)
cached_app_dir = os.path.dirname(os.path.dirname(cached_app_build_dir))
os.makedirs(cached_app_build_dir, exist_ok=True)
os.makedirs(os.path.dirname(cached_app_data_env_dir), exist_ok=True)

load_dotenv(cached_app_data_env_dir)

app = typer.Typer()
typer.clear()

try:
    with open("src/manifest.json", "r") as manifest_file:
        manifest_data = json.load(manifest_file)

    manifest_name = manifest_data["name"]
    manifest_name_lower = manifest_data["name"].lower()
    manifest_version = manifest_data["version"]
except FileNotFoundError:
    manifest_name_lower = None
    manifest_version = None


@app.command(help="Show the version of the extension", name="version")
def __version__():
    typer.echo(
        f"{bcolors.OKCYAN}Current web-ext-helper version: {bcolors.OKGREEN}{__ext_version__}{bcolors.ENDC}"
    )


@app.command(help="Update the extension", name="update")
def __update__():
    typer.echo(f"{bcolors.OKCYAN}Updating web-ext-helper...{bcolors.ENDC}")
    try:
        sp.run(
            [
                "pip",
                "install",
                "web-ext-helper",
                "--upgrade",
            ],
            check=True,
        )
    except sp.CalledProcessError as e:
        typer.echo(f"{bcolors.FAIL}{e.stderr.decode()}{bcolors.ENDC}", err=True)
        raise typer.Exit(1)


@app.command(help="Build the extension from the files in the src folder", name="build")
def __build__(
    compress: bool = typer.Option(
        True, "--compress", "-co", help="Compress the output"
    ),
    clean: bool = typer.Option(False, "--clean", "-cl", help="Clean the build folder"),
):
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    if clean:
        shutil.rmtree(cached_app_build_dir)
        os.mkdir(cached_app_build_dir)

    name = f"{cached_app_build_dir}/{manifest_name_lower}-{manifest_version}.zip"

    with rich.progress.Progress(
        "[progress.description]{task.description}",
        "[progress.percentage]{task.percentage:>3.0f}%",
        rich.progress.BarColumn(),
        rich.progress.TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("[green]Building...", total=100)
        total_file_count = sum(len(files) for _, _, files in os.walk("src"))
        processed_file_count = 0

        with zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED) as build:
            for root, _, files in os.walk("src"):
                for file in files:
                    if file != "src":
                        description = f"Adding file: {bcolors.OKCYAN}{os.path.relpath(os.path.join(root, file), 'src')}{bcolors.ENDC} to output file"
                        build.write(
                            os.path.join(root, file),
                            os.path.relpath(os.path.join(root, file), "src"),
                            compress_type=zipfile.ZIP_DEFLATED if compress else None,
                        )

                        processed_file_count += 1
                        progress_percentage = (
                            processed_file_count / total_file_count
                        ) * 100
                        progress.update(
                            task,
                            advance=progress_percentage
                            - progress.tasks[task].completed,
                            description=description,
                        )

    typer.echo(
        f"\n{bcolors.OKGREEN}Extension built successfully in {bcolors.PURPLE}{progress.tasks[task].finished_time:.2f}{bcolors.OKGREEN} seconds.{bcolors.ENDC}"
    )


@app.command(help="Validate the extension", name="validate")
def __validate__():
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    typer.echo(f"{bcolors.OKCYAN}Validating extension...{bcolors.ENDC}")

    try:
        sp.run(
            [
                r"C:\Program Files\nodejs\web-ext.cmd",
                "lint",
                "--source-dir",
                "src",
            ],
        )
    except FileNotFoundError:
        error(
            "web-ext not found. Please install it globally using 'npm install -g web-ext'"
        )
        raise typer.Exit(1)
    except sp.CalledProcessError as e:
        typer.echo(f"{bcolors.FAIL}{e.stderr.decode()}{bcolors.ENDC}", err=True)
        raise typer.Exit(1)


@app.command(help="Run the extension in Firefox", name="run")
def __run__():
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    typer.echo(f"{bcolors.OKCYAN}Running extension...{bcolors.ENDC}")

    try:
        sp.run(
            [
                r"C:\Program Files\nodejs\web-ext.cmd",
                "run",
                "--source-dir",
                "src",
            ],
        )
    except FileNotFoundError:
        error(
            "web-ext not found. Please install it globally using 'npm install -g web-ext'"
        )
        raise typer.Exit(1)
    except sp.CalledProcessError as e:
        typer.echo(f"{bcolors.FAIL}{e.stderr.decode()}{bcolors.ENDC}", err=True)
        raise typer.Exit(1)


@app.command(help="Sign the extension for self-hosting the extension", name="sign")
def __sign__():
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    with rich.progress.Progress(
        "[progress.description]{task.description}",
        "[progress.percentage]{task.percentage:>3.0f}%",
        rich.progress.BarColumn(),
        rich.progress.TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("[green]Signing extension...", total=100)

        try:
            api_key, api_secret = os.environ.get("AMO_API_KEY", None), os.environ.get(
                "AMO_API_SECRET", None
            )

            if api_key is None or api_secret is None:
                error(
                    "AMO_API_KEY and AMO_API_SECRET environment variables not found.\nPlease set them using the set-amo-credentials command before publishing the extension"
                )
                raise typer.Exit(1)

            sp.run(
                [
                    r"C:\Program Files\nodejs\web-ext.cmd",
                    "sign",
                    "--channel=unlisted",
                    "--source-dir",
                    "src",
                    f"--api-key={api_key}",
                    f"--api-secret={api_secret}",
                ],
            )
            progress.update(task, advance=100, description="Signing extension...")
        except FileNotFoundError:
            error(
                "web-ext not found. Please install it globally using 'npm install -g web-ext'"
            )
            raise typer.Exit(1)
        except sp.CalledProcessError as e:
            typer.echo(f"{bcolors.FAIL}{e.stderr.decode()}{bcolors.ENDC}", err=True)
            raise typer.Exit(1)


@app.command(help="Publish the extension to the Mozilla Addons Store", name="publish")
def __publish__():
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    typer.echo(f"{bcolors.OKCYAN}Publishing extension...{bcolors.ENDC}")

    try:
        api_key, api_secret = os.environ.get("AMO_API_KEY", None), os.environ.get(
            "AMO_API_SECRET", None
        )

        if api_key is None or api_secret is None:
            error(
                "AMO_API_KEY and AMO_API_SECRET environment variables not found.\nPlease set them using the set-amo-credentials command before publishing the extension"
            )
            raise typer.Exit(1)

        sp.run(
            [
                r"C:\Program Files\nodejs\web-ext.cmd",
                "sign",
                "--channel=listed",
                "--source-dir",
                "src",
                f"--api-key={api_key}",
                f"--api-secret={api_secret}",
            ],
        )
    except FileNotFoundError:
        error(
            "web-ext not found. Please install it globally using 'npm install -g web-ext'"
        )
        raise typer.Exit(1)
    except sp.CalledProcessError as e:
        typer.echo(f"{bcolors.FAIL}{e.stderr.decode()}{bcolors.ENDC}", err=True)
        raise typer.Exit(1)


@app.command(help="Delete the extension from the Mozilla Addons Store", name="delete")
def __delete__(confirm: bool = typer.Option(False, "--confirm", "-c")):
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    if not confirm:
        typer.confirm(
            f"Are you sure you want to delete the extension from the Mozilla Addons Store?: {bcolors.OKCYAN}{manifest_name} v{manifest_version}{bcolors.ENDC}",
            abort=True,
        )

    typer.echo(f"{bcolors.OKCYAN}Deleting extension...{bcolors.ENDC}")

    try:
        with open("src/manifest.json", "r") as manifest_file:
            manifest_data = json.load(manifest_file)
            guid = manifest_data["browser_specific_settings"]["gecko"]["id"]

        api_key, api_secret = os.environ.get("AMO_API_KEY", None), os.environ.get(
            "AMO_API_SECRET", None
        )

        if api_key is None or api_secret is None:
            error(
                "AMO_API_KEY and AMO_API_SECRET environment variables not found.\nPlease set them using the set-amo-credentials command before deleting the extension"
            )
            raise typer.Exit(1)

        jwt_token = generate_jwt(api_key, api_secret)

        res = req.get(
            f"https://addons.mozilla.org/api/v5/addons/addon/{guid}/delete_confirm",
            headers={
                "Authorization": f"JWT {jwt_token}",
            },
        )
        delete_confirm_token = res.json()["delete_confirm"]

        req.delete(
            f"https://addons.mozilla.org/api/v5/addons/addon/{guid}",
            headers={
                "Authorization": f"JWT {jwt_token}",
            },
            params={
                "delete_confirm": delete_confirm_token,
            },
        )

        typer.echo(
            f"{bcolors.OKGREEN}Successfully deleted extension from the Mozilla Addons Store: {bcolors.OKCYAN}{manifest_name} with Addon ID {guid}{bcolors.ENDC}"
        )
    except req.exceptions.HTTPError as e:
        typer.echo(f"{bcolors.FAIL}{e.response.text}{bcolors.ENDC}", err=True)
        raise typer.Exit(1)


@app.command(
    help="Delete the credentials for the Mozilla Addons Store",
    name="del-amo-credentials",
)
def __del_amo_credentials__():
    if os.path.exists(cached_app_data_env_dir):
        os.remove(cached_app_data_env_dir)

    typer.echo(
        f"{bcolors.OKGREEN}Successfully deleted the credentials for the Mozilla Addons Store{bcolors.ENDC}"
    )


@app.command(
    help="Set the credentials for the Mozilla Addons Store", name="set-amo-credentials"
)
def __set_amo_credentials__(
    api_key: str = typer.Option(
        ...,
        "--api-key",
        "-k",
        help="The API key for the Mozilla Addons Store",
    ),
    api_secret: str = typer.Option(
        ...,
        "--api-secret",
        "-s",
        help="The API secret for the Mozilla Addons Store",
    ),
):
    with open(cached_app_data_env_dir, "w") as env_file:
        env_file.write(f"AMO_API_KEY={api_key}\n")
        env_file.write(f"AMO_API_SECRET={api_secret}\n")

    typer.echo(
        f"{bcolors.OKGREEN}Successfully set the credentials for the Mozilla Addons Store{bcolors.ENDC}"
    )


@app.command(
    help="Clean all files and folders created by web-ext-helper (including the build folder and the cache folder)",
    name="clean",
)
def __clean__():
    shutil.rmtree("__pycache__", ignore_errors=True)
    shutil.rmtree(cached_app_dir, ignore_errors=True)

    typer.echo(
        f"{bcolors.OKGREEN}All files and folders created by {bcolors.OKCYAN}web-ext-helper{bcolors.OKGREEN} have been deleted.{bcolors.ENDC}"
    )


@app.command(
    help="View the current manifest.json file of the extension", name="manifest"
)
def __manifest__():
    if not os.path.exists("src/manifest.json"):
        error("src/manifest.json not found")
        raise typer.Exit(1)

    with open("src/manifest.json", "r") as manifest_file:
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


@app.command(help="Initialize a new extension", name="init")
def __init__():
    if os.path.exists("src/manifest.json"):
        error("src/manifest.json already exists")
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

        if logo is not None:
            os.makedirs("src/assets", exist_ok=True)
            shutil.copyfile(logo, os.path.join("src/assets", os.path.basename(logo)))

        manifest = {
            "manifest_version": 2,
            "name": name,
            "version": version,
            "description": description,
            "permissions": permissions,
            "background": {"scripts": ["background.js"]},
            "browser_action": {
                "default_icon": {logo_size[0]: f"assets/{os.path.basename(logo)}"},
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

        with open("src/manifest.json", "w") as manifest_file:
            json.dump(manifest, manifest_file, indent=2)

        with open("src/background.js", "w") as background_file:
            background_file.write("")

        typer.echo(f"{bcolors.OKGREEN}Created src/manifest.json{bcolors.ENDC}")

    ask_for_input(False, None, None, None, None, None, None, None, None)


if __name__ == "__main__":
    app()
