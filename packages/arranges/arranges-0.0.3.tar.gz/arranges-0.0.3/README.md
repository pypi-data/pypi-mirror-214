# Arranges

## Range string fields for Pydantic BaseModels

I needed a way to parse batches of byte, row and line and other object ranges
in my `merge-files` app, in a way that I can just drop it in as a string field
type. The reason for this is so the machine-generated command line help is
flat and readable by humans.

It it kinda grew into a monster so I've split it out into this separate
package. It gives a couple of classes for dealing with ranges:

* `Range`, a class that can be constructed from Python-style slice notation
  strings (e.g. `"1:10"`, `"0x00:0xff`, `":"`), range-likes, iterables of
  int-like objects. It has convenient properties lke being iterable, immutable,
  has a stable string representation and matching hash, it can be treated
  like a `set` and its constructor is compatible with `range` and `slice`.
* The `Ranges` class is similar but supports holes in ranges - it's an ordered,
  mutable list of non-overlapping `Range` objects that simplifies as data is
  added.

## Constraints

I made it to select lines or bytes in a stream of data, so it:

* only supports `int`s;
* does not allow negative indices, the minimum is 0 and the maximum is
  unbounded;
* it's compatible with `range` and `slice`, but `step` is fixed to `1`. This
  may change in the future;
* does not support duplicate ranges. Ranges are merged together as they are
  added to the `Ranges` object;
* it is unpydantic in that its constructors are duck-typed, which is what I
  need; and
* it violates the Zen of Python by having multiple ways to do the same thing,
  but it's also useful.
* Currently the interface is *unstable*, so lock the exact version in if you
  don't want breaking changes.

## Installation

`pip install arranges` if you want to use it. You'll need Python 3.10 or
above.

### Dev setup

To add features etc you'll ideally need `git`, `make`, `bash` and something
with a debugger. Config for Visual Studio Code is included.

Clone the repo and `make dev` to make the venv, install dependencies, then
`code .` to open the project up in the venv with tests and debugging and all
that jazz.

Type `make help` to see the other options, or run the one-liner scripts in the
`./build` dir if you want to run steps without all that fancy caching nonsense.

## Usage

* [RTFM](https://bitplane.github.io/arranges/)
* Read [the tests](../arranges/tests/), which have full coverage.
* [Read the API docs](../docs/api.md)

## License

Free as in freedom from legalese; the [WTFPL with a warranty clause](../LICENSE).

Political note: I don't want to live in a world where lawyers tell me how to
speak. If you don't trust me enough to use the WTFPL then you shouldn't be
running my code in the first place.
