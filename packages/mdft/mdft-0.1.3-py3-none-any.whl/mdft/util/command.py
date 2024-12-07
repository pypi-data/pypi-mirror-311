import re
from pathlib import Path
from typing import List, Optional

from .line import Line
from .options import Options

PATH_OPTIONS_RE = r'(?:([^\s"]+)|"((?:\\.|[^"])*)")'
LINE_MATCHER = r"<!-- *mdft(?: +(.*))? *-->"


class Command:
    options: Options
    path: Path

    def __repr__(self):
        return f"({self.path}, {self.options})"

    def __init__(self, path: Path, options: Options):
        self.options = options
        self.path = path

    @classmethod
    def _match_command(cls, line: str) -> Optional[re.Match[str]]:
        return re.match(LINE_MATCHER, line, re.IGNORECASE)

    @classmethod
    def parse_command(cls, base: Path, line: str) -> "Command":
        matches = cls._get_line_matches(line)

        options = Options.parse(matches[1]) if len(matches) == 2 else Options()

        path = Path(matches[0])
        if not path.is_absolute():
            path = base / path

        return Command(path, options)

    @classmethod
    def _get_line_matches(cls, line: str) -> List[str]:
        match = cls._match_command(line)

        if match is None:
            raise Exception("Invalid definition")

        content = match.group(1) or ""
        matches = re.finditer(PATH_OPTIONS_RE, content)
        matches = [match.group(1) or match.group(2) for match in matches]

        if len(matches) > 2 or len(matches) < 1:
            raise Exception("Invalid definition")

        return matches

    @classmethod
    def is_command(cls, line: str) -> bool:
        return cls._match_command(line) is not None

    @classmethod
    def for_file(cls, path: Path) -> List[Line["Command"]]:
        base = path.parent
        result = []
        index = 0

        with open(path, "r+") as file:
            for line in file:
                index += 1

                if Command.is_command(line):
                    command = Command.parse_command(base, line)
                    result.append(Line(command, index))

        return result
