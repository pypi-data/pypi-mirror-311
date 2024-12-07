import re
from pathlib import Path
from typing import Tuple

STR_INCLUDE_FILES = "include_files"
STR_INCLUDE_ROOT = "include_root"
STR_KEEP_LINE = "keep_line"
STR_FILTER = "filter"
STR_LINK = "link"


class Options:
    include_files: bool = True
    include_root: bool = False
    keep_line: bool = True
    filter: bool = True
    link: bool = True
    index: int = 0
    path: Path

    @classmethod
    def parse(cls, options: str) -> "Options":
        result = Options()
        result.path, options = parse_path_options(options)

        for option in options.split(","):
            option, value = parse_option(option)

            if option == STR_INCLUDE_FILES:
                result.include_files = value
            elif option == STR_INCLUDE_ROOT:
                result.include_root = value
            elif option == STR_KEEP_LINE:
                result.keep_line = value
            elif option == STR_FILTER:
                result.filter = value
            elif option == STR_LINK:
                result.link = value
            elif option == "":
                pass
            else:
                raise Exception(f"Unexpected option: {option}")

        return result


def parse_path_options(line: str) -> Tuple[Path, str]:
    PATH_OPTIONS_RE = r'(?:([^\s"]+)|"((?:\\.|[^"])*)")'
    matches = re.finditer(PATH_OPTIONS_RE, line)
    options = ""
    path = "./"

    matches = [match.group(1) or match.group(2) for match in matches]

    if len(matches) == 1:
        options = matches[0]

    if len(matches) == 2:
        options = matches[1]
        path = matches[0]

    if len(matches) > 2:
        raise Exception("Unexpected parameter", matches[2])

    return Path(path), options


def parse_option(option: str) -> Tuple[str, bool]:
    if option.startswith("!"):
        return option[1:].lower(), False
    return option.lower(), True
