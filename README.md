# devops-flask-app

A production-grade DevOps reference implementation demonstrating containerisation, reverse proxying, CI/CD automation, and security scanning using industry-standard tooling.

![CI/CD Pipeline](https://github.com/ParmeetBhamrah/devops-flask-app/actions/workflows/ci.yml/badge.svg)

---

## Overview

This project implements a fully containerised web application backed by a structured CI/CD pipeline. It is intended to demonstrate practical application of core DevOps principles, including infrastructure as code, immutable deployments, environment-based configuration, and automated quality assurance.

| Concept | Implementation |
|---|---|
| Version Control | Git + GitHub |
| Containerisation | Docker |
| Multi-container Orchestration | Docker Compose |
| Reverse Proxy | Nginx |
| In-memory Data Store | Redis |
| CI/CD Pipeline | GitHub Actions |
| Environment Management | `.env` + `os.environ` |
| Production WSGI Server | Gunicorn |
| Automated Testing | Pytest + Flake8 |
| Security Scanning | pip-audit |
| Structured Logging | Python `logging` module (stdout) |

---

## Architecture

All services run within an isolated Docker Compose network. Nginx acts as the sole public-facing entry point and proxies requests internally to the Flask application, which communicates with Redis for persistent state.

```
                    ┌─────────────────────────────────────────┐
                    │         Docker Compose Network          │
                    │                                         │
 Browser ──────────▶│  Nginx (port 80)                        │
 http://127.0.0.1   │       │  reverse proxy                  │
                    │       ▼                                 │
                    │  Flask App (port 5000)                  │
                    │       │  Gunicorn, 2 workers            │
                    │       ▼                                 │
                    │  Redis (port 6379)                      │
                    │       visit counter + cache             │
                    └─────────────────────────────────────────┘
```

**CI/CD Pipeline (GitHub Actions):**

```
git push ──▶ Run Tests (Pytest + Flake8) ──▶ Build Docker Image (SHA tag)
         └──▶ Security Scan (pip-audit CVE check)
```

---

## Repository Structure

```
devops-flask-app/
│
├── app/
│   ├── app.py              # Flask application entry point
│   ├── requirements.txt    # Python dependency manifest
│   ├── tests.py            # Pytest test suite
│   ├── Dockerfile          # Application container definition
│   └── templates/
│       └── index.html      # Web interface template
│
├── nginx/
│   └── nginx.conf          # Reverse proxy configuration
│
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions pipeline definition
│
├── docker-compose.yml      # Multi-container orchestration manifest
├── .env                    # Runtime environment variables (not committed)
└── README.md
```

---

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git

### Running Locally

```bash
# Clone the repository
git clone https://github.com/ParmeetBhamrah/devops-flask-app.git
cd devops-flask-app

# Initialise environment configuration
cp .env.example .env

# Build and start all services
docker compose up --build

# Access the application
open http://127.0.0.1
```

### API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Home page; increments and displays Redis visit counter |
| `/health` | `GET` | Health check returning application and Redis status |
| `/reset` | `GET` | Resets the visit counter to zero |
| `/nginx-health` | `GET` | Confirms Nginx reverse proxy availability |

---

## Operational Reference

```bash
# Start services in detached mode
docker compose up -d

# Stream logs across all services
docker compose logs -f

# Stream logs for a specific service
docker compose logs -f flask-app

# Stop all running services
docker compose down

# Stop services and remove volumes (resets Redis state)
docker compose down -v

# List running containers and their status
docker compose ps

# Rebuild images following source changes
docker compose up --build
```

---

## CI/CD Pipeline

Every push to the `main` branch triggers the following automated workflow:

```
push to main
     │
     ├──▶ Test Stage
     │       ├── Pytest (unit + integration tests)
     │       ├── Flake8 (PEP 8 lint enforcement)
     │       └──▶ Build Stage (on test success)
     │               └── Docker image built and tagged with Git commit SHA
     │
     └──▶ Security Stage (runs in parallel)
             └── pip-audit (CVE vulnerability scan)
```

Pipeline configuration is defined in `.github/workflows/ci.yml`.

---

## DevOps Principles Applied

**Separation of Concerns**
Each container encapsulates a single responsibility. Nginx handles request routing and termination; Flask contains application logic; Redis manages ephemeral state. Services communicate only through defined network interfaces.

**Infrastructure as Code**
The entire runtime environment is declared in version-controlled YAML files. Any authorised contributor can reproduce a fully functional environment with a single command, eliminating environment drift.

**Immutable Artifacts**
Docker images are tagged with the Git commit SHA at build time. Every deployed artefact is traceable to a specific revision of the source code, enabling reliable rollbacks and audit trails.

**Externalised Configuration**
No credentials or environment-specific values are hardcoded. All configuration is injected at runtime via environment variables, in accordance with the twelve-factor application methodology.

**Standardised Health Checks**
The `/health` endpoint follows the health check contract expected by orchestrators such as Kubernetes and cloud load balancers, returning structured status information for both the application and its dependencies.

**Disposable Infrastructure**
Containers are treated as ephemeral units. The `restart: unless-stopped` policy ensures automatic recovery from unexpected failures without manual intervention.

---

## Author

**Parmeet Bhamrah** — [github.com/ParmeetBhamrah](https://github.com/ParmeetBhamrah)