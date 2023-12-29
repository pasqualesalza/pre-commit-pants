import toml

# Read the version from pyproject.toml.
with open("pyproject.toml", "r") as f:
    pyproject_toml = toml.load(f)
    __app_name__ = pyproject_toml["tool"]["poetry"]["name"]
    __version__ = pyproject_toml["tool"]["poetry"]["version"]
