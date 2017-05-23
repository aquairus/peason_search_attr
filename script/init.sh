apt-get update
apt-get install freeglut3-dev build-essential libx11-dev libxmu-dev libxi-dev libgl1-mesa-glx libglu1-mesa libglu1-mesa-dev python-opencv vim  python-pip  python-dev python-dateutil  curl  -y


apt-get install -y \
  git \
  wget \
  bc \
  cmake \
  libatlas-base-dev \
  libatlas-dev \
  libboost-all-dev \
  libopencv-dev \
  libprotobuf-dev \
  libgoogle-glog-dev \
  libgflags-dev \
  protobuf-compiler \
  libhdf5-dev \
  libleveldb-dev \
  liblmdb-dev \
  libsnappy-dev \
  python-dev \
  python-pip \
  python-numpy \
  gfortran 

apt-get install libfreetype6-dev libxft-dev

apt-get install python-numpy python-scipy python-matplotlib python-sklearn python-skimage python-h5py python-protobuf python-leveldb python-networkx python-nose python-pandas python-gflags Cython ipython python-yaml -y

pip install easydict flask simplejson imutils widgetsnbextension setuptools enum singledispatch jsonschema scandir    flask-gzip
pip pyzmq setuptools -U
pip install numpy  -U
pip install flask-gzip elasticsearch
pip install matplotlib easydict
pip install jupyter

sudo ln /dev/null /dev/raw1394



python -c 'import ipykernel.kernelspec; ipykernel.kernelspec.install(user=True)'
