#!/usr/bin/env python3
#
# Copyright (C) 2019 Simmo Saan <simmo.saan@gmail.com>
# Copyright (C) 2021 Sébastien Helleu <flashcode@flashtux.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""
Generate Python stub: API constants and functions, with type annotations.

This script requires Python 3.6+.
"""

from pathlib import Path
from typing import TextIO

import re

DOC_DIR = Path(__file__).resolve().parent / "en"

STUB_HEADER = """\
#
# WeeChat Python stub file, auto-generated by python_stub.py.
# DO NOT EDIT BY HAND!
#

from typing import Dict

"""

CONSTANT_RE = r"""\
  `(?P<constant>WEECHAT_[A-Z0-9_]+)` \((?P<type>(string|integer))\)(?: \+)?\
"""

FUNCTION_RE = r"""\
\[source,python\]
----
# prototype
def (?P<function>\w+)(?P<args>[^)]*)(?P<return>\) -> [^:]+:) \.\.\.\
"""


def write_stub_constants(stub_file: TextIO) -> None:
    """
    Write constants in the stub file, extracted from the Scripting guide.
    """
    types = {
        "integer": "int",
        "string": "str",
    }
    constant_pattern = re.compile(CONSTANT_RE)
    with open(DOC_DIR / "weechat_scripting.en.adoc") as scripting_file:
        scripting = scripting_file.read()
        for match in constant_pattern.finditer(scripting):
            stub_file.write(f'{match["constant"]}: {types[match["type"]]}\n')


def write_stub_functions(stub_file: TextIO) -> None:
    """
    Write function prototypes in the stub file, extracted from the
    Plugin API reference.
    """
    function_pattern = re.compile(FUNCTION_RE, re.DOTALL)
    with open(DOC_DIR / "weechat_plugin_api.en.adoc") as api_doc_file:
        api_doc = api_doc_file.read()
        for match in function_pattern.finditer(api_doc):
            url = f'https://weechat.org/doc/api#_{match["function"]}'
            stub_file.write(
                f"""\n
def {match["function"]}{match["args"]}{match["return"]}
    \"""`{match["function"]} in WeeChat plugin API reference <{url}>`_\"""
    ...
"""
            )


def stub_api() -> None:
    """Write Python stub file."""
    with open("weechat.pyi", "w") as stub_file:
        stub_file.write(STUB_HEADER)
        write_stub_constants(stub_file)
        write_stub_functions(stub_file)


if __name__ == "__main__":
    stub_api()
