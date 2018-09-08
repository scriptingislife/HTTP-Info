# HTTP-Info
Homebrewed urlscan.io in a docker container. Screenshot a website and log web requests.

# Try It Out

### Prerequisites

* Install Docker.
* Be able to execute `docker` as the current user. [Linux Guide](https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user)
* Have a [puush.me](https://puush.me/) account.

### Download the code
`git clone https://github.com/becksteadn/HTTP-Info.git && cd HTTP-Info`

### Set your puush.me API key

![Get your API key](https://puu.sh/BgkK6/fa2d86e75d.png)


`export HTTPINFO_PUUSHAPI="<API Key>"`

### Build the container
`docker build -t http-info .`

### Run the container
Some pages will crash without a shared `/dev/shm`. 

`docker run -v /dev/shm:/dev/shm -e HTTPINFO_PUUSHAPI -e HTTPINFO_URL="https://scriptingis.life" http-info`
