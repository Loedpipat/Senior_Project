# Use Ubuntu 18.04 base image
FROM ubuntu:18.04

# Prevent interactive prompts
ARG DEBIAN_FRONTEND=noninteractive

# Update package list and install required packages
RUN apt-get update && apt-get install -y \
    iw wireless-tools ethtool iproute2 net-tools iperf3 && \
    apt-get clean

# Default command
CMD ["/bin/bash"]
