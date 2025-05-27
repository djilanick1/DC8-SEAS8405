
# MITRE ATT&CK Threat Model: Log4Shell Exploitation

| ATT&CK Tactic         | Technique (ID)                | Threat Description                           | Example                                        | Mitigation Strategy                          |
|------------------------|-------------------------------|-----------------------------------------------|------------------------------------------------|----------------------------------------------|
| Initial Access         | Exploit Public-Facing App (T1190) | Remote exploit of log4j via `/log` endpoint     | `${jndi:ldap://...}` payload                   | Input validation, WAF, patch Log4j           |
| Execution              | Command and Scripting Interpreter (T1059.001) | Execution of Java code through JNDI lookup   | Malicious Java class loaded from attacker LDAP | Disable JNDI, upgrade Log4j to ≥ 2.17.0      |
| Persistence            | Server Software Component (T1505.003) | Insertion of persistent code via exploit     | Backdoor class or cronjob in container         | Container immut



# STRIDE Threat Model: Log4Shell Exploitation

| STRIDE | Threat Description | Example | Mitigation |
|--------|--------------------|---------|------------|
| Spoofing | Attacker mimics user | Sends malicious input to /log | Validate and sanitize input |
| Tampering | Modify logs/input | Exploit modifies server logs | Use secure logging practices |
| Repudiation | Deny actions | No logs of attacker input | Enable audit logging |
| Info Disclosure | Sensitive info logged | Log exposes headers/tokens | Limit log details |
| DoS | App crashes on exploit | Repeated `${jndi:` payloads | Input filters, resource limits |
| Elevation | Code execution via JNDI | Remote class loading | Patch log4j, block JNDI |
