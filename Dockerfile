FROM python:3.7-alpine

WORKDIR app/


# Run install your requirements
RUN pip install requirements.txt

# Copy application modules to docker container
COPY . /app/

# Run module with intit application
CMD ['python', '/app/assistant.py']