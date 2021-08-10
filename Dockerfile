FROM tensorflow/tensorflow:2.4.2-gpu
WORKDIR /home

CMD bash

COPY [\
"Data",\
"Models",\
"config.py",\
"main.py",\
"preprocess.py",\
"type.py",\
"utils.py",\
"requirement.txt",\
"/home/"\
]

RUN \
alias sudo="";\
set -e;\
    pip install -r requirement.txt;\
    mkdir Data Models MountPoint;\
    mv sample_submit.csv test.csv train.csv Data;\
    mv DenceOnly.hdf5 Models\
    #sudo apt install -y libgl1-mesa-dev;
