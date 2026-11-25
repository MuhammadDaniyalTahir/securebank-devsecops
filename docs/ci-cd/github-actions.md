# GitHub Actions CI Workflow

## 1. Purpose

This document explains how Continuous Integration (CI) is implemented in the SecureBank project using GitHub Actions. It describes the workflow configuration, execution process, triggers, job configuration, and automated testing mechanism to help developers understand how our CI pipeline operates.

## 2. Continuous Integration Overview

Continuous Integration (CI) is a software development practice in which developers frequently integrate their code changes into a shared repository. Each integration can trigger automated processes, such as building the application and executing tests, to validate newly introduced changes.

CI addresses the problem of identifying defects and regressions that may occur when new code is integrated with existing functionality. Instead of relying entirely on manual testing after every change, automated checks provide developers with faster feedback about potential issues.

In SecureBank, we use GitHub Actions to automate our CI process. When commits are pushed to the `main` branch or pull request events occur, our configured workflow executes the automated test suite to check whether the application continues to behave as expected.

## 3. Workflow Configuration

GitHub Actions requires workflow configuration files to be stored inside the `.github/workflows/` directory at the root of the repository.

Our workflow configuration is maintained in:

`.github/workflows/secure-pipeline.yml`

The workflow uses the following configuration:

```yaml
name: SecureBank CI
```

The `name` property defines the workflow's display name in the GitHub Actions interface. The actual filename is `secure-pipeline.yml`, whereas its display name is `SecureBank CI`.

### 3.1 Workflow Permissions

Our workflow explicitly defines the following permissions:

```yaml
permissions:
  contents: read
```

This configuration grants the workflow's `GITHUB_TOKEN` read-only access to repository contents.

We follow the principle of least privilege by granting only the permissions currently required by our CI workflow. Since our current pipeline only needs to check out the repository and execute tests, read-only repository access is sufficient.

## 4. Workflow Triggers

A workflow trigger defines the event that causes a GitHub Actions workflow to execute. It allows us to automate validation whenever specific activities occur in our repository.

### 4.1 Push Event

```yaml
push:
  branches:
    - main
```

This configuration triggers the workflow whenever commits are pushed to the `main` branch.

Pushes to other branches do not trigger the workflow through this event.

### 4.2 Pull Request Event

```yaml
pull_request:
```

This configuration triggers the workflow when pull request events occur.

Since we haven't specified a branch filter, the workflow is not restricted to pull requests targeting a particular branch.

This allows our CI pipeline to validate proposed changes before they are merged into the target branch.

## 5. Job Configuration

A job is a group of steps that execute together on a specified runner environment. Each job is identified by a unique job ID within the workflow.

Our SecureBank CI workflow currently contains one job:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
```

### 5.1 Job ID

The job ID is `test`. It identifies the job within our workflow.

### 5.2 Runner Configuration

We use `runs-on: ubuntu-latest` to specify the execution environment.

GitHub Actions provisions a GitHub-hosted Ubuntu runner to execute the job's steps.

The runner provides an isolated execution environment for checking out our source code, configuring Python, installing dependencies, and executing automated tests.

## 6. Workflow Execution Steps

Our `test` job consists of four steps that execute sequentially by default.

### 6.1 Checkout Repository

Uses `actions/checkout@v4` to check out the repository's source code into the runner's workspace.

This makes the repository files available to subsequent workflow steps.

### 6.2 Set Up Python

Uses `actions/setup-python@v5` to configure Python 3.13 in the runner environment.

This helps maintain consistency in the Python version used by our CI pipeline.

### 6.3 Install Dependencies

This step installs the required application and development dependencies.

Our workflow executes the following commands:

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

The first command upgrades `pip`, the Python package installer, to its latest available version.

The second command installs the dependencies defined in `requirements-dev.txt`. This file also includes application dependencies through `requirements.txt`.

Separating dependency installation from the testing step makes the workflow easier to understand and maintain.

### 6.4 Run Automated Tests

Executes:

```bash
python -m pytest -v
```

This command discovers and runs our automated test suite.

We use `python -m pytest` to execute Pytest through the configured Python interpreter. The `-v` option enables verbose output, displaying individual test names and their execution results.