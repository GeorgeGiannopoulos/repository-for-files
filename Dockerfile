FROM python:latest

ENV PROJECT_HOME=/app \
    VIRTUAL_ENV=/opt/venv

# set env variables
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# Prepare Python Environment:
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python -m pip install --upgrade pip
RUN pip install wheel

WORKDIR ${PROJECT_HOME}

# Install dependencies:
COPY requirements.txt ${PROJECT_HOME}
RUN pip install -r requirements.txt

# Copy Source code:
COPY . ${PROJECT_HOME}

# Expose to the World:
EXPOSE 8000

# Ensure Persistence of Data:
VOLUME ["/app/files"]

# Run the application:
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
