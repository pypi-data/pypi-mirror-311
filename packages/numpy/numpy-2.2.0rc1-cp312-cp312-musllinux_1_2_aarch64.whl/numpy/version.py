
"""
Module to expose more detailed version info for the installed `numpy`
"""
version = "2.2.0rc1"
__version__ = version
full_version = version

git_revision = "de271f1dcecad4d9fd9297101fe73987b9111eaf"
release = 'dev' not in version and '+' not in version
short_version = version.split("+")[0]
