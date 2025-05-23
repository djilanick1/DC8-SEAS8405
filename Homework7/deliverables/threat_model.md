# Dockerized Flask App Threat Model

## Summary
This document presents a comprehensive security analysis of a Dockerized Flask web application app.py found in the after folder, covering:
- STRIDE Threat Model
- MITRE ATT&CK for Containers Mapping
- NIST 800-53 Control Alignment

---

## STRIDE Threat Model

| Threat      | Description                                                                                       | Example / Endpoint               | Mitigation Recommendation                                          |
|-------------|---------------------------------------------------------------------------------------------------|----------------------------------|--------------------------------------------------------------------|
| Spoofing    | No authentication mechanisms, allowing any requester                                              | `/`, `/ping`, `/calculate`       | Enforce token-based auth (e.g., API keys or JWT)                   |
| Tampering   | Lack of strict validation could allow command injection                                           | `/ping` uses `subprocess`        | Use input validation, restrict shell access                        |
| Repudiation | No audit logging, preventing traceability                                                         | All endpoints                    | Implement request/response logging                                 |
| Info Leak   | Raw ping output may leak internal network data                                                    | `/ping`                          | Limit command output or sanitize responses                         |
| DoS         | No input limits; `subprocess` or `literal_eval` could be abused for resource exhaustion           | `/calculate`, `/ping`            | Implement input limits and rate limiting                           |
| Privilege Escalation | Containers run as root; no seccomp/AppArmor                                              | Docker container config          | Use non-root containers, enable namespace and seccomp              |

---

## MITRE ATT&CK for Containers Mapping

| Technique ID | Technique Name                          | Risk Vector                                 | Mitigation                                 |
|--------------|------------------------------------------|----------------------------------------------|--------------------------------------------|
| T1609        | Container Administration Command         | `subprocess` call to `ping`                 | Input validation, container restrictions   |
| T1610        | Deploy Container                         | Insecure image pull or build                | Use signed base images, CI image scanning  |
| T1611        | Escape to Host                           | Running as root, no seccomp                 | Use unprivileged users, seccomp profiles   |
| T1608        | Exploit Public-Facing App                | No auth or rate limiting                    | Add authentication, validation, rate limit |
| T1612        | Modify System Image                      | `ADD` in Dockerfile, no trust               | Use `COPY`, scan and verify images         |
| T1203        | Exploitation for Client Execution        | `literal_eval`, `subprocess` abuse          | Sanitize inputs, safer parsing methods     |

---

## Vulnerability to NIST 800-53 Control Mapping

| Vulnerability                              | Control ID | Control Name                            | Remediation                                                         |
|--------------------------------------------|------------|-----------------------------------------|----------------------------------------------------------------------|
| Lack of authentication                     | AC-3       | Access Enforcement                      | Implement token authentication                                      |
| Use of `subprocess` without validation     | SI-10, CM-7| Input Validation, Least Functionality   | Sanitize input, restrict external commands                          |
| No resource limits                         | SC-5       | Denial of Service Protection            | Apply resource constraints, rate limits                             |
| Running as root                            | CM-6, AC-6 | Least Privilege                         | Run as non-root, drop Linux capabilities                           |
| No container health checks                 | SI-4, AU-12| Monitoring, Audit Logging               | Add health checks, monitor container lifecycle                      |
| Insecure base image                        | SI-2, CM-2 | Flaw Remediation, Baseline Config       | Use secure, minimal, and patched base images                        |
| No audit trail                             | AU-2, AU-12| Audit Events, Logging                   | Enable structured logs for API and container events                 |
| Service binds to 0.0.0.0                   | SC-7       | Boundary Protection                     | Bind only to needed interfaces (e.g., 127.0.0.1)                    |

---

## Summary of Remediation Actions

- Replace `subprocess` with backend service proxy or tightly validated shell call
- Use `ast.literal_eval` securely and limit input length
- Run Docker containers as **non-root**
- Set Docker memory/CPU/PID limits via `docker-compose.yml`
- Use base image like `python:3.13-alpine` (0 CVEs)
- Add `HEALTHCHECK` in Dockerfiles
- Apply seccomp profiles and AppArmor where possible
- Bind services only to `127.0.0.1` unless explicitly exposed
- Enable structured logging and rate limiting middleware
