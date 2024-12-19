## some helper commands for running tests

### running pytest only

podman build -t pytest -f containerfiles/pytest .

podman run -it --rm --name pytest pytest:latest

### running pytest and coverage

podman build -t coverage -f containerfiles/coverage .

podman run -it --rm --name coverage coverage:latest