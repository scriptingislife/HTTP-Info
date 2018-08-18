# HTTP-Info
Homebrewed urlscan.io in a docker container.

# Try It Out

### Download the code
`git clone https://github.com/becksteadn/HTTP-Info.git && cd HTTP-Info`

### Set your puush.me API key

![Get your API key](https://puu.sh/BgkK6/fa2d86e75d.png)


`export HTTPINFO_PUUSHAPI="<API Key>"`

### Build the container
`docker build .`

### Run the container
Some pages will crash without a shared `/dev/shm`. 

`docker run -v /dev/shm:/dev/shm -e HTTPINFO_PUUSHAPI -e HTTPINFO_URL="https://scriptingis.life" <image-id>`
