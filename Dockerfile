# Pull Base Image
FROM python:3.11-slim-buster

# Python environment setup
# Keeping Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turning off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Setting working directory
ENV PROJECT=/home/app
WORKDIR ${PROJECT}

# Installing requirements
COPY ./requirements.txt ${PROJECT}/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r ${PROJECT}/requirements.txt

# Copying project
COPY . ${PROJECT}

# Set container port
EXPOSE 8185

#Running application
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8185" ]
