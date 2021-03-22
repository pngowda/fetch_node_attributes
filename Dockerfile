# Based on python3 docker image
FROM python:3.8

# Updating apps
# RUN apt-get update -y

# Setting docker working directory.
WORKDIR /vagrant

# Copy the required files for docker build
COPY node_info.py requirements.txt ./

# Setting file permissions.
RUN chmod 777 node_info.py requirements.txt

# Install library dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Running python script.
CMD ["python3","node_info.py"]