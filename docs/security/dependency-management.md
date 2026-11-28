# Dependency Management System

## 1. Purpose 

### Why it is necessary for security ?
Dependency management is important for maintaining application consistency and reducing supply-chain risks. If dependency versions are not controlled, pip may resolve different versions during different installations. This can introduce unexpected changes, including versions that have not been tested or may contain known vulnerabilities. It can also make deployments unpredictable because dependencies may change between workflow executions.

### Version Pinning

I am using version pinning concept in dependency management. If we specify the versions of dependencies in our declaration file then it is not sufficient. We need auto-generated lock file necessarily to secure the system. 

### Transitive dependencies vs Direct dependencies

For example, Flask requires blinker, click, werkzeug etc. to work properly. We mention Flask in our dependency declarations but didn't mention blinker and all other. So, Flask is direct and other are transitive dependencies in this case. We need to control the versions of direct as well as transitive dependencies to keep our system secure. 

### Risks
#### Reproducibility Problem
We would be unable to produce the same results while having no changes in our application due to uncontrolled version installation. To make our application run in the way that it's behaviour remains consistent, version controlling is very important.

#### Unexpected dependency changes
One time pip can resolve flask to 3.1.0 and maybe next time it resolve 3.1.5 because it find it more compatible, but we didn't test our application in newer version and that can cause problems.

#### Potential introduction of vulnerable or compromised dependency versions.

Now, we also don't know that the newer version installed by pip is secure or vulnerable. In this way our application would become vulnerable. 

## 2. Dependency Separation

### Runtime dependencies vs development dependencies

Dependencies that are necessary to only run the application are runtime dependencies, while the dependencies that are necessary to develop the application are called development dependencies. Development dependencies also include runtime dependencies.

I've write runtime dependencies in requirements.in input file.
I've write development dependencies in requirements-dev.in input file.
I used `pip-compile` command to auto-generate the lock files requirements.txt and requirements-dev.txt.

## 3. Hash Verification

I generated lockfile containing exact versions using `pip-compile` command. Firstly I generated the lockfile:
```bash
pip-compile --generate-hashes --allow-unsafe --output-file=requirements-dev.txt requirements-dev.in
```
Then I installed the dependencies using the generated lockfiles:
```bash
python -m pip install --require-hashes -r requirements-dev.txt
```

It guarantees that the exact same file is downloaded and installed using hash verification method. But keep in mind, it didn't guarantee that the dependency is not vulnerable and secure. 

## 4. Dependency Vulnerability Auditing

I have also audited all the dependencies for vulnerabilities to make my system secure.

```bash
pip-audit -r requirements-dev.txt
```
Output:
```Plain text
No known vulnerabilities found.
```

## 5. Clean Environment Verification

After implementing dependency management, I executed the workflow in order to test the function of application to make sure my application is working properly after implementing the control. 
My two environments are:

- .venv-runtime-test
- .venv-dev-test

### Created new test environment

For verification, I tested another clean environment where only installed application dependencies:

```bash
python -m pip install --require-hashes -r requirements.txt
```
This command is for **Runtime environment**. 

And for **Development environment**:
```bash
python -m pip install --require-hashes -r requirements-dev.txt
```

Both environments successfully executed the workflow, that's how I tested both environments.

### CI Verification

The dependency installation process was also verified through the
GitHub Actions CI pipeline.

- Workflow: SecureBank CI
- Trigger: Push to main
- Result: Successful
- Verification: Dependencies were installed using hash verification
  (`--require-hashes`), and the automated test suite completed successfully.
- Workflow run: [View successful workflow run](https://github.com/MuhammadDaniyalTahir/securebank-devsecops/actions/runs/46095206316)

#### I also recorded the following results
Command:
```bash
python -m pytest --cov=app --cov-report=term-missing
```
#### Result:
- Coverage: 100% of currently measured application statements.
- pip-audit: No known vulnerabilities found.

## 6. Limitations

- Lockfiles ensure controlled dependency versions and hashes, but they do not guarantee that installed packages are trustworthy or secure.
- Hash verification confirms artifact integrity against recorded hashes. It does not establish the safety of the package itself.
- `pip-audit` only identifies vulnerabilities covered by its available advisory sources. It cannot detect every unknown vulnerability or malicious package.

