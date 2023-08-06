# Contributing

Table of Contents:

- [Getting Installed](#getting-installed)
- [Test Installation](#test-installation)

## Getting Installed

```shell
git clone https://github.com/korawica/dup-fmt.git
```

> **Note**: \
> If you want to set user and email before push your edited code,
> ```shell
> git config --local user.name "Korawich Anuttra"
> git config --local user.email "korawich.anu@gmail.com"
> git config --local credential.helper ""
> ```

```shell
python -m pip install --upgrade pip
python -m venv venv
./env/Scripts/activate
```

> **Note**: \
> For create performance, you can use `virtualenv` instead of build-in `venv`.

```shell
(venv) $ pip install -e ".[test,dev]" --no-cache
(venv) $ pip uninstall dup-fmt
```

## Test Installation

```shell
(venv) $ pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  --no-cache \
  "dup-fmt[test,dev]"
(venv) $ pytest -v
```

```shell
(venv) $ git add . ; git commit --amend --no-edit
```

## Release Code

```shell
bump2version patch
```

> **Note**: \
> `git restore .`
