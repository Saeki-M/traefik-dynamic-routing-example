This is a sample repository for running traefik

# Testing dynamic reverse proxy
start docker compose 
```
docker compose up
```

This will start traefik, a fastapi app for providing the routing configuration information, and two dummy backend services.
traefik will request the fastapi app for the configuration file, and it will change the setting dynamically.
First, try accessing http://localhost:8080/vm1/agent1 and http://localhost:8080/vm2/agent2, and confirm you can access the two dummy backends.
Next, comment out the following section in `app/main.py`
```python
"vm1-agent1": {
    "rule": "PathPrefix(`/vm1/agent1`)",
    "service": "vm1-agent1-service",
    "middlewares": ["strip-vm-agents"],
},
```

Fastapi is running on hot reload, so it will update the configuration file it returns.
Traefik polls for the configuration file every 10 seconds, so wait for the configuration to be updated (you should get `fastapi-1   | INFO:     172.26.0.3:53348 - "GET /traefik-config HTTP/1.1" 200 OK` in the logs).
Next, try accessing http://localhost:8080/vm1/agent1 and you should get "404 page not found" which confirms the routing has been dynamically updated.

# Deploying traefik to cloud run
When deploying to cloud run, the following command can be used.
Replace $CONFIG_API_ENDPOINT with the endpoint of the service that returns the configuration file.
```shell
gcloud run deploy traefik-service \
  --image=traefik:3.2.1 \
  --command="traefik" \
  --args="--entryPoints.web.address=:80","--providers.http.endpoint=$CONFIG_API_ENDPOINT","--providers.http.pollInterval=10s" \
  --port=80 \
  --platform=managed \
  --allow-unauthenticated \
  --region=asia-northeast1
```