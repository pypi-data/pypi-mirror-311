from pathlib import Path, PurePosixPath
import platform
import toml
import shutil
import os


def get_config_path():
    if os.environ.get("ANTELOPE_CONFIG_PATH") is None:
        if platform.system() in ["Linux", "Darwin", "Windows"]:
            config_path = Path.home() / ".config" / "antelope" / "config.toml"

            return config_path

    else:
        config_path = Path(os.environ.get("ANTELOPE_CONFIG_PATH"))
        return config_path


def get_config():
    config_path = get_config_path()
    if not config_path.exists():
        return None
    else:
        with open(config_path, "r") as f:
            config = toml.load(f)
        return config


def validate_config_file(config):
    keys = {
        "deployment",
        "mysql",
        "s3",
        "multithreading",
        "computation",
        "folders",
        "analysis",
    }
    valid = keys.issubset(config.keys())
    return valid


def cp_st_config():
    if platform.system() in ["Linux", "Darwin", "Windows"]:
        # copy  streamlit config to home if it doesn's exist
        stconfig = Path.home() / ".streamlit" / "config.toml"
        stcredentials = Path.home() / ".streamlit" / "credentials.toml"
        if not stconfig.exists():
            stconfig.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                Path(os.path.abspath(__file__)).parent.parent
                / "configs"
                / ".streamlit"
                / "config.toml",
                stconfig,
            )
        if not stcredentials.exists():
            stcredentials.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                Path(os.path.abspath(__file__)).parent.parent
                / "configs"
                / ".streamlit"
                / "credentials.toml",
                stcredentials,
            )


def validate_config(config):
    for name, path in config["folders"].items():
        if not Path(path).exists():
            return False
    for folder in config["analysis"]["folders"]:
        if not Path(folder).exists():
            return False
    cluster_install = PurePosixPath(config["computation"]["basedir"])
    if not cluster_install.is_absolute():
        return False
    cluster_data = Path(config["computation"]["antelope_data"])
    if not cluster_data.exists():
        return False
    return True
