# Quick Start

0. target System
- Linux Machine that can download docker
- Can use Nvidia GPU

1. Inatll Docker
Check this [Docker official page](https://docs.docker.com/engine/install/), then install docker on your system.

2. Install Nvidia Docker
Check this [github repository](https://github.com/NVIDIA/nvidia-docker), then install nvidia docker.

3. Clone This Repository
Enter the following command in your terminal.
```
git clone [This repository URL]
```

4. Download Train and Test Data
Download data for learning and predict from [competition page](https://signate.jp/competitions/266).
Then, moving data to "Datas" directory.

5. Build Dockerfile
Enter the following command in your terminal.
```
docker built -t competition .
```
Then, wait finishing the build.

6. Start docker container
Enter the following command in your terminal.
```
mkdir MountPoint
docker run -it --rm --mount type=bind,src=$(pwd)/MountPoint,dst=/home/MountPoint competition
```

7. Start learning or predict, enter the following command.
If you want learning, 
```
python main.py --learning
```
Model file is in /home/Models.

If you want to save your learning model file, use:
```
cp /home/Models/DenceOnly.hdf5 /home/MountPoint
```
It is available in "MountPoint" directory in  your current directory.


you want to predict, enter the following command.
```
python main.py
```

The result is available in "/home/Outputs/"
