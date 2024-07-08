# Advaced RoboCup@Home

This repo is under working, documentation will be completed step by step

This repo hosts the codebase for Advanced RoboCup@Home course at ICS, TUM.

Supervisor: Fengyi Wang

Developers: Xuhao Jin, Runcong Wang, Yueyang Zhang

## Prerequest

### nvidia-container-toolkit

This project contains various machine learning models, which are containerized in devcontainers in order to avoid any conflict of dependencies. To run them, you have to have `nvidia-container-toolkit` installed.

Install [nvidia-container-toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

Ckeck the installation by running a simple container:

```bash
docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
```

If it works, skip to the configuration of [Contact Graspnet](#contact-graspnet)

#### Troubleshooting

If the following error code is encountered:

```bash
Failed to initialize NVML: Unknown Error
```

try to run the simple container again with remapped device:

```bash
docker run --rm --gpus all --device /dev/nvidia0:/dev/nvidia0 \
  --device /dev/nvidiactl:/dev/nvidiactl \
  --device /dev/nvidia-uvm:/dev/nvidia-uvm \
  --device /dev/nvidia-uvm-tools:/dev/nvidia-uvm-tools \
  ubuntu nvidia-smi
```

If it works, you just need to enable cgroups to manage the process. To do so, access `nvidia_container_runtime` configuration file with any editor as root, for example:

```bash
sudo vim /etc/nvidia-container-runtime/config.toml
```

Locate the line:

```toml
no-cgroups = true
```

set it to false. Then, run the container once again without device remapping, see if the output is correct.

If the error persists, it could be the case that the container can't establish any connection to the GPUs, consult this [issue](https://github.com/NVIDIA/nvidia-docker/issues/1730) in official repo for a self examination.

### Remote Development extension for VSCode

To run the models in devcontainers, you have to download `remote development` extension in VSCode.

## HSRB Configuration
