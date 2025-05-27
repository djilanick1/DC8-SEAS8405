# MITRE-Based Threat Modeling for Log4Shell

## ATT&CK Matrix: Adversarial Techniques

| Tactic              | Technique (ID)                          | Description                                        | Example                                           | Mitigation Strategy                          |
|---------------------|------------------------------------------|----------------------------------------------------|--------------------------------------------------|----------------------------------------------|
| Initial Access      | Exploit Public-Facing Application (T1190)| Remote code injection via `/log` endpoint          | `${jndi:ldap://...}` payload                     | Patch Log4j, WAF, input sanitization         |
| Execution           | Command and Scripting Interpreter (T1059.001) | Remote class execution via JNDI                  | Malicious Java code loaded                       | Disable JNDI, use latest Log4j                |
| Persistence         | Server Software Component (T1505.003)    | Injects persistent backdoor or cronjob             | Attacker class remains active                    | Use read-only containers, ephemeral infra     |
| Defense Evasion     | Masquerading (T1036)                     | Logs disguised as normal user input                | `${jndi:}` embedded in benign text               | Log filtering, anomaly detection              |
| Privilege Escalation| Exploitation for Privilege Escalation (T1068) | Runs code with root inside container            | Compromised JVM runs as root                     | Drop root, apply container security controls  |
| Credential Access   | Unsecured Credentials (T1552)            | Sensitive data in logs                             | Tokens or headers logged                         | Mask credentials in logs                      |
| Impact              | Service Stop (T1489)                     | App crash from malformed input                     | Log4j exploit shuts down app                     | Input filters, DoS protection                 |

---

## MITRE DEFEND Matrix: Defensive Techniques

| D3FEND Technique (ID)   | Defensive Mechanism                  | Description                                         | Application                                     |
|--------------------------|---------------------------------------|-----------------------------------------------------|------------------------------------------------|
| D3-SI                    | Software Patch                       | Patch vulnerable Log4j libraries                    | Upgrade to Log4j 2.17.0                        |
| D3-IV                    | Input Validation                     | Filter out suspicious user input patterns           | Block `${jndi:...}` in user input              |
| D3-SL                    | Service Log Analysis                 | Detect anomalies in logs                            | Monitor for unusual JNDI payloads              |
| D3-NET                   | Network Segmentation                 | Block exploit reachability to LDAP servers          | Restrict egress from container to host         |
| D3-NSM                   | Network Session Monitoring           | Detect outbound LDAP calls                          | Alert on unusual protocol destinations         |
| D3-RM                    | Runtime Memory Protection            | Block unsafe operations in runtime                  | Use JVM security policies                      |
| D3-UC                    | User Context Isolation               | Restrict service context                            | Use non-root containers, AppArmor/seccomp      |

---

## MITRE RE&CT Matrix: Incident Response Phases

| RE&CT Phase      | Response Action                     | Example Activity                                | Tool/Action                                     |
|------------------|--------------------------------------|--------------------------------------------------|-------------------------------------------------|
| Detect           | Monitor logs for `${jndi:` patterns | Observe suspicious input hitting `/log`         | `docker logs`, Fluentd, ELK                     |
| Contain          | Stop affected services              | Shut down vulnerable container                   | `docker-compose down`                           |
| Eradicate        | Remove vulnerable version           | Rebuild app with patched Log4j                  | Rebuild image using Log4j 2.17.0                |
| Recover          | Validate patched service            | Test benign inputs after redeployment           | `curl -X POST http://localhost:8080/log -d ...` |
| Post-Incident    | Audit and harden future builds      | Add checks to CI/CD, logging, and dependency updates | GitHub Actions, Snyk, Trivy                  |

