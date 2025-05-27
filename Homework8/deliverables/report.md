# Homework8: Implementing a Secure IAM Architecture

---

## Introduction

The purpose of this assignment is to design and implement a secure Identity and Access Management (IAM) architecture using Keycloak as the identity provider and a Flask application as a protected microservice. We will also configure OAuth 2.0 and OpenID Connect (OIDC) to secure the Flask API, ensuring that only authenticated and authorized users can access protected resources. Additionally, we will analyze potential security risks and apply best practices to mitigate them.

---

## Part 1: Environment Setup

### 1. **Setup Keycloack:**
To proceed, we have to open ports 8080 and 8180 on the inbound rules of the security group of our Bastion EC2 instance. I then download Keyclock in my EC2, set the admin credential for the CLI /opt/keycloak/bin/kcadm.sh config credentials \
  --server http://localhost:8180 \
  --realm master \
  --user admin \
  --password admin

  I then started the Keycload in development environment, opening a second termianl using this: ./kc.sh start-dev --http-host=0.0.0.0 --hostname-strict=false --https-protocols=false

  Once loggged into the web console, i tried to export the realm-master in the jason format, however it was giving me a partial download and i finally did it via the CLI:
  cd /opt/keycloak/bin

./kc.sh export \
  --dir /opt/keycloak/data/export \
  --realm your-realm-name \
  --users=realm_file

   
 ![image](https://github.com/user-attachments/assets/72709753-54d7-4252-b3ce-864f65aced34)
                      |


### 2. **Protect the Flask API**
The token validation is implemented with this function: token_required(f); to ensure the API correctly handles authenticated and unauthenticated requests, there are clear routes for public and protected access


### 3. **Test the setup:**
  Although i did everything manually, i loaded a scripts to automate the process in Homework8/keycloack

  Test the API with and without a valid token to ensure access controls are enforced; we can see on this image that testing the /public returens 200 but testing the /protected returns 404, 401.

  ![image](https://github.com/user-attachments/assets/f49ad470-340d-4ed0-9f29-d9f5786a159c)



## Part 2: Security Analysis and Best Practices (Write-up)

1. **Threat Modeling:**

***Methodology***: STRIDE  
***Architecture***: Keycloak (OIDC) + Flask API + Docker Compose

---

##STRIDE Breakdown

| STRIDE Category        | Threat                         | Description | Example in System | Mitigation |
|------------------------|--------------------------------|-------------|--------------------|------------|
| **S: Spoofing**        | Identity Forgery               | Attacker impersonates a legitimate user or service. | Forged JWT sent to Flask API. | Verify JWT signature with Keycloak public keys and validate `aud` & `iss` claims. |
| **T: Tampering**       | Token/Data Manipulation        | Tokens or requests are altered in transit or memory. | JWT contents altered client-side. | Use RS256-signed JWTs; never trust client-side claims. |
| **R: Repudiation**     | Action Denial                  | Lack of audit logs prevents accountability. | No logs for API access or token use. | Enable logging in Flask and event auditing in Keycloak. |
| **I: Information Disclosure** | Data/Token Leak         | Sensitive information exposed via logs or responses. | Access token logged by Flask. | Avoid logging Authorization headers or JWTs. |
| **D: Denial of Service** | Resource Exhaustion          | Abusing token endpoint or API to cause crash. | Multiple invalid token requests to Flask. | Rate limit endpoints; use fail2ban or circuit breakers. |
| **E: Elevation of Privilege** | Privilege Escalation     | Misconfigured roles allow over-permissioned access. | `flask-client` can modify Keycloak. | Assign minimal scopes/roles; enforce role checks in Flask. |

---

### Key Components at Risk

| Component      | Risk Vector                               | Mitigation Strategy |
|----------------|--------------------------------------------|---------------------|
| Keycloak       | Brute-force login or exposed endpoints     | Use CAPTCHA, lockout policy, secure admin console |
| Flask API      | No RBAC enforcement                        | Parse roles from JWT (`realm_access.roles`) |
| JWT Storage    | Insecure session/token handling            | Use `HttpOnly` cookies or Authorization headers |
| Docker Config  | Containers run as root or leak secrets     | Use `USER`, `.env`, and `secrets:` properly |
| Network        | Token interception                         | Enforce HTTPS via NGINX or ALB+ACM |

2. **Mitigation Strategies:**
- Use **short-lived access tokens** and **refresh tokens** with revocation.
- Enable **audit logging** in both Keycloak and Flask.
- Implement **rate limiting** and abuse protection on Flask endpoints.
- Use **non-root containers**, restrict network bindings (127.0.0.1).
- Deploy behind **HTTPS** using NGINX reverse proxy or AWS ALB with ACM.
- Apply **role-based access control** based on scopes defined in Keycloak.
  

