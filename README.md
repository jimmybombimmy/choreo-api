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

## API Structure

To call endpoints in our API, you will need the suffix of `/api/v1/<route>/xxx`.

For example, you can retrieve all `task_types` locally by running:

```bash
curl http://localhost:8000/api/v1/task-types/
```

Change port, or anything else for further environments, as needed.

**Note:** As the app evolves this might not be so simple

### Layered Architecture

Due to this being a relatively small application, this follows a **Layered architecture** approach.

Below outlines the structure:

```
api/       → How the outside world talks to the application
core/      → Central application concerns
db/        → How storage is connected/configured
enums/     → Reusable enumerations
models/    → What gets stored
schemas/   → What goes over the API
scripts/   → Development/test scripts
services/  → What the application does
types/     → Reusable type definitions
utils/     → Generic helpers
```

Ref:

- [You Don’t Need a Framework — You Just Need This FastAPI Structure](https://medium.com/@hadiyolworld007/you-dont-need-a-framework-you-just-need-this-fastapi-structure-e0b1f24c599f)
  - Mostly followed, with minor changes
- [full-stack-fastapi-template (GitHub)](https://github.com/fastapi/full-stack-fastapi-template)
  - Good example for FastAPI code. Not followed very heavily
