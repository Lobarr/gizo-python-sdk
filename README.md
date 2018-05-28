# Gizo Python SDK

[![Build Status](https://semaphoreci.com/api/v1/gizo-network/gizo-python-sdk/branches/develop/badge.svg)](https://semaphoreci.com/gizo-network/gizo-python-sdk)
[![CodeFactor](https://www.codefactor.io/repository/github/gizo-network/gizo-python-sdk/badge/master)](https://www.codefactor.io/repository/github/gizo-network/gizo-python-sdk/overview/master)
 [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/your/your-project/blob/master/LICENSE)

This is a [Gizo](https://github.com/gizo-network/gizo) compatible Python SDK which implements the JSON RPC exposed on dispatcher nodes.

<!-- toc -->

- [Installing](#installing)
- [Getting Started](#getting-started)
  * [Connecting to Gizo main network](#connecting-to-gizo-main-network)
  * [Connecting to Gizo test network](#connecting-to-gizo-test-network)
  * [Connecting to specific dispatcher](#connecting-to-specific-dispatcher)
  * [Specifying file path for config file](#specifying-file-path-for-config-file)
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
### Connecting to Gizo main network

```python
from gizo-sdk import Gizo

gizo = Gizo()

```
### Connecting to Gizo test network

```python
from gizo-sdk import Gizo

gizo = Gizo(test=True)

```
### Connecting to specific dispatcher
```python
from gizo-sdk import Gizo

url = "gizo://304e301006072a8648ce3d020106052b81040021033a0004f14a7b28af6fdf3136779e0a82e618d5f481ab0377222e71c9473e552785eb4adedfb67030b15ba1d877f9e1a06dd8a58870dd1402da7e6e@99.233.0.99:9995"
gizo = Gizo(url=url)
```
### Specifying file path for config file

```python
from gizo-sdk import Gizo

gizo = Gizo(export_file="./tmp/.gizo")

```
> Config file holds currently connected dispatcher and user's public and private keypair


> Important - config file should be kept safe as keypair could be used to execute private jobs (treat as environment variables)

## API
### Version
Returns dispatcher node's version information
```python
from gizo-sdk import Gizo
gizo = Gizo()
version = gizo.Version()
````

### Example return

```python
{
    'Version': 1, 
    'Height': 0, 
    'Blocks': ['001f176b24e37440867e1a60fdb1c8e691a29e1651e9b7b57d6eb38335d94dfe']
}
```

### PeerCount
Return the number of peers a node has
```python
from gizo-sdk import Gizo
gizo = Gizo()
count = gizo.PeerCount()
````
### BlockByHash
Returns block of specified hash

```python
from gizo-sdk import Gizo

hash = "001f176b24e37440867e1a60fdb1c8e691a29e1651e9b7b57d6eb38335d94dfe"
gizo = Gizo()
block = gizo.BlockByHash(hash)
```

## Built With

* [Hprose](https://github.com/hprose/hprose-python) - communication with dispatcher node
* [Furl](https://github.com/gruns/furl) - url parser
* [Requests](https://github.com/requests/requests) - http client library
* [Robber.py](https://github.com/vesln/robber.py) - assertion library

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