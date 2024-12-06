from setuptools import setup

name = "types-pynput"
description = "Typing stubs for pynput"
long_description = '''
## Typing stubs for pynput

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pynput`](https://github.com/moses-palmer/pynput) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `pynput`. This version of
`types-pynput` aims to provide accurate annotations for
`pynput==1.7.7`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/pynput`](https://github.com/python/typeshed/tree/main/stubs/pynput)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`693add9512ac0db5bb877e1e57fd0e46fb22158e`](https://github.com/python/typeshed/commit/693add9512ac0db5bb877e1e57fd0e46fb22158e).
'''.lstrip()

setup(name=name,
      version="1.7.7.20241127",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pynput.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pynput-stubs'],
      package_data={'pynput-stubs': ['__init__.pyi', '_info.pyi', '_util.pyi', 'keyboard/__init__.pyi', 'keyboard/_base.pyi', 'keyboard/_dummy.pyi', 'mouse/__init__.pyi', 'mouse/_base.pyi', 'mouse/_dummy.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
