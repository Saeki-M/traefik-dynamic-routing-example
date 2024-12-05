from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/traefik-config")
def get_traefik_config():
    config = {
        "http": {
            "routers": {
                # "vm1-agent1": {
                #     "rule": "PathPrefix(`/vm1/agent1`)",
                #     "service": "vm1-agent1-service",
                #     "middlewares": ["strip-vm-agents"],
                # },
                "vm2-agent2": {
                    "rule": "PathPrefix(`/vm2/agent2`)",
                    "service": "vm2-agent2-service",
                    "middlewares": ["strip-vm-agents"],
                },
            },
            "services": {
                "vm1-agent1-service": {
                    "loadBalancer": {"servers": [{"url": "http://backend1"}]}
                },
                "vm2-agent2-service": {
                    "loadBalancer": {"servers": [{"url": "http://backend2"}]}
                },
            },
            "middlewares": {
                "strip-vm-agents": {
                    "stripPrefixRegex": {"regex": ["^/vm[0-9]+/agent[0-9]+"]}
                },
            },
        }
    }
    return JSONResponse(content=config)
