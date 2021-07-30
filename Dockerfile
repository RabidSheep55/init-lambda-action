# Base image contains awscli and pip
FROM woahbase/alpine-awscli

RUN mkdir app
WORKDIR /app

# Copy code and install requirements
COPY action.yml main.py requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

# Setup to be able to run main.py
ENV PYTHONPATH /app

# Code file to execute when the docker container starts up
CMD ["./main.py"]
