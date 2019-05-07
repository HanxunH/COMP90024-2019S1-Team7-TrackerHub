FROM kuralabs/python3-dev

# Update and install prerequisites
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y              \
        build-essential             \
        mpich

RUN pip3 install --upgrade pip
RUN pip3 install Pillow torch torchvision requests
RUN pip3 install setuptools --upgrade

# Install mpi4py
RUN env MPICC=/usr/bin/mpicc pip3 install mpi4py

ENV http_proxy http://wwwproxy.unimelb.edu.au:8000
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000

RUN python3 -V

RUN mkdir /workspace
WORKDIR /workspace
ADD . /workspace

CMD [ "mpirun","-n","12","python","-u","coconut_image_recong.py","--load_with_config" ]
