# Base image contains awscli and pip
FROM woahbase/alpine-awscli

# Copy code and install requirements
COPY action.yml main.py requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

# Code file to execute when the docker container starts up
CMD ["./main.py"]
