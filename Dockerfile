# Use a lightweight Ubuntu 20.04 base image
FROM ubuntu:20.04

# Prevent interactive prompts
ARG DEBIAN_FRONTEND=noninteractive

# Install required networking tools and iperf3
RUN apt-get update && apt-get install -y \
    iw wireless-tools ethtool iproute2 net-tools iperf3 && \
    apt-get clean

# Default command
CMD ["/bin/bash"]
