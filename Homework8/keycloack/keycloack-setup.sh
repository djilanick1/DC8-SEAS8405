# to be run once Keycloak starts
#!/bin/bash

# Wait for Keycloak to become available
until curl -s http://localhost:8080; do
  echo "Waiting for Keycloak..."
  sleep 3
done

echo "Configuring Keycloak..."

docker exec -it $(docker ps -qf "name=keycloak") /opt/keycloak/bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

docker exec -it $(docker ps -qf "name=keycloak") /opt/keycloak/bin/kcadm.sh create realms -s realm=master-realm -s enabled=true

docker exec -it $(docker ps -qf "name=keycloak") /opt/keycloak/bin/kcadm.sh create clients -r master-realm -s clientId=flask-client -s enabled=true -s publicClient=true -s directAccessGrantsEnabled=true -s redirectUris='["*"]'

docker exec -it $(docker ps -qf "name=keycloak") /opt/keycloak/bin/kcadm.sh create users -r master-realm -s username=testuser -s enabled=true

USER_ID=$(docker exec -it $(docker ps -qf "name=keycloak") /opt/keycloak/bin/kcadm.sh get users -r master-realm -q username=testuser --fields id --format csv | tail -n1)

docker exec -it $(docker ps -qf "name=keycloak") /opt/keycloak/bin/kcadm.sh set-password -r master-realm --userid $USER_ID --new-password testpassword

echo "Exporting realm configuration..."
docker exec -it $(docker ps -qf "name=keycloak") /opt/keycloak/bin/kc.sh export --dir /opt/keycloak/data/import --realm master-realm --users realm_file
