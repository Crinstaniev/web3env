# web3env

## Install Docker

The demo relies on `docker` to run. To install docker, refer to the docker official documentation <https://docs.docker.com/engine/install/>

## Run DEMO

Depend on your platform, we built docker images for `arm64` and `amd64`.

For `arm64` (Arm Chips, Apple Silicon) platform, run:

```bash
docker run -p 8080:8080 --name web3env web3env:arm64
```

For `amd64` (Intel CPU, AMD CPU) platform, run:

```bash
docker run -p 8080:8080 --name web3env web3env:amd64
```

Then you can access the UI from `http://localhost:8080`.
