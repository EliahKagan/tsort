<!-- SPDX-License-Identifier: 0BSD -->

# tsort - topological sort, like the *nix utility

This Python script is similar [the `tsort` command on Unix-like
systems](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/tsort.html).

It does that job and is used in a similar way, but it does not aim for
POSIX-compliance and it is not suitable as a replacement for a system `tsort`
command.

## License

The contents of this repository are licensed under
[0BSD](https://spdx.org/licenses/0BSD.html). See **[`LICENSE`](LICENSE)**.

## Implementation details and purpose

The script file, `tsort.py`, does not actually *implement* topological sort.
Instead, it uses
[`graphlib.TopologicalSorter`](https://docs.python.org/3/library/graphlib.html#graphlib.TopologicalSorter)
from the Python standard library. Although this program can be useful to run,
my main goal is to demonstrate `graphlib` usage.
