# Use a lightweight Ubuntu base image
FROM ubuntu:trusty

# Prevent interactive prompts
ARG DEBIAN_FRONTEND=noninteractive

# Install required networking tools
RUN apt-get update && apt-get install -y \
    iw wireless-tools ethtool iproute2 net-tools && \
    apt-get clean

# Default command
CMD ["/bin/bash"]
