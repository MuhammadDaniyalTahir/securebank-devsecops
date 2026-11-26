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
