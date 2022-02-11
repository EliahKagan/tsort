#!/usr/bin/env python3

"""
Topological sort, like the *nix utility.

https://pubs.opengroup.org/onlinepubs/9699919799/utilities/tsort.html
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
    except CycleError:  # FIXME: Report what cycle was found.
        die('cyclic dependency, no topological ordering', Status.CYCLIC)

    for vertex in ordering:
        print(vertex)


if __name__ == '__main__':
    run()
