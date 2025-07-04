# Homework7: Securing Containerized Microservices

---

## Introduction

The purpose of this assignment is to step into the cybersecurity architects shoes and get some hands on experience securing a Python web app that has some vulnerabilities. To proceed, we'll analyze the system, pinpoint its security weaknesses, and then fix them using secure coding practices, container hardening techniques, and thoughtful architectural decisions. As we go, we'll map out potential threats, design a more secure setup, and make sure our fixes actually work. We will also include a screen recording showing our process along with the below brief technical report. 

---

## Part 1: Environment Setup

### 1. **Understand the Application:**
   Manually reviewing the app.py flask code reveals these vulnerabilities:

| **Vunerabilities**              | **Code where to find**                                  | **Risk**                                                          |
|---------------------------------|---------------------------------------------------------|-------------------------------------------------------------------|
| Hard coded credentials          |    PASSWORD = "supersecretpassword"                     | Risk: Credential leakage, reuse across environments               |
| Command Injection               | subprocess.check_output(f"ping -c 1 {ip}", shell=True)  | Rosk: Unvalidated user input can execute arbitrary system commands|
| Insecure eval ()                | result = eval(expression)                               | Risk: Remote Code Execution (RCE)                                 |


### 2. **Run the Environment:**
   - Use `make start` to launch the application: to do this, i had to install Docker Compose and restart the docker daemon
   - Test the endpoints: `/`, `/ping?ip=8.8.8.8`, and `/calculate?expr=2+3`.
     ![image](https://github.com/user-attachments/assets/f29e71e3-aa4a-41f4-9b20-3d49623cf68f)

When testing endpoint /calculate?expr=2+3, i had a 500 Internal Server Error; this means the Flask app crashed while trying to process the request to /calculate?expr=2+3. This is due to the fact that passing 2+3 in the query string is one thing, but the + is being interpreted as a space, not as the + character. In URLs, + is URL-encoded as %2B. To correct this, i ran $curl "http://localhost:15000/calculate?expr=2%2B3" result 5


### 3. **Initial Scanning:**
   - Run `make check`, `make scan`, and `make host-security`. To perform thes command, installation of docker-scout was needed, follow by the creation of a new docker ID, with EC2 device confirmation on Docker Hub. I have also update the Makefile, changing docker scout to docker-scout.
   - Vulnerabilities and misconfigurations: the below was extractd from the files before_scan.txt and before_host-security.txt


  #### 1.3.1. Host & Container Misconfigurations (Docker Bench)

###### High-Priority Issues Identified:

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


#### 1.3.2. Docker Image Vulnerabilities (Docker Scout)

###### Image Scanned: `mywebapp:latest`  
**Base image:** `python:3.9-alpine`

#####  Vulnerabilities Found:
- **High:** 3
- **Medium:** 1     

## Part 2: Secure the App and Container

1. **Code Remediation:**
The available app.py code in the after folder has the required securities implemented:
- the use of os.environ.get('PASSWORD', 'default_password') instead of a hardcoded string; this can also be overridden with an environment variable.
- ast.literal_eval() is used in /calculate, which is safe for basic math expressions.
- input validation: / validates with .isalnum() and /ping uses ipaddress.ip_address() to reject invalid IPs.
- App binds to 127.0.0.1 via app.run(host='127.0.0.1', port=5000) instead of 0.0.0.0

2. **Docker Hardening:**
   The modified Dockerfile in the after folder:
   - Uses python:3.13-alpine, which is a minimal Alpine-based image; ensure the app runs as a non-root user.
   - Adds appuser with adduser -D and switches with USER appuser
   - Implements a HEALTHCHECK using curl -f http://localhost:5000/
   - Implements multi-stage builds help reduce image size further by separating build and runtime layers.

3. **docker-compose.yml Improvements:**
The modified docker-compose.yaml in the after folder: 
   - Adds `read_only`, `security_opt`, `mem_limit`, and `pids_limit`.
   - Restricts port exposure to `127.0.0.1`.
   - Uses `.env` files for secret handling; under db service with env_file
To test this modified files, i had to stop the containers currently running from the before folder, prune them to delete them and test the newly secured app; i had to do this because i was having this error: failed to bind host port for 127.0.0.1:15000:172.21.0.2:5000/tcp: address already in use
Also i ran into an issue where after running the make dbuild, no containers (web, db) was created; i checked the logs (docker logs after-web-1; docker logs after-db-1); to fix the app i add to install the pyhton virtual environment and to fix the db, i add simpleeval to requirements.txt, modify the docker file and docker-compose aswell (see in the after folder).
After analyzing the vulnerability scan result, only 3 HIGH remain: 3 High, 1 Medium CVE in python:3.9-alpine base image; the easy fix is to use the base alpine base image with no HIGH vulnerabilities: tag 3.13 and add it into the Dockerfile: FROM python:3.13-alpine

## Part 3: Threat Modeling

Check results in deliverables/threat_model.md.

## Part 4: Security Architecture Implementation

1. **Architecture Design:**
   Lucidchart was used to make the diagram. available as deliverables/architecture_diagram.png

2. **Auto-Hardening Script:**
 The script does fully meet the hardening criteria; available in deliverables folder.

## Part 5: Recording the Simulation
Video available on youtube here https://www.youtube.com/watch?v=6DgtkeYuCX4

## Part 6: Summary Report

## Steps Taken
We took a close look at the security of a Flask application that runs in Docker. This involved a few key steps:
- We thought about potential threats using something called STRIDE.
- We mapped those threats to real-world attack techniques using the MITRE ATT&CK framework.
- We checked how well the application lined up with security best practices from NIST 800-53.
- We also used automated tools like Bandit and Docker Scout to scan the code and container setup for weaknesses.

## Vulnerabilities Found & Fixed
We found a few important security issues and got them sorted out. These included:
- The application was using subprocess, which can sometimes be risky.
- The containers were running with root privileges, which gives them too much power.
- There wasn't a way to easily check if the containers were healthy (HEALTHCHECK was missing).
- There weren't any limits on the resources the containers could use.
We fixed these by adding security configurations directly into the Docker setup files (daemon.json, Dockerfiles, and docker-compose.yml).

## Architecture & Improvements
The improved setup now has:
- Containers that run as non-root users, which is much safer.
- Limits on how many resources the containers can use.
- More secure ways the application communicates.
- Health checks so we can easily see if everything is running okay.
We also suggested adding a rate-limiting system to the API gateway and setting up monitoring for extra security.

## Lessons Learned
This process highlighted that security needs to be a part of both the application's code and the infrastructure it runs on. Even small things, like allowing unrestricted access to the system's shell or exposing ports publicly, can create big security problems. We also learned that thinking about potential threats beforehand and using automation are really important for making sure things stay secure over time.


---

