# File-Manager (repository)

## How it Works

- An `python` image is used

- The `pip` is updaded to latest version

- Change working directory to where the project's code will be reside

- The project's python dependencies are copied to the project's home directory and are installed

- The project's source code is copied inside the image

- An entrypoint using python command and a cmd command that runs the expected main script of the project are executed

## How to Configure

1. Select a `python` image version that matches the one used to develop the project (replace `latest`)

2. Change the environmental variable named `FILE_MANAGER_SERVER_URL` for CORS support

3. An environmental variable named `FILE_MANAGER_API_KEY` is used to enabled authentication where a header named `X-Api-Key` and the value of the env var must be present on each request

4. Change to `True` or `False` the environmental variables `FILE_MANAGER_AUTH_INCOMING` and `FILE_MANAGER_AUTH_OUTGOING` to control which requests should be lock under authentacation michanism

## How to Use

Build image

```shell
docker build -t file-manager:latest .
```

Run container

```shell
docker run -idt -p 8000:8000 --restart=unless-stopped --name file-manager file-manager:latest
```
