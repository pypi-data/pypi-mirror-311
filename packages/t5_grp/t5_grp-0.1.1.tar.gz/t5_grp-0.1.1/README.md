# t5_grp

This project provides a tool for generating visual representations of CI/CD pipelines using data defined in YAML files. The tool leverages Jinja2 for templating and creates an HTML output that visually represents the stages and jobs within a pipeline, including their dependencies and artifacts.


## Table of Contents
- [Features]
- [Development Setup]
- - [Prerequisites]
- - [Build Instructions]
- [User Manual]
- [Pull Request Process]
- - [Creating a PR]
- - [Rules for PRs]
- [CI/CD Workflows]
- [License]

## Features
- YAML Pipeline Configuration
    - Support for multiple stages and jobs
    - Job dependencies management
    - Artifact tracking
    - Allow failure flags
- Visual Pipeline Representation
    - Interactive HTML output
    - Dependency arrows visualization
    - Stage-based layout
    - Artifact tracking across stages

## Configuration Example
```bash
pipeline:
- name: Example Pipeline
- stages:
  - build
  - test
- jobs:
  - name: compile
  - stage: build
  - script:
   - echo "Building..."
  - artifacts:
   - paths:
    - dist/
```

## Output Example
```bash
The tool generates an HTML visualization that shows:
- Pipeline stages in sequential order
- Jobs within each stage
- Dependencies between jobs (shown as arrows)
- Artifacts produced by each job
```

## Development Setup

### Prerequisites

To use this project, you need:

- Python 3.12 or higher
- Required Python packages:
  - - Jinja2
  - - PyYAML
- Poetry (for dependency management)

### Build Instructions

Clone the repository:
```bash
git clone https://github.com/CS6510-SEA-F24/t5-project.git
```
Build the Project:
Using Nox for Automated Builds, Tests, and Linting, file in `noxfile.py`:

We use nox to run automated sessions like testing, linting, and building the project.
Nox allows us to define a "do-all" type script to ensure everything runs in one command.

To run all sessions:

Install the dependencies using Poetry:

```bash
poetry install
```

Run application with Poetry:
```bash
poetry run cicd file_path
# e.g. poetry run cicd /Users/yoyowu/NEU/t5_grp/src/tests/test_files/valid.yaml
```

Running Tests To run all unit tests:
```bash
poetry run pytest
```

To run tests with coverage reports:
```bash
poetry run pytest --cov=src/ --cov-report=term-missing --cov-fail-under=60
```

Lint Code (Flake8): Check code style against PEP8 guidelines:
```bash
poetry run flake8 src
```

Auto-format Code(Black): Automatically format the code in src/ and tests/ to follow PEP8 guidelines:
```bash
poetry run black src
```

Run all checks (using nox)
```bash
poetry run nox -s all
```

### Installation
```bash
pip install t5_grp
```
### Usage

Basic usage:
```bash
cicd path/to/pipeline.yaml
```
With options:
```bash
cicd path/to/pipeline.yaml -o custom_output.html -t dark --stage-gap 80
```

## Pull Request Process

### Creating a PR

#### Always use feature branch to make change:

```bash
git checkout -b <branch_name> # create a new branch with <branch_name>
```

> Direct push to the `main` branch is strictly forbidden as this is the Production branch. All change
> should be merged with an approved PR.

#### Ensure your code is up-to-date with the `main` branch:

```bash
git config pull.rebase true # always use rebase to reconcile divergent branches
git pull
```

> Regularly pull from the `main` branch avoids conflicts pilling up.
> Please make sure you pull again before creating a PR.
#### Follow the PR Template:

- Your PR description should address any relevant context to help the reviewer to understand the
  PR. If this is related to an issue, reference the issue in the description.
- Make sure to use the checklist, and give explanations to any unchecked ones.

#### Check PR details:

- Make sure the origin and destination of the PR is correct, as well as everything in the Commits
  and Files changed tabs before clicking "Create Pull Request".

### Rules for PRs

#### Testing:

- Ensure all new code is properly tested.
#### Commit Guidelines:

- Use [meaningful commit messages](https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/).
  Squash commits if necessary to clean up the history.

#### Merging:

- When merging PRs, always use **SQUASH AND MERGE** to combine all changes into a single commit.

## CI/CD Workflows

This project uses **GitHub Actions** for CI/CD automation. The configured CI/CD workflows are:

- **PR Size Check**:

    - This workflow is triggered when a new PR is created, or when a new commit is pushed to an existing PR.
    - It fails if the size of PR is greater than 150 lines, and no override label is provided.


- **Pipeline Run**:
    - This workflow is triggered when:
        - A PR is created/ updated.
        - A PR is merged.
    - This workflow will execute:
        - Build: Ensures the code builds successfully.
        - Run Unit Tests: All tests must pass.
        - Test Coverage Verification: Verifies that test coverage meets minimum requirements.
        - Code Quality Checks: Checkstyle and SpotBugs
        - Artifacts Upload: Build artifacts and generated reports are uploaded after pipeline run

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.