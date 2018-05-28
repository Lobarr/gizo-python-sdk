# Gizo Python SDK

[![Build Status](https://semaphoreci.com/api/v1/gizo-network/gizo-python-sdk/branches/develop/badge.svg)](https://semaphoreci.com/gizo-network/gizo-python-sdk)
[![CodeFactor](https://www.codefactor.io/repository/github/gizo-network/gizo-python-sdk/badge/master)](https://www.codefactor.io/repository/github/gizo-network/gizo-python-sdk/overview/master)
 [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/your/your-project/blob/master/LICENSE)

This is a [Gizo](https://github.com/gizo-network/gizo) compatible Python SDK which implements the JSON RPC exposed on dispatcher nodes

<!-- toc -->

- [Installing](#installing)
- [Getting Started](#getting-started)
- [API](#api)
- [Built With](#built-with)
- [Versioning](#versioning)
- [Contributing](#contributing)
  * [Prerequisites](#prerequisites)
  * [Setup Instructions](#setup-instructions)
  * [Guidelines](#guidelines)
  * [Style guideline](#style-guideline)
- [Tests](#tests)
- [Licensing](#licensing)
- [Authors](#authors)

<!-- tocstop -->

## Installing

All you need to do to get this sdk is to install using pip by running the following command:

```shell
pip install gizo-sdk
```
> Not deployed yet

## Getting Started

```python
from gizo-sdk import Gizo

gizo = Gizo()
```

## API
Supported methods documented at [API](https://github.com/Lobarr/gizo-python-sdk/wiki/API)

## Built With

* [Hprose](https://github.com/hprose/hprose-python) - used for communication with dispatcher node
* [Furl](https://github.com/gruns/furl) - used for parsed url
* [Requests](https://github.com/requests/requests) - used for make API calls

## Versioning


We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/gizo-network/gizo-python-sdk/tags). 

## Contributing
We welcome and appreciate contributions from anyone regardless of magnitude of fixes. Just make sure to have fun while at it! If you'd like to contribute, follow the below instructions to setup a dev environment and make sure your contributions follow our coding guidelines.

### Prerequisites
* Python >= 3.5.6 - [Install](https://www.python.org/downloads/release/python-365/)
* Pip - [Install](https://pip.pypa.io/en/stable/installing/)
* Pytest
```shell
pip install pytest
```

### Setup Instructions
* Fork the repo
* Clone the repo by running the following command
```shell
git clone https://github.com/gizo-network/gizo-python-sdk.git
cd gizo-python-sdk
```
* Change git remote origin to your fork and upstream to this repo
```shell
git remote set-url origin https://github.com/USERNAME/gizo-python-sdk.git
git remote add upstream https://github.com/gizo-network/gizo-python-sdk.git
```
> replace USERNAME with your github username
* Create virtual environment and activate
```shell
python3 -m venv venv
source ./venv/bin/activate
```
* Install dependencies
```shell

pip install -r requirements.txt
```

If you've made it here, you're all set!

### Guidelines
* Stick to [git branching model](http://nvie.com/posts/a-successful-git-branching-model/)
    * Make pull requests from your feature or hotfix branches into the develop branch
* Push to the origin of your forked repo and make pull requests to the develop branch
    * Pull requests straight to master would be rejected 
* Commit messages should be prefixed with the modules they modify.
    * E.g `gizo, utils: example message`

### Style guideline

* Linting is enforced by pylint with the aid of the `.pylinrc` file
## Tests

To run tests, you'd need have pytest installed. Run the following commands to run tests

```shell
pytest 
```

## Licensing

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Authors

* **Jesuloba Egunjobi** - [Lobarr](https://github.com/Lobarr)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.