# Advaced RoboCup@Home

This repo is under working, documentation will be completed step by step

This repo hosts the codebase for Advanced RoboCup@Home course at ICS, TUM.

Supervisor: Fengyi Wang

Developers: Xuhao Jin, Runcong Wang, Yueyang Zhang

To clone the repo:

```bash
git clone git@github.com:Jonas-Zhang97/TUM-AdvRoboCup.git adv_robocup
```

## Prerequest

### nvidia-container-toolkit

This project contains various machine learning models, which are containerized in devcontainers in order to avoid any conflict of dependencies. To run them, you have to have `nvidia-container-toolkit` installed.

Install [nvidia-container-toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

Ckeck the installation by running a simple container:

```bash
docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
```

### Remote Development extension for VSCode

To run the models in devcontainers, you have to download `remote development` extension in VSCode.

## HSRB Configuration

After the container is built, try some basic command to verify if everything is correct. For example, run

```bash
roscore
```

If nothing is being prompt, consult *Port 11311 Forwarding Error* in [Troubleshooting](#troubleshooting) for a solution.

You can now try to run the hsrb in simulator, for that, enter `sim_mode`:


```bash
sim_mode
```

In `sim_mode`, launch:

```bash
roslaunch hsrb_gazebo_launch hsrb_megaweb2015_world.launch
```

## HSRB ROS Packages

More infomation can be found [here](https://docs.hsr.io/hsrio_manual_en/gitlab/gitlab.html)

Download the codes of hsrb-samples, -moveit and -rosnav, then unzip them into the devcontainer home directory (i.e. `/workspaces/<repo_name>`).

In `hsrb_ws/src`, create symbolic link to the packages:

```bash
ln -s /workspaces/adv_robocup/hsrb_moveit/ _hsrb_moveit && \
ln -s /workspaces/adv_robocup/hsrb_samples/ _hsrb_samples && \
ln -s /workspaces/adv_robocup/hsrb_rosnav/ _hsrb_rosnav
```

## MoveIt

Configure MoveIt. You can skip `moveit_tutorials` and `panda_moveit_config`.

Note: Put every thing in `workspaces/adv_robocup/hsrb_ws/src/moveit_utils`, which is on the `.gitignore` list.

## Build the workspace

To build the workspace, first go to `src/` folder, use `rosdep` to complete the missing dependencies automatically:

```bash
rosdep install -y --from-paths . --ignore-src --rosdistro noetic
```

Then go to `hsrb_ws/`:

```bash
sudo catkin build -DCMAKE_BUILD_TYPE=Release
```

## Troubleshooting

- *Nvidia Container Toolkit Configuration Error*

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

- *Port 11311 Forwarding Error*

If after running `roscore`, nothing is being prompt, it is possible that some processes is occuping the ros standard port 11311. In your local machine, list all the processes that are using port 11311:

```bash
sudo lsof -i :11311
```

And kill the corresponding processes with:

```bash
sudo kill <PID> 
```
