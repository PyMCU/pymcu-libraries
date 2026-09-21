# PyMCU Libraries

The curated index of libraries that work with [PyMCU](https://pymcu.org).

PyPI carries the bytes. This repository decides what exists: a list of
distributions that are known to be PyMCU libraries, and a measured record of
which chips each one actually builds for.

```
libraries.txt          one distribution per line -- the whole submission
upstream-examples/     measurement programs for upstream entries (see below)
index.json             generated; do not edit by hand
deploy/                the Worker that serves the index from R2
```

## Submitting a library

1. Publish your library to PyPI. See the
   [authoring guide](https://docs.pymcu.org/library/authoring) for the package
   layout, the `pymcu.toml` manifest and the `pymcu.libraries` entry point.
2. Open a pull request adding one line to `libraries.txt` with your
   distribution name.

CI answers on the PR. It installs the distribution, then:

- checks the package with `pymcu lint --library`: ASCII-only sources, a valid
  manifest, an architecture dispatch whose default branch raises, and a public
  API surface matching `api-surface.lock`;
- compiles your example **for one chip per architecture**, including the ones
  you did not declare, and compares the result against your `supports.arch`.
  Declaring an architecture that does not build fails the check; building for
  one you never declared is reported so you can claim it.

Merging regenerates `index.json`.

You do not need a PR for later releases. A scheduled run re-installs the newest
version of everything listed and measures it again, so an entry says what builds
*today* rather than what built the day it was submitted -- and a library that
stops building against a new compiler is marked `broken` without anyone filing
an issue.

## Upstream libraries

Some libraries are worth listing without asking their author to adopt PyMCU's
manifest at all: an existing CircuitPython or MicroPython package on PyPI, plain
Python with no interpreter-only surface, needs nothing more than the index
saying what it provides. An `upstream` line in `libraries.txt` does that,
naming the module(s), the stdlib layer it is written against, and a
measurement program:

```
upstream <distribution> provides=<module>[,<module>...] layer=<native|micropython|circuitpython> example=<path> [name=<name>]
```

`example` is a path, relative to this repository's root, to a copy of the
library's own example, committed under `upstream-examples/<distribution>/`.
That copy exists only to measure the library; this repository never carries a
copy of the library's own code, staged or otherwise, only of the one file
compiled to test it.

**Unlike a regular submission, adding an upstream entry is a maintainer
action**, not something the library's own author opens a PR for -- there is no
manifest for them to author in the first place. A maintainer:

1. Confirms the distribution is plain Python with no PyMCU-specific surface,
   and that its own example actually exercises the library (constructs the
   object, calls a method) rather than merely importing it.
2. Commits a copy of that example under `upstream-examples/<distribution>/`.
3. Adds the `upstream` line to `libraries.txt`.

CI measures it exactly like a regular submission: one chip per architecture,
with the declared layer enabled. There is no `supports.arch` to compare the
result against, since there is nothing here that could have gotten out of
sync with a manifest that does not exist. An upstream entry whose imports are
other upstream entries is measured with them in scope -- the measurement
index names every submission of the run -- so list the dependency entries
first.

An upstream entry is re-measured on the same weekly schedule as everything
else, and is removed from `libraries.txt` (by a maintainer, again) once it
stops building -- there being no author to notify plays no part in when that
happens.

## How the index is published

Two copies of the same file, because one address is not reachable from
everywhere:

| URL | Served from | For |
|---|---|---|
| `https://libraries.pymcu.org/index.json` | R2 bucket `pymcu-libraries` via the Worker in `deploy/` | everyday use, and the web catalogue |
| `https://raw.githubusercontent.com/PyMCU/pymcu-libraries/main/index.json` | this repository | CI, containers, anything running in a data centre |

The mirror is not redundancy for its own sake. The `pymcu.org` zone runs Bot
Fight Mode, which answers 403 to requests coming from data centres -- the
playground hit exactly this, and its CI works around it by pulling toolchains
through R2's S3 endpoint instead of the public hostname. `pymcu install` runs
inside other people's CI, so the index needs an address that does not sit behind
that protection. `raw.githubusercontent.com` is public, needs no credentials,
and is already trusted by every CI runner.

The driver tries the primary and falls back to the mirror; `PYMCU_LIBRARY_INDEX`
overrides both.

R2 rather than a static site build: the index is regenerated on a schedule, and
`wrangler r2 object put` is one call with no site redeploy behind it. The
object is served with `Cache-Control: no-cache` and an ETag -- only names that
carry a fingerprint are safe to cache, a rule this project learned the hard way
on the playground.

## Regenerating locally

```bash
pip install --pre "pymcu-compiler[all]"
pymcu index build --from libraries.txt --output index.json
```

`pymcu index verify` measures what is already installed and fails on any
discrepancy; that is what the PR check runs.
