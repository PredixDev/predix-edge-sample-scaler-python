# Use Predix Edge base alpine linux image
#FROM dtr.predix.io/predix-edge/alpine-amd64

# start with the node image
FROM node:10-alpine

LABEL maintainer="Predix Edge Adoption"
LABEL hub="https://hub.docker.com"
LABEL org="https://hub.docker.com/u/predixedge"
LABEL repo="predix-edge-sample-scaler-python"
LABEL version="1.0.6"
LABEL support="https://forum.predix.io"
LABEL license="https://github.com/PredixDev/predix-docker-samples/blob/master/LICENSE.md"

#install python3 and the latest pip into the base image
RUN apk update && apk add python3 && pip3 install --upgrade pip

# Set the working directory to /app
WORKDIR /src

# Copy the current directory contents into the container at /src
ADD . /src

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME my-python-edge-app


# Run app.py when the container launches
CMD ["python3", "src/app.py"]
