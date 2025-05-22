# Homework7: Securing Containerized Microservices

---

## Introduction

The purpose of this assignment is to step into the cybersecurity architects shoes and get some hands on experience securing a Python web app that has some vulnerabilities. To proceed, we'll analyze the system, pinpoint its security weaknesses, and then fix them using secure coding practices, container hardening techniques, and thoughtful architectural decisions. As we go, we'll map out potential threats, design a more secure setup, and make sure our fixes actually work. We will also include a screen recording showing our process along with the below brief technical report. 

---

## Part 1: Environment Setup

1. **Understand the Application:**
   Manually reviewing the app.py flask code reveals these vulnerabilities:

| **Vunerabilities**              | **Code where to find**                                  | **Risk**                                                          |
|---------------------------------|---------------------------------------------------------|-------------------------------------------------------------------|
| Hard coded credentials          |    PASSWORD = "supersecretpassword"                     | Risk: Credential leakage, reuse across environments               |
| Command Injection               | subprocess.check_output(f"ping -c 1 {ip}", shell=True)  | Rosk: Unvalidated user input can execute arbitrary system commands|
| Insecure eval ()                | result = eval(expression)                               | Risk: Remote Code Execution (RCE)                                 |


2. **Run the Environment:**
   - Use `make start` to launch the application: to do this, i had to install Docker Compose and restart the docker daemon
   - Test the endpoints: `/`, `/ping?ip=8.8.8.8`, and `/calculate?expr=2+3`.
     ![image](https://github.com/user-attachments/assets/f29e71e3-aa4a-41f4-9b20-3d49623cf68f)

When testing endpoint /calculate?expr=2+3, i had a 500 Internal Server Error; this means the Flask app crashed while trying to process the request to /calculate?expr=2+3. This is due to the fact that passing 2+3 in the query string is one thing, but the + is being interpreted as a space, not as the + character. In URLs, + is URL-encoded as %2B. To correct this, i ran $curl "http://localhost:15000/calculate?expr=2%2B3" result 5


3. **Initial Scanning:**
   - Run `make check`, `make scan`, and `make host-security`. To perform thes command, installation of docker-scout was needed, follow by the creation of a new docker ID, with EC2 device confirmation on Docker Hub. I have also update the Makefile, changing docker scout to docker-scout.
   - Vulnerabilities and misconfigurations: the below was extractd from the files before_scan.txt and before_host-security.txt

---

## 1.3.1. Host & Container Misconfigurations (Docker Bench)

### High-Priority Issues Identified:

| **ID**     | **Description**                                                                 |
|------------|----------------------------------------------------------------------------------|
| 1.1        | No separate partition for containers                                             |
| 1.5        | Auditing for Docker daemon is not configured                                     |
| 2.1        | Network traffic is not restricted between containers on default bridge           |
| 2.8        | User namespace support is disabled                                               |
| 2.11       | No authorization configured for Docker client commands                           |
| 2.12       | Centralized and remote logging not configured                                    |
| 2.14–2.15  | Live restore and userland proxy not configured properly                          |
| 2.18       | Containers not restricted from acquiring new privileges                          |
| 3.15       | Docker socket has incorrect ownership (`/var/run/docker.sock`)                   |
| 4.1        | Containers running as root user (`before-db-1`)                                  |
| 4.5        | Docker Content Trust not enabled                                                 |
| 4.6        | No healthcheck instructions for multiple images                                  |
| 5.2        | SELinux not enabled or configured for containers                                 |
| 5.10–5.14  | Missing CPU/memory limits, PID cgroup limits, exposed ports, and read/write FS   |
| 5.25–5.28  | Containers not restricted from acquiring additional privileges                   |

---

## 1.3.2. Docker Image Vulnerabilities (Docker Scout)

### Image Scanned: `mywebapp:latest`  
**Base image:** `python:3.9-alpine`

###  Vulnerabilities Found:
- **High:** 3
- **Medium:** 1     

## Part 2: Secure the App and Container

1. **Code Remediation:**
   - Refactor `app.py` to:
     - Eliminate hardcoded passwords.
     - Replace `eval()` with `ast.literal_eval`.
     - Validate all inputs.
     - Restrict Flask to localhost.

2. **Docker Hardening:**
   - Use a minimal base image.
   - Ensure the app runs as a non-root user.
   - Add a `HEALTHCHECK` directive.
   - Implement multi-stage builds if possible.

3. **docker-compose.yml Improvements:**
   - Add `read_only`, `security_opt`, `mem_limit`, and `pids_limit`.
   - Restrict port exposure to `127.0.0.1`.
   - Use `.env` files for secret handling.

## Part 3: Threat Modeling

1. **Threat Model Documentation:**
   - Perform STRIDE analysis on the app.
   - Use MITRE ATT&CK for Containers to identify relevant techniques.
   - Create a table mapping vulnerabilities to controls (e.g., NIST 800-53).

2. **Save and Submit:**
   - Write results in `deliverables/threat_model.md`.

## Part 4: Security Architecture Implementation

1. **Architecture Design:**
   - Draft a diagram showing the hardened app infrastructure (use tools like Lucidchart or draw.io).
   - Save as `deliverables/architecture_diagram.png`.

2. **Auto-Hardening Script:**
   - Write a Python script (`docker_security_fixes.py`) to:
     - Update `daemon.json` with hardening flags.
     - Inject `USER`, `HEALTHCHECK`, and limits into Dockerfile and Compose.

## Part 5: Recording the Simulation

1. **Record Your Screen:**
   - Use OBS or QuickTime.
   - Include:
     - Initial scan and vulnerable app behavior.
     - Code and config remediation.
     - Threat model explanation.
     - Re-scans showing reduced vulnerabilities.

2. **Add Commentary:**
   - Use voiceover or annotations.
   - Describe what you are doing and why.

3. **Export:**
   - Save as MP4.

## Part 6: Summary Report

Write `deliverables/summary_report.md` (1–2 pages) including:
- Steps taken.
- Vulnerabilities found and fixed.
- Architecture and how it improves security.
- Reflection on lessons learned.

---

