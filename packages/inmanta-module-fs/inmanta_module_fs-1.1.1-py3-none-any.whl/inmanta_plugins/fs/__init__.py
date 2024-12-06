"""
Copyright 2024 Inmanta

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: code@inmanta.com
"""

import os

import inmanta_plugins.fs.resources  # noqa: F401
from inmanta.module import Project
from inmanta.plugins import Context, plugin


def _extend_path(ctx: Context, path: str):
    current_module_prefix = "." + os.path.sep
    if path.startswith(current_module_prefix):
        module_and_submodule_name_parts = ctx.owner.namespace.get_full_name().split(
            "::"
        )
        module_name = module_and_submodule_name_parts[0]
        if module_name in Project.get().modules.keys():
            return os.path.join(module_name, path[len(current_module_prefix) :])
        else:
            raise Exception(
                f"Unable to determine current module for path {path}, called from {ctx.owner.namespace.get_full_name()}"
            )
    return path


def determine_path(ctx: Context, module_dir: str, path: str):
    """
    Determine the real path based on the given path
    """
    path = _extend_path(ctx, path)
    parts = path.split(os.path.sep)

    modules = Project.get().modules

    if parts[0] == "":
        module_path = Project.get().project_path
    elif parts[0] not in modules:
        raise Exception(f"Module {parts[0]} does not exist for path {path}")
    else:
        module_path = modules[parts[0]]._path

    return os.path.join(module_path, module_dir, os.path.sep.join(parts[1:]))


def get_file_content(ctx: Context, module_dir: str, path: str):
    """
    Get the contents of a file
    """
    filename = determine_path(ctx, module_dir, path)

    if filename is None:
        raise Exception("%s does not exist" % path)

    if not os.path.isfile(filename):
        raise Exception(f"{path} isn't a valid file ({filename})")

    file_fd = open(filename)
    if file_fd is None:
        raise Exception("Unable to open file %s" % filename)

    content = file_fd.read()
    file_fd.close()

    return content


@plugin
def source(ctx: Context, path: "string") -> "string":  # type:ignore[name-defined]
    """
    Return the textual contents of the given file
    """
    return get_file_content(ctx, "files", path)


class FileMarker(str):
    """
    Marker class to indicate that this string is actually a reference to a file on disk.

    This mechanism is backward compatible with the old in-band mechanism.

    To pass file references from other modules, you can copy paste this class into your own module.
    The matching in the file handler is:

        if "FileMarker" in content.__class__.__name__

    """

    def __new__(cls, filename):
        obj = str.__new__(cls, "imp-module-source:file://" + filename)
        obj.filename = filename
        return obj


@plugin
def file(ctx: Context, path: "string") -> "string":  # type:ignore[name-defined]
    """
    Return the textual contents of the given file
    """
    filename = determine_path(ctx, "files", path)

    if filename is None:
        raise Exception("%s does not exist" % path)

    if not os.path.isfile(filename):
        raise Exception("%s isn't a valid file" % filename)

    return FileMarker(os.path.abspath(filename))


@plugin
def list_files(ctx: Context, path: "string") -> "list":  # type:ignore[name-defined]
    """
    List files in a directory
    """
    path = determine_path(ctx, "files", path)
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
