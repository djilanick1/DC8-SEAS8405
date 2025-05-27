# Incident Response: Log4Shell

## Detect
- Check container logs for `${jndi:`
- Identify external connections (e.g. to LDAP)

## Contain
- Stop container: `docker-compose down`

## Eradicate
- Confirm exploit vectors patched (log4j >= 2.17.0)
- Ensure no running rogue processes

## Recover
- Deploy updated app with input validation
- Test benign requests

## Notes
This aligns with MITRE REACT: Detect, Contain, Eradicate, Recover
```
