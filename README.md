# HTTP-Info
Homebrewed urlscan.io in a docker container. Screenshot a website and log web requests.

## Features
* Screenshots the homepage
* Records URL, method, status code, MIME type, and content size of every HTTP request
* Calculates SHA-256 hash of response bodies 

# Try It Out

### Prerequisites

* Install Docker.
* Be able to execute `docker` as the current user. [Linux Guide](https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user)

### Download the code
`git clone https://github.com/becksteadn/HTTP-Info.git && cd HTTP-Info`

### Build the container
`docker build -t http-info .`

### Run the container
Some pages will crash without a shared `/dev/shm`. 

`docker run -v /dev/shm:/dev/shm -v "$(pwd)":/info http-info https://scriptingis.life`
