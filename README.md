# py-envdefault-argparse
A Python3 library which enables a custom EnvDefault action for the ArgParse utility; this functionality is a convention among DevOps Python tooling.

When using argparse, pipenv, and this module, users have the capability to
specify that their applications receive arguments via command-line flags,
environment variables, and/or `.env` files.

## Installation

```bash
pipenv install git+git@github.com:rewardStyle/py-envdefault-argparse.git#egg=envdefault
# To install and lock all dependencies properly, install a specific sha:
pipenv install -e git+git@github.com:rewardStyle/py-envdefault-argparse.git@<GIT_SHA>#egg=envdefault
```

## Use Cases

Use when creating a Python3 tool which requires sensitive information ( such as API tokens )
to be supplied to the application at runtime.
This information can be supplied as an environment variable, in an `.env` file,
or with flags as direct arguments to the application on the command line.

```python
import argparse
from envdefault.envdefault import EnvDefault


CONFIG = None


def main():
    print ( f"The username is {CONFIG.username}" )


if __name__ == '__main__':
    parser = argparse.ArgumentParser ( description='description' )
    parser.add_argument ( "--username", default='guest', required=True, action=EnvDefault )
    parser.add_argument ( "--password", required=True, action=EnvDefault )
    CONFIG = parser.parse_args()
    main()
```

## The WHYs

### Why was this module developed ?

DevOps tooling often requires authenticating with services,
such as APIs for Google, GitHub, DataDog, etc. Sensitive information
such as credentials and API tokens cannot be included in tool repos,
or in containers used to execute the tools.

A common pattern then emerged where the sensitive info was being supplied
in a myriad of ways. Using pipenv and `.env` files makes local development
and usage easy without requiring the developer to constantly modify and
verify their global environment variables.
And execution environments such as Jenkins or CircleCI means that
the applications can still leverage environment variables ( preferred )
or command line arguments at runtime.

Creating the custom EnvDefault action allows tool developers to support
all these conventions within a single `argparse.parser.add_argument()` call;
and furthermore allows all DevOps Python tooling to take advantage of
the capabilities in a uniform manner ( where previously, tools had been
copy/pasting custom argparse logic ).
