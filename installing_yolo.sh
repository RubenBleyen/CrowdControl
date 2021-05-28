echo "Updating..."
sudo apt update
sudo apt upgrade

echo "Installing python..."
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8

echo "Installing other dependencies..."
sudo apt install make git g++

echo "Installing cmake..."
sudo apt install cmake

echo "Installing wget..."
sudo apt install wget

echo "Installing CUDA Toolkits..."
wget -O /etc/apt/preferences.d/cuda-repository-pin-600 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /"
sudo apt install cuda-10-2
echo 'export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}' >> ~/.bashrc

echo "Installing opencv..."
sudo apt install libopencv-dev python3-opencv