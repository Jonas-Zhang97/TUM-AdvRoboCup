##### Base Stage #####

FROM nvidia/cuda:12.2.2-devel-ubuntu20.04 as base

LABEL MAINTAINER="yueyang.zhang@tum.de"

SHELL [ "/bin/bash", "-c" ]

# setup environment
ENV LANG=en_US.UTF-8
ENV LC_NUMERIC=en_US.UTF-8
ENV LC_ALL=C
ENV DEBIAN_FRONTEND=noninteractive

# setup timezone
RUN echo 'Etc/UTC' > /etc/timezone && \
  ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
  apt-get update && \
  apt-get install -q -y --no-install-recommends tzdata && \
  rm -rf /var/lib/apt/lists/*

# USE German mirror to speed up things
RUN cp /etc/apt/sources.list /etc/apt/sources.list.old \
  && sed -i -e 's/http:\/\/archive\.ubuntu\.com\/ubuntu\// \
  http:\/\/de.archive\.ubuntu\.com\/ubuntu/' /etc/apt/sources.list
RUN apt-key update && apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 4B63CF8FDE49746E98FA01DDAD19BAB3CBF125EA

# install packages
RUN apt-get update && apt-get install -q -y --no-install-recommends \
  terminator \
  vim \
  git \
  bash-completion \ 
  software-properties-common \
  ca-certificates \
  curl \
  wget \
  ssh \
  dirmngr \
  gnupg2 \
  lsb-release \
  python3.7\
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

# Fix ssl certificate issue
RUN apt-get update
RUN apt-get install ca-cacert \
  && update-ca-certificates \
  && rm -rf /var/lib/apt/lists/*


##### ROS Stage #####

FROM base as ros

# install ros
RUN sh -c 'echo "deb [arch=amd64] http://packages.ros.org/ros/ubuntu focal main" > /etc/apt/sources.list.d/ros-latest.list'
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
RUN apt-get update
RUN apt-get install -y ros-noetic-desktop-full
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
RUN source ~/.bashrc

RUN apt-get update && apt-get install --no-install-recommends -y \
  python3-rosdep \
  python3-rosinstall \
  python3-rosinstall-generator \
  python3-wstool \
  python3-vcstools \
  python3-catkin-tools\
  && rm -rf /var/lib/apt/lists/*

# bootstrap rosdep
RUN rosdep init \
  && rosdep update

ENV ROS_PACKAGE_PATH=/opt/ros/noetic/share

##### User Stage #####

FROM ros as user

ARG USERNAME=cgnet-developer
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
  && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && apt-get update \
  && apt-get install -q -y sudo \
  && rm -rf /var/lib/apt/lists/* \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
  && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

CMD ["bash"]

RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

RUN sudo mkdir -p /home/$USERNAME/Downloads/openssl/ssl \
  && sudo cp -r /etc/ssl/* /home/$USERNAME/Downloads/openssl/ssl/ \
  && sudo rm /etc/ros/rosdep/sources.list.d/20-default.list \
  && sudo rosdep init \
  && rosdep update

RUN echo "source /opt/ros/noetic/setup.bash" >> /home/$USERNAME/.bashrc


##### Runtime Stage #####

FROM user as runtime

ENV NVIDIA_VISIBLE_DEVICES \
  ${NVIDIA_VISIBLE_DEVICES:-all}

ENV NVIDIA_DRIVER_CAPABILITIES compute,graphics,utility,video,display

# detailed fix for the ssl certificate issue
RUN sudo mkdir -p /home/$USERNAME/Downloads/openssl/ssl \
  && sudo cp -r /etc/ssl/* /home/$USERNAME/Downloads/openssl/ssl/ \
  && sudo rm /etc/ros/rosdep/sources.list.d/20-default.list \
  && sudo rosdep init \
  && rosdep update

RUN echo "source /opt/ros/noetic/setup.bash" >> /home/$USERNAME/.bashrc


##### Dependencies Stage #####

FROM runtime as dependencies

# setup denpendencies for Contact GraspNet
RUN sudo apt-get update && sudo apt-get install -y \
  build-essential \
  bzip2\
  ca-certificates \
  clang \
  curl \
  libblas-dev \
  libbz2-dev \
  libdbus-1-dev \
  libdbus-glib-1-dev \
  libexpat1-dev \
  libfontconfig1-dev \
  libfreetype6-dev \
  libglib2.0-dev \
  libgstreamer-plugins-base1.0-dev \
  libgstreamer1.0-dev \
  libhdf4-alt-dev \
  libhdf5-dev \
  libicu-dev \
  libomp-dev \
  libjpeg-dev \
  libjsoncpp-dev \
  libclang-10-dev \
  libcurl4-openssl-dev \
  libkrb5-dev \
  liblcms2-dev \
  libnetcdf-dev \
  libogg-dev \
  libpng-dev \
  libssl-dev \
  libtheora-dev \
  libtiff-dev \
  libtool \
  libvorbis-dev \
  libxcb1-dev \
  libxml2-dev \
  libxslt1-dev \
  llvm \
  lz4 \
  qt5-default \
  tcl-dev \
  tk-dev \
  uuid-dev \
  zlib1g-dev \
  cudnn9-cuda-12 \
  && sudo rm -rf /var/lib/apt/lists/*

RUN pip install \
  pillow==8.0.1 \
  pyface==7.1.0 \
  pygments==2.7.2 \
  pyparsing==2.4.7 \
  PyQt5==5.9.2 \
  pyside2==5.11.0 \
  python-dateutil==2.8.1 \
  setuptools==50.3.1 \
  sip==5.0.0 \
  six==1.15.0 \
  tornado==6.0.4 \
  traits==6.1.1 \
  traitsui==7.1.0 \
  trimesh==3.8.12 \
  wheel==0.35.1 \
  h5py==2.10.0\
  future==0.18.2 \
  envisage==4.9.2 \
  absl-py==0.11.0 \
  astor==0.8.1 \
  astunparse==1.6.3 \
  apptools==4.5.0 \
  cachetools==4.1.1 \
  certifi==2020.6.20 \
  configobj==5.0.6 \
  chardet==3.0.4 \
  cycler==0.10.0 \
  kiwisolver==1.3.0 \
  mkl==2021.1.1 \
  mkl-service==2.4.0 \
  mkl_fft==1.3.0 \
  mkl_random==1.2.2 \
  decorator==4.4.2 \
  freetype-py==2.2.0 \
  gast==0.3.3 \
  google-auth==1.23.0 \
  google-auth-oauthlib==0.4.2 \
  google-pasta==0.2.0 \
  grpcio==1.33.2 \
  h5py==2.10.0 \
  idna==2.10 \
  imageio==2.9.0 \
  importlib-metadata==2.0.0 \
  keras-applications==1.0.8 \
  keras-preprocessing==1.1.2 \
  markdown==3.3.3 \
  matplotlib==3.3.2 \
  mayavi==4.7.1 \
  networkx==2.5 \
  numpy==1.19.2 \
  olefile==0.46 \
  oauthlib==3.1.0 \
  opencv-python==4.4.0.46 \
  opt-einsum==3.3.0 \
  protobuf==3.13.0 \
  pyasn1==0.4.8 \
  pyasn1-modules==0.2.8 \
  pyglet==1.5.9 \
  pyopengl==3.1.0 \
  pyrender==0.1.43 \
  pyyaml==5.3.1 \
  requests==2.24.0 \
  requests-oauthlib==1.3.0 \
  rsa==4.6 \
  rtree \
  scipy==1.4.1 \
  shapely==1.7.1 \
  six==1.15.0 \
  tensorboard==2.2.2 \
  tensorboard-plugin-wit==1.7.0 \
  tensorflow-estimator==2.2.0 \
  tensorflow-gpu==2.2.0 \
  termcolor==1.1.0 \
  urllib3==1.25.11 \
  tqdm==4.51.0 \
  traits==6.1.1 \
  traitsui==7.1.0 \
  trimesh==3.8.12 \
  vtk \
  werkzeug==1.0.1 \
  wrapt==1.12.1 \
  zipp==3.4.0 \
  python-fcl==0.0.12

# Some more tools
RUN sudo apt-get update
RUN sudo apt-get install -y net-tools \
  && sudo apt-get install -y iputils-ping \
  && sudo apt-get install -y lshw