import shutil
import os
import subprocess
from pathlib import Path
import toml


def main() -> int:
    root_path = Path(__file__).parent.parent.parent

    # region Read config values from pyproject.toml
    # cfg = Config(str(root_path / "pyproject.toml"))
    cfg = toml.load(root_path / "pyproject.toml")
    # print(cfg)
    cfg_pkg_name = str(cfg["custom"]["metadata"]["pkg_out_name"])
    cfg_entry_name = str(cfg["custom"]["metadata"]["entry_point_name"])
    cfg_build_dir = str(cfg["custom"]["metadata"]["build_dir"])
    cfg_build_readme = str(cfg["custom"]["metadata"]["build_readme"])
    cfg_build_license = str(cfg["custom"]["metadata"]["build_license"])
    # endregion Read config values from pyproject.toml

    # region Set up build and dist directories
    build_path = root_path / cfg_build_dir
    if build_path.exists():
        shutil.rmtree(build_path, ignore_errors=True)
    build_path.mkdir(parents=True, exist_ok=True)

    dist_path = root_path / "dist"
    if dist_path.exists():
        shutil.rmtree(dist_path, ignore_errors=True)
    # endregion Set up build and dist directories

    # region Copy sphinx_cli_help directory to build directory
    dev_help_path = root_path / "sphinx_cli_help"
    build_dev_help_path = build_path / cfg_pkg_name
    shutil.copytree(dev_help_path, build_dev_help_path)
    # endregion Copy sphinx_cli_help directory to build directory

    # region Readme
    # Copy README.md to build directory
    if cfg_build_readme:
        readme_path = Path(cfg_build_readme)
        if not readme_path.is_absolute():
            readme_path = root_path / readme_path
        if readme_path.exists():
            shutil.copy(readme_path, build_path)
    # endregion Readme

    # region License
    if cfg_build_license:
        license_path = Path(cfg_build_license)
        if not license_path.is_absolute():
            license_path = root_path / license_path
        if license_path.exists():
            shutil.copy(license_path, build_path)

    shutil.copy(root_path / "pyproject.toml", build_path)
    # endregion License

    # region update pyproject.toml
    # open pyproject.toml, replace sphinx_cli_help and cli-hlp with config values
    with open(build_path / "pyproject.toml", "r") as f:
        content = f.read()
        content = content.replace("sphinx_cli_help", cfg_pkg_name)
        content = content.replace("cli-hlp", cfg_entry_name)
    with open(build_path / "pyproject.toml", "w") as f:
        f.write(content)
    # endregion update pyproject.toml

    _process_interactive_hlp(build_dev_help_path, cfg_entry_name, cfg_pkg_name)

    # region Run Poetry Build on build directory
    env = os.environ.copy()
    subprocess.run(["poetry", "build", "--no-interaction", "-C", str(build_path)], env=env)
    shutil.copytree(build_path / "dist", dist_path)
    # clear build directory
    shutil.rmtree(build_path, ignore_errors=True)
    # endregion Run Poetry Build on build directory

    return 0


def _process_interactive_hlp(build_dev_help_path: Path, cfg_entry_name: str, cfg_pkg_name: str) -> None:
    i_help = build_dev_help_path / "cli" / "interactive_hlp.py"
    with open(i_help, "r") as f:
        content = f.read()
        content = content.replace("cli-hlp", cfg_entry_name)
        content = content.replace("sphinx_cli_help", cfg_pkg_name)

    with open(i_help, "w") as f:
        f.write(content)


if __name__ == "__main__":
    SystemExit(main())
