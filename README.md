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

## Contact GraspNet

Contact GraspNet is developed by NVlabs (see original repo [here](https://github.com/NVlabs/contact_graspnet/tree/main)), which is a general grasp pose generator for parallel jaw gripper.

Clone the forked and modified version of Contact GraspNet with:

```bash
git clone https://github.com/Jonas-Zhang97/contact_graspnet_hoi.git
```

### Configure the Contact GraspNet

Open VSCode, reopen folder in devcontainer. All the dependencies are already installed in the container, so you don't need to create conda environment any more.

If you cloned official version of Contact GraspNet, you will still have to download check points from the [official cloud drive](https://drive.google.com/drive/folders/1tBHKf60K8DLM5arm-Chyf7jxkzOr5zGl), and unzip them in `/contact_graspnet_hoi/checkpoints`. The modified version contains already check points.

Try to inference with example data with:

```bash
python contact_graspnet/inference.py --np_path=test_data/*.npy
```

or alternatively with depth image with a single object:

```bash
python contact_graspnet/inference.py --np_path=depth_image_data/*.npy
```
