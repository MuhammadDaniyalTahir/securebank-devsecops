# SecureBank DevSecOps

An educational banking API project focused on secure software
development, application security, and DevSecOps engineering practices.

## Project Goals

-   Build a Python Flask banking API.
-   Apply security controls throughout the software development
    lifecycle.
-   Automate application testing and security scanning.
-   Build and scan Docker images.
-   Implement software supply-chain security.
-   Deploy securely using Kubernetes.
-   Develop practical skills in security automation, infrastructure
    hardening, and secure CI/CD.

## Technology Stack

-   **Language:** Python 3.13
-   **Framework:** Flask
-   **Database:** SQLite (planned)
-   **Testing:** Pytest, pytest-cov
-   **CI/CD:** GitHub Actions
-   **Application Security:** SAST, SCA, and secret scanning (planned)
-   **Containerization:** Docker (planned)
-   **Container Security:** Trivy (planned)
-   **Supply-Chain Security:** Syft, Cosign (planned)
-   **Infrastructure Security:** Terraform, Checkov (planned)
-   **Runtime Security:** Falco (planned)

## Project Status

### Phase 1: Project Foundation

-   [x] Initialize Git repository.
-   [x] Configure Python virtual environment.
-   [x] Establish application and development dependencies.
-   [x] Implement Flask application factory.
-   [x] Create initial health-check endpoint.
-   [x] Configure Pytest fixtures and test client.
-   [x] Implement initial automated health-check tests.
-   [x] Verify test execution and code coverage.
-   [x] Create GitHub repository and configure SSH authentication.
-   [x] Push local project to GitHub.
-   [x] Configure initial GitHub Actions CI workflow.
-   [x] Automate dependency installation and test execution.
-   [x] Verify successful CI execution on GitHub.

### Current CI Pipeline

The initial GitHub Actions workflow automatically executes on:

-   Pushes to the `main` branch.
-   Pull Request events.

The pipeline currently performs the following steps:

1.  Check out repository source code.
2.  Set up Python 3.13.
3.  Install application and development dependencies.
4.  Execute automated tests using Pytest.

### Upcoming Work

-   Improve CI pipeline security and reliability.
-   Introduce security testing and vulnerability scanning.
-   Implement database integration.
-   Develop user registration and authentication.
-   Implement secure account management and transactions.
-   Introduce Docker and container security.
-   Implement software supply-chain security.
-   Deploy and secure the application using Kubernetes.

## Development Philosophy

This project follows a security-first engineering approach:

**Requirements → Threat Modeling → Secure Design → Implementation → Code
Review → Testing → Security Automation**

Each feature is developed incrementally, with attention to security
requirements, potential attack scenarios, testing, and engineering
decisions.

This is an educational simulation. It is not intended for real banking
operations or financial transactions.
