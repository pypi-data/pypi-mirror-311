# pytest-flake-detection

Continuously runs your tests to detect flaky tests. Will default to a maximum of [99](https://en.wikipedia.org/wiki/99_Flake) runs, but can be configured to run indefinitely, or any number you desire.

----

This [pytest](https://github.com/pytest-dev/pytest) plugin was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with [@hackebrot](https://github.com/hackebrot)'s [cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin) template.

## Features

- This is extremely crude as of right now, but it will run your tests a number of times and report any tests which intermittently fail, along with stats on the failures.

* TODO
    - Lax mode: if a test passes continuously for the first N runs, it will be considered a pass and not run again. This is useful for tests which are slow to run, but are not flaky. 
    - Randomised order: tests are run in a random order each time, to help detect flaky tests which are dependent on the order of other tests.
    - Playing nice with other plugins: this plugin will not interfere with other plugins which modify the test order, as it will randomise the order after all other plugins have had a chance to modify it.

## Requirements

You will need pytest, and some electricity in your computer.

## Installation

You can install "pytest-flake-detection" via [pip](https://pypi.org/project/pip) from [PyPI](https://pypi.org/project/pytest-flake-detection/):

```bash
$ pip install pytest-flake-detection
```

## Usage

```bash
$ pytest-flake-detect --max-runs 30 .
```


If you encounter any problems, please [file an issue](https://github.com/charles-turner-1/pytest-flake-detection/issues) along with a detailed description.

[Cookiecutter](https://github.com/audreyr/cookiecutter)  
[@hackebrot](https://github.com/hackebrot)  
[MIT](https://opensource.org/licenses/MIT)  
[BSD-3](https://opensource.org/licenses/BSD-3-Clause)  
[GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.txt)  
[Apache Software License 2.0](https://www.apache.org/licenses/LICENSE-2.0)  
[cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin)  
[pytest](https://github.com/pytest-dev/pytest)  
[tox](https://tox.readthedocs.io/en/latest/)  
[pip](https://pypi.org/project/pip/)  
[PyPI](https://pypi.org/project)  
