import sys

_names = sys.builtin_module_names

if ("posix" not in _names) and ("nt" in _names):
    from mslex import quote
else:
    from shlex import quote
