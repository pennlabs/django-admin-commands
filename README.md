# PyPI Template

This template repo contains all the sample configuration needed to create a PyPI package following all of Penn Labs' suggested configuration.

## Installation

Click the green "Use this template" button and make a new repo with your desired name. Create a new folder to hold your reusable package. You should write tests in the `tests` directory. Run the provided init script `./init.sh <name of project> <name of github repo> <name of pypi package>` to configure most of the project. See the configuration section for final changes that need to be made. Follow the Usage instructions when developing and releasing new versions. You can also rename `README.md.template` to `README.md` (replacing this file) to get a basic Readme.

## Features

* CircleCI
  * Workflow to test and publish your project to PyPI using contexts to keep PyPI credentials safe
* Tox
  * Python 3.4-3.7 and Django 2.0-2.2 testing environments
  * Testing, linting, and code coverage configuration
* Git
  * .gitignore file to prevent common unnecessary files from being committed
* MIT License

## Usage

### Developing

* Development should happen on a feature branch and changes should be merged through a Pull Request
* `CHANGELOG.md` should be constantly updated with features being developed. The date for an unreleased version should just be `UNRELEASED`

### Releasing a new version

In the master branch:

* Update `VERSION` in `setup.py`
* Change the release date of the new version to the current date (YYYY-MM-DD) in `CHANGELOG.md`
* Commit your changes with the message "Release x.y.z"
* Tag your commit: `git tag -a x.y.z -m "Release x.y.z"`
* Push your changes to Github: `git push` and `git push --tags`

CircleCI will then build and publish the new version to PyPI

## Configuration

| File               | Line | Description                                                        |
|--------------------|------|-------------------------------------------------------------------------------------|
| setup.py           | 37   | Add a short description of your project here                       |
| tests/settings.py  | 12   | Replace this line with the dotted path to your package's AppConfig |
| tests/urls.py      | 5    | Replace the namespace with the namespace of your project           |
