gcloud run deploy traefik-service \
  --image=traefik:3.2.1 \
  --command="traefik" \
  --args="--entryPoints.web.address=:80","--providers.http.endpoint=http://34.84.160.41:80/traefik-config","--providers.http.pollInterval=10s" \
  --port=80 \
  --platform=managed \
  --allow-unauthenticated \
  --region=asia-northeast1
