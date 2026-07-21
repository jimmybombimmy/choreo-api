# Choreo-API

## Description

Pending

## Local Setup

1 - To install all packages, including dev + linting, run the following command

```bash
uv sync --all-groups
```

2 - Enter the virtual environment

```bash
source .venv/bin/activate
```

3 - Run FastAPI

```bash
fastapi dev
```

## Docker Setup

Run the following command to get docker running locally

```bash
docker-compose up -d --build
```

## Pre-commit

This repo relies on pre-commit hooks to format and lint the files before pushing to Git.

See ./.pre-commit-config.yaml for the hooks initialised.

To run these hooks inside of venv all files and see the results:

```bash
uv run pre-commit run --all-file
```
