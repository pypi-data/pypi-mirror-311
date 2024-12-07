import os

from mdft.file import File
from mdft.util import Command, Options

from .file_filter import FileFilter


class FileScanner:
    @classmethod
    def _scan(cls, parent: File, options: Options, filter: FileFilter):
        for entry in os.scandir(parent.path):
            file = File.from_entry(entry)

            if filter.does_filter(file.path):
                continue

            if file.is_dir:
                cls._scan(file, options, filter)

            if options.include_files or file.is_dir:
                parent.add_child(file)

    @classmethod
    def scan(cls, blueprint: Command, filter: FileFilter) -> File:
        if not blueprint.path.exists():
            raise Exception(f"Provided path does not exist: {blueprint.path}")

        if not blueprint.path.is_dir():
            raise Exception("Provided path must be a directory")

        parent = File(blueprint.path.name, blueprint.path.parent, True)
        cls._scan(parent, blueprint.options, filter)
        return parent
