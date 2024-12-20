## building and running the app inside a container

```bash
podman build -t risk-auth-service -f containerfiles/risk-auth-service .
podman run -it --rm -p 8000:8000 risk-auth-service:latest
```

## some helper commands for running tests

### running pytest only

```bash
podman build -t pytest -f containerfiles/pytest .
podman run -it --rm --name pytest pytest:latest
```

### running pytest and coverage

```bash
podman build -t coverage -f containerfiles/coverage .
podman run -it --rm --name coverage coverage:latest
```