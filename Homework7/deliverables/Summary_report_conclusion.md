## Summary Report

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
