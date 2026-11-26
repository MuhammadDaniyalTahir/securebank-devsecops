# Security Controls Register

## 1. Purpose

This register provides a centralized inventory of security controls implemented or planned for the SecureBank project. It tracks each control's category, implementation status, and associated technical documentation.

Detailed implementation decisions, security rationale, and verification evidence are maintained in their respective documentation files.

## 2. Security Controls

| ID | Security Control | Category | Status | Documentation |
|---|---|---|---|---|
| SC-001 | Least-privilege GitHub Actions permissions | CI/CD Security | Verified | [GitHub Actions](../ci-cd/github-actions.md) |
| SC-002 | Immutable GitHub Actions references using commit SHA pinning | Supply Chain Security | Verified | [Pipeline Security](../ci-cd/pipeline-security.md#2-immutable-github-actions-references) |

## 3. Status Definitions

| Status | Definition |
|---|---|
| Planned | Identified but implementation has not started |
| In Progress | Implementation is underway |
| Implemented | Control has been implemented but verification is incomplete |
| Verified | Implementation has been tested and supporting evidence recorded |
| Needs Improvement | Control exists but requires further improvement |

## 4. Maintenance

- Add controls when they are identified during requirements analysis or threat modeling.
- Update their status as implementation and verification progress.
- Link each control to its detailed technical documentation.
- Keep verification claims supported by actual test results or other evidence.
- Update this register whenever a control's implementation status changes.
