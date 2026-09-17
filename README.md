# AWS Cloud Security Monitoring & Automated Threat Detection Engine

A serverless security telemetry and threat detection laboratory deployed on AWS using SAM, Python, API Gateway, and Amazon Cognito. This project demonstrates Zero Trust API authorization, real-time threat logging, and incident response monitoring within a cloud environment.

---

## 🏗️ Architecture Overview

The system establishes a secure API gateway boundary backed by identity verification, automated logging, and encrypted storage:

* **Authentication & Identity Control:** Amazon Cognito User Pool and App Client issuing JWT tokens with enforced password policies.
* **API Security Boundary:** Amazon API Gateway enforcing JWT Cognito Authorizer checks across all protected endpoints.
* **Compute & Logic:** AWS Lambda (Python 3.11) executing under least-privilege IAM roles (`LabRole`).
* **Data Protection:** Amazon S3 bucket enforced with AES-256 server-side encryption and strict TLS transport policies (`aws:SecureTransport: false` denial).
* **Threat Telemetry & Auditing:** Real-time AWS CloudWatch Log Streams tracking authorization failures (401/403) and valid execution traces.

```
[ Client / Attacker ]
│
▼
[ Amazon API Gateway ] ◄─── (JWT Authorizer via Amazon Cognito)
│
┌────┴────────────────────────┐
│                             │
(401/403 Rejected)       (200 Authorized)
│                             │
▼                             ▼
[ CloudWatch Logs ]       [ AWS Lambda Engine ] ──► [ Encrypted S3 ]
```

---

## 📂 Repository Structure

```text
aws-cloud-sec-monitoring/
├── architecture/
│   ├── cloudwatch-telemetry.png    # Verified CloudWatch execution log stream trace
│   └── lambda-success-test.png      # 200 OK unit test verification banner
├── docs/                            # Security architecture documentation
├── iac/
│   └── template.yaml               # AWS SAM Infrastructure-as-Code
├── src/
│   ├── app.py                      # Core API handler & claim extractor
│   └── secops_handler.py           # Remediation logic
├── tests/
│   └── attack_simulation.py        # Automated Red Team threat test suite
└── README.md
```

---

## 🧪 Threat Simulation Suite

The repository includes an automated attack simulation script (`tests/attack_simulation.py`) that tests the API security posture against common threat vectors:

* **Unauthenticated Scanning:** Sends raw HTTP requests without Authorization headers (Expected: 401 Unauthorized).
* **Token Tampering:** Injects malformed/fake Bearer JWT tokens into request headers (Expected: 401 Unauthorized).
* **Reconnaissance & Path Enumeration:** Probes non-existent/protected endpoints (`/admin`, `/config`, `/env`, `/v1/keys`) (Expected: 403 Forbidden).

### Verified Simulation Output

```text
=== STARTING CLOUD THREAT SIMULATION ===

[+] Executing Test 1: Unauthenticated Endpoint Scan
    Response Status: 401 (Expected: 401 Unauthorized)

[+] Executing Test 2: Tampered Bearer Token Injection
    Response Status: 401 (Expected: 401 Unauthorized)

[+] Executing Test 3: Reconnaissance & Path Enumeration
    Scanning /admin -> Status: 403
    Scanning /config -> Status: 403
    Scanning /env -> Status: 403
    Scanning /v1/keys -> Status: 403

=== THREAT SIMULATION COMPLETE ===
```

---

## 🚀 Deployment Instructions

### Prerequisites

* AWS CLI configured with valid credentials
* AWS SAM CLI installed
* Python 3.11+

### 1. Build & Deploy Infrastructure

```bash
# Validate template syntax
sam validate -t iac/template.yaml

# Build SAM application package
sam build -t iac/template.yaml

# Deploy stack
sam deploy
```

### 2. Execute Threat Simulation

```bash
# Install test suite dependencies
pip install requests

# Execute simulation against live API Gateway endpoint
python tests/attack_simulation.py "https://<YOUR-API-ID>.execute-api.us-east-1.amazonaws.com/Prod/data"
```

---

## 📊 Verification & Telemetry Proofs

* **CloudWatch Telemetry Logs:** `architecture/cloudwatch-telemetry.png`
* **Lambda Handler Success Result:** `architecture/lambda-success-test.png`
