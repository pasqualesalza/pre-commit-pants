import toml

__app_name__ = "pre-commit-pants"

# Read the version from pyproject.toml.
with open("pyproject.toml", "r") as f:
    pyproject_toml = toml.load(f)
    __version__ = pyproject_toml["tool"]["poetry"]["version"]
