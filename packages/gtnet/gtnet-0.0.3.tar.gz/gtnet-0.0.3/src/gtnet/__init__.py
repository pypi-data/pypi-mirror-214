from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("package-name")
except PackageNotFoundError:
    # package is not installed
    __version__ = '0.0.1'
    pass

del version, PackageNotFoundError
