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

  Test the API with and without a valid token to ensure access controls are enforced




## Part 2: Security Analysis and Best Practices (Write-up)

1. **Threat Modeling:**

2. **Mitigation Strategies:**
  

