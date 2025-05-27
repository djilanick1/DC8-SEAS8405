# STRIDE Threat Model: Log4Shell Exploitation

| STRIDE | Threat Description | Example | Mitigation |
|--------|--------------------|---------|------------|
| Spoofing | Attacker mimics user | Sends malicious input to /log | Validate and sanitize input |
| Tampering | Modify logs/input | Exploit modifies server logs | Use secure logging practices |
| Repudiation | Deny actions | No logs of attacker input | Enable audit logging |
| Info Disclosure | Sensitive info logged | Log exposes headers/tokens | Limit log details |
| DoS | App crashes on exploit | Repeated `${jndi:` payloads | Input filters, resource limits |
| Elevation | Code execution via JNDI | Remote class loading | Patch log4j, block JNDI |
