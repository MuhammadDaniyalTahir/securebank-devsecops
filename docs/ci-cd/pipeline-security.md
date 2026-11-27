# CI/CD Pipeline Security

## 1. Purpose

This document describes the security controls implemented in the SecureBank CI/CD pipeline using GitHub Actions. It explains the security objectives, potential threats, implementation decisions, and verification methods associated with securing the pipeline.

The objective is to reduce the risk of unauthorized access, malicious workflow execution, and compromise of the software delivery process.

## 2. Immutable GitHub Actions References

### 2.1 Security Objective

Third-party GitHub Actions are external dependencies that execute code within our CI runner. Therefore, their integrity is an important part of securing our software delivery pipeline.

To reduce the risk of unexpected code changes in third-party actions, we implemented SHA pinning.

Instead of referencing actions using mutable version tags, we reference specific Git commits using their full commit SHAs.

This ensures that our workflow executes the exact commits we have reviewed and selected, even if the corresponding Git tags are moved later.

### 2.2 Threat Analysis

The following security threats motivated the implementation of SHA pinning:

1. **Malicious code execution:** An attacker who compromises an action maintainer's account or release process could potentially move a version tag to point to a malicious commit. Workflows using that mutable tag could then execute the malicious code.
2. **Exposure of accessible secrets:** Malicious code executing within a CI runner could potentially access secrets exposed to its execution context, such as API keys, deployment credentials, or tokens.
3. **Unauthorized use of workflow permissions:** Malicious code could misuse the permissions granted to the workflow's `GITHUB_TOKEN` to perform unauthorized repository operations.

SHA pinning mitigates the risk of a mutable tag silently redirecting our workflow to a different commit. However, it does not guarantee that the pinned commit itself is safe or prevent an attacker from modifying our workflow configuration.

### 2.3 Implementation

We replaced mutable version-tag references with full commit SHAs obtained from the official GitHub repositories.

**1. actions/checkout**

- Release tag: `v4.4.0`
- Commit SHA: `11d5960a326750d5838078e36cf38b85af677262`

**2. actions/setup-python**

- Release tag: `v5.6.0`
- Commit SHA: `a26af69be951a213d495a4c3e4e4022e16d87065`

Our updated workflow configuration:

```yaml
- name: Checkout repository
  uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4.4.0

- name: Set up Python
  uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5.6.0
  with:
    python-version: '3.13'
```

### 2.4 Verification

We verified the action references against their official GitHub repositories using `git ls-remote`.

**Checkout verification:**

```bash
git ls-remote https://github.com/actions/checkout.git 'refs/tags/v4.4.0*'
```

**Python setup verification:**

```bash
git ls-remote https://github.com/actions/setup-python.git 'refs/tags/v5.6.0*'
```

The returned hashes matched the full commit SHAs used in our workflow configuration.

After implementing SHA pinning, we pushed the updated workflow to our GitHub repository.

The GitHub Actions workflow executed successfully, confirming that the pinned action references were usable and that our existing CI pipeline continued to function.

### 2.5 Maintenance Considerations

SHA pinning prevents automatic changes when an upstream version tag is moved. However, it also means that newer releases and security fixes are not automatically adopted.

Therefore, action updates must be handled deliberately.

When updating an action, we should:

1. Review the latest release and its security advisories.
2. Identify the corresponding full commit SHA from the official repository.
3. Verify the selected reference.
4. Update the workflow configuration.
5. Execute the CI pipeline and confirm successful operation.

This approach balances dependency integrity with the need to receive security updates.

## 3. Least-Privilege GitHub Actions Permissions

### 3.1 Security Objective

The purpose of applying this control is to ensure that the workflow only have necessary permissions to perform it's tasks. Giving additional permissions to code or workflow will increase the chances of threats and cyber attacks.

### 3.2 Threat Analysis

Currently my workflow configuration has `contents: read` permission because it only have to download source code from github repo and install dependencies and python setup. It means that API token is not able to write any changes in the repository. It don't require any other permission yet. But if I give it additional permission of `write-all` then it will increase the chances of following threats.

#### 3.2.1 Modify repository content

If compromised then attacker can modify the repo code because of providing additional permission.

#### 3.2.2 Push unauthorized commits

If compromised then attacker can push unauthorized commits and execute that malicious code as well.

#### 3.2.3 Modify branches or create release

If compromised then attacker can modify the repo and you will lose your original work if not saved locally.

### 3.3 Permission scoping

In a case where additonal permission is required to a job, only give that task required permission that is called **permission scoping**. Because there are two types of permissions.

#### 1. Workflow-level permission
It is the default permission for all jobs. Don't give unnecessary additional permission the whole workflow, because it will be harmful because it will increase the **blast radius** if compromised.

##### 2. Job-level permission
It is permission for a specific job. Only the job will recieve the additional permission that requires those permissions because job-level permissions overrides the workflow-level permissions. It will ensure the reduction in blast radius. 

### 3.4 Implementation

Our current workflow uses workflow-level permissions:

```yaml
permissions:
  contents: read
```
This permission is sufficient for the current CI workflow because it only needs to access repository contents to check out the source code and execute automated tests.

No additional repository write or package publishing permissions are currently required.

### 3.5 Verification

After explicitly mentioning this in the workflow, I pushed the code in main branch so that workflow will get executed and it must be verified that our permission is working perfectly and not restricting any required action.

## 4. Preventing Unnecessary Credential Persistence

### 4.1 Security Objective

The purpose of this security control is to prevent the GitHub token used by the checkout action from being persisted in the repository's local Git configuration. Subsequent workflow steps do not require this credential, so preventing its persistence reduces unnecessary credential exposure.

### 4.2 Threat Analysis

#### 4.2.1 Data exposure

It will cause different threats. It can execute the malicious code that can be used for many purposes. One of the main harmful intent is to download the content of private repository to external server. 

#### 4.2.2 Modify repository content

It can modify the repository files and content if respective permissions are given in the workflow. It needs write permissions for workflow to modify the repositry content but in our case we only have `read` permission so that's not possible in our case.

#### 4.2.3 Other system compromise

It will try to compromise the other systems in the same environment where runner exists.

#### 4.2.4 External communication

It will try to communicate with external servers if network allows it to do. That will be harmful for exposing the secrets as well as downloading the malicous code, exploits and continuous communication with attacker's server can also be established.

### 4.3 Implementation

I have implemented security control that credentials must not persist in the workflow when they are used in the following way:

``` yml 
with:
  persist-credentials: false
```

This setting prevents the token from being persisted in the local git configuration so that it's unavailable to subsequent steps.

### 4.4 Verification

I have pushed this updated workflow and github actions run successfully without any hurdle. 

### 4.5 Limitations

This control reduces credential exposure but does not make the workflow immune to other security threats.

- It does not prevent malicious code execution.
- It does not isolate workflow steps.
- It does not protect other credentials or sensitive files accessible to the runner.
- It does not prevent network-based data exfiltration.
