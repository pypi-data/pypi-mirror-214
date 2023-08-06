"""Top-level package for basic_template_repo."""
import os
from pathlib import Path
import toml


__package_name__ = "pyxy3d"
__version__ = "v0.0.17"

__author__ = """Mac Prible"""
__email__ = "prible@gmail.com"
__repo_owner_github_user_name__ = "mprib"
__repo_url__ = (
    f"https://github.com/{__repo_owner_github_user_name__}/{__package_name__}/"
)
__repo_issues_url__ = f"{__repo_url__}issues"


# set up local app data folder and logging
__app_dir__ = Path(os.getenv("LOCALAPPDATA"), __package_name__)
__app_dir__.mkdir(exist_ok=True, parents=True)

# create a toml file for user settings in LOCALAPPDATA and default the project folder to USER
__settings_path__ = Path(__app_dir__, "settings.toml")

__user_dir__ = Path(os.getenv("USERPROFILE"))
# __user_dir__.mkdir(exist_ok=True,parents=True)

if __settings_path__.exists():
    USER_SETTINGS = toml.load(__settings_path__)
else:
    # default to storing pyxy projects in user/__package_name__
    USER_SETTINGS = {"recent_projects":[],
                     "last_project_parent":str(__user_dir__) # default initially to home...this will be where the 'New' folder dialog starts
                     } 

    
    with open(__settings_path__, "a") as f:
        toml.dump(USER_SETTINGS, f)


__log_dir__ = Path(__app_dir__, "logs")
__log_dir__.mkdir(exist_ok=True, parents=True)

# a helpful reference
__root__ = Path(__file__).parent.parent

print(f"Thank you for using {__package_name__}!")
print(f"This is printing from: {__file__}")
print(f"Source code for this package is available at: {__repo_url__}")
print(
    f"Data and Log files associated with {__package_name__} are stored in {__app_dir__}"
)


def get_config(session_directory: Path) -> dict:
    """
    A broadly useful little function to get the config file
    """
    config_path = Path(session_directory, "config.toml")

    with open(config_path, "r") as f:
        config = toml.load(config_path)
    return config
