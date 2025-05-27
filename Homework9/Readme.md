# Week9: Log4Shell Vulnerability Homework

This project demonstrates the exploitation and mitigation of the Log4Shell vulnerability (CVE-2021-44228) using a vulnerable Java Spring Boot application deployed via Docker Compose.

---

## Objectives

- Simulate a real-world Log4Shell exploit scenario
- Apply MITRE ATT&CK, DEFEND, and REACT frameworks
- Harden and redeploy the application using secure coding practices

---

## Project Structure
![image](https://github.com/user-attachments/assets/81ce4a36-e1ec-4d7c-9642-aa2cbb60a93a)


---

## Phases

### Part 1: Exploitation (MITRE ATT&CK)
- Vulnerable version of Log4j 2.14.1 logs unsanitized input.
- Exploit performed using JNDI payload and attacker-controlled LDAP server.

### Part 2: Defense (MITRE DEFEND)
- Log4j upgraded to 2.17.0.
- Input validation implemented to block JNDI patterns.

### Part 3: Response (MITRE REACT)
- Detect: Logs examined for exploit traces
- Contain: Vulnerable container stopped
- Eradicate: Patched container deployed
- Recover: System restored with mitigation verified

---

## Lessons Learned

- Logging libraries must be treated as part of the attack surface.
- Validate all input—even when passed to internal services.
- MITRE frameworks provide a clear guide for security lifecycle management.

---

## Requirements

- Docker & Docker Compose
- Java + Maven (if building manually)
- Python 3 (for attacker LDAP simulation)

---

## References

- [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [MITRE DEFEND](https://defend.mitre.org/)
- [MITRE REACT](https://www.mitre.org/publications/technical-papers/react-a-framework-for-incidence-response)


