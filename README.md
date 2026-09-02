# SysOps CLI Toolkit

[![Enterprise CI Pipeline](https://github.com/nishantParmar11-techsolutions/-sysops-cli-toolkit-/actions/workflows/ci.yml/badge.svg)](https://github.com/nishantParmar11-techsolutions/-sysops-cli-toolkit-/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Typer](https://img.shields.io/badge/Typer-0.12.3-brightgreen.svg)](https://typer.tiangolo.com/)
[![Security: Bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade command-line interface (CLI) engineered with Typer and Rich for infrastructure monitoring, remote webhook dispatching, microservice health audits, and real-time terminal telemetry.

---

## 🏛️ Architectural Overview

```
[ Operator / CLI Command ]
            │
            ▼
  [ Typer CLI Engine ] ─── (Click 8.1.x Core)
            │
     ┌──────┴─────────────────────────┐
     ▼                                ▼
[ Health Audits & Pings ]    [ Telemetry & Inspection ]
(Microservices & Webhooks)    (System Resources & Specs)
     │                                │
     └──────────────┬─────────────────┘
                    ▼
         [ Rich Terminal UI Engine ]
       (Color-coded Panels & Tables)
```

---

## ⚙️ Architecture & Tech Stack

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **CLI Framework** | Typer 0.12.3, Click < 8.2 | Type-hinted subcommands, options, and auto-generated help manuals |
| **Terminal UX** | Rich | Styled tables, layout panels, progress indicators, and syntax highlights |
| **Networking** | Requests, HTTPX | Synchronous and asynchronous ping probes and webhook dispatchers |
| **AppSec Verification** | Bandit AST Scanner | Automated AST scanning for shell injections and security vulnerabilities |
| **CI/CD Automation** | GitHub Actions 4-Stage DAG | Linting, Python 3.10–3.12 matrix, AppSec audit, and Wheel packaging |

---

## 🚀 Key Features

* **Interactive Terminal Telemetry:** Generates formatted system diagnostic tables, CPU/memory summaries, and microservice status reports directly in the terminal.
* **Automated Webhook Health Probes:** Dispatches latency tests and ping validations against internal and external endpoints.
* **Hardened Dependency Matrix:** Pinned compatibility between Typer and Click ensures CLI rendering without runtime metavar crashes.
* **Packaging & Wheel Validation:** CI guarantees package distribution readiness via Python `build` wheel checks and container sanity runs.

---

## 📁 Repository Structure

```text
├── .github/workflows/
│   └── ci.yml             # 4-Stage Enterprise DAG CI/CD Pipeline
├── main.py                # Main executable CLI entrypoint and commands
├── requirements.txt       # Production dependencies
├── Dockerfile             # Containerized CLI runtime
├── Makefile               # Development automation workflows
└── README.md              # Technical specifications & usage manual
```

---

## 🛠️ Quick Start

### 1. Installation
```bash
git clone [https://github.com/nishantParmar11-techsolutions/-sysops-cli-toolkit-.git](https://github.com/nishantParmar11-techsolutions/-sysops-cli-toolkit-.git)
cd -sysops-cli-toolkit-
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. View Available Commands
```bash
python main.py --help
```

### 3. Run System Health Audit
```bash
python main.py health
```

