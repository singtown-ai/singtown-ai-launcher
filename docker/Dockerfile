FROM debian:bookworm-slim

ENV NVIDIA_CONTAINER_TOOLKIT_VERSION=1.18.0-1
ADD https://nvidia.github.io/libnvidia-container/gpgkey /tmp/gpgkey
ADD https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list /tmp/nvidia-container-toolkit.list
COPY wsl-distribution.conf /etc/wsl-distribution.conf
COPY docker-compose.yml /root/docker-compose.yml

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates podman podman-compose && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends gnupg2 \
  && gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg /tmp/gpgkey \
  && sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' /tmp/nvidia-container-toolkit.list | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
  && apt-get remove -y gnupg2 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
  nvidia-container-toolkit=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
  nvidia-container-toolkit-base=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
  libnvidia-container-tools=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
  libnvidia-container1=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
  && apt-get clean && rm -rf /var/lib/apt/lists/* && rm -f /tmp/*