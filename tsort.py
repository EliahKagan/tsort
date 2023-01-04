#!/usr/bin/env python3

# Copyright (c) 2022 Eliah Kagan
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

"""
Topological sort, like the *nix utility.

https://pubs.opengroup.org/onlinepubs/9699919799/utilities/tsort.html

This tool does that job and is used in a similar way, but it does not aim for
POSIX-compliance and it is not suitable as a replacement for a system tsort
command.

The code in this file does not actually implement topological sort. Instead, it
uses graphlib.TopologicalSorter from the Python standard library. Although this
program can be useful to run, my main goal is to demonstrate graphlib usage.
"""

import enum
import fileinput
from graphlib import CycleError, TopologicalSorter
import sys
from typing import Iterable, Iterator, NoReturn

import more_itertools
from typeguard import typechecked


@enum.unique
class Status(enum.IntEnum):
    """Failing exit statuses."""
    CYCLIC = 1
    MALFORMED = 2


@typechecked
def die(message: str, exit_status: int) -> NoReturn:
    """Prints an error message to stderr and exits with given status."""
    print(f'{sys.argv[0]}: error: {message}', file=sys.stderr)
    sys.exit(exit_status)


@typechecked
def tokens() -> Iterator[str]:
    """Yields all input tokens, reading one line at a time."""
    lines: Iterable[str] = fileinput.input()
    return (token for line in lines for token in line.split())


@typechecked
def run() -> None:
    """Read edges from stdin or a file and output a linearization."""
    tsorter: TopologicalSorter = TopologicalSorter()

    try:
        for src, dest in more_itertools.chunked(tokens(), 2):
            if src == dest:
                tsorter.add(dest)
            else:
                tsorter.add(dest, src)
    except ValueError:
        die('input specifies an odd number of vertices', Status.MALFORMED)

    try:
        ordering = list(tsorter.static_order())
    except CycleError as error:
        _, cycle = error.args  # pylint: disable=unbalanced-tuple-unpacking
        die(f'dependency cycle: {" ".join(cycle)}', Status.CYCLIC)

    for vertex in ordering:
        print(vertex)


if __name__ == '__main__':
    run()
