#!/usr/bin/env bash

<<comment
script needs to be run from REPOROOT or git TOPDIR [however you call it or define it]
use clean_all_podman.sh to clean everything podman related
comment

# 1. Build the coverage container image
echo "Building coverage image..."
podman build -t coverage:latest -f ./containerfiles/coverage .
if [ $? -ne 0 ]; then
    echo "Coverage build failed!"
    exit 1
fi

# 2. Build the risk-auth-service container image
echo "Building risk-auth-service image..."
podman build -t risk-auth-service:latest -f ./containerfiles/risk-auth-service .
if [ $? -ne 0 ]; then
    echo "Risk-auth-service build failed!"
    exit 1
fi

# 3. Run the coverage image to collect test coverage
echo "Running coverage tests..."
podman run --rm --name coverage coverage:latest
if [ $? -ne 0 ]; then
    echo "Coverage run failed!"
    exit 1
fi

# 4. Run the risk-auth-service app
echo "Running risk-auth-service..."
podman run -d --rm -p 8000:8000 --name risk-auth-service risk-auth-service:latest
if [ $? -ne 0 ]; then
    echo "Failed to start risk-auth-service!"
    exit 1
fi

echo "Adding 5 sec of sleep to give podman some time to start risk-auth-service" && sleep 5

# 5. Run post_logs.sh script to post logs to the app
echo "Running post_logs.sh..."
./tests/post_logs.sh
if [ $? -ne 0 ]; then
    echo "Failed to post logs!"
    exit 1
fi

# 5.1 Let's put one ugly echo since we are not using printf; too late now
echo ""

# 6. Run podman logs to see if app is running fine
echo "Running podman logs risk-auth-service to see if app is running"
podman logs risk-auth-service

# 7. Open the web browser to the logs page
echo "Opening browser at http://0.0.0.0:8000/logs..."
# Adjust the following line based on your system. On Linux systems, `xdg-open` is common.
xdg-open "http://0.0.0.0:8000/logs" || open "http://0.0.0.0:8000/logs" || echo "Could not open the browser automatically. Please visit http://0.0.0.0:8000/logs."

# End of script
echo "Process completed!"
