# HOracle

HOracle is an detailed activity tracker for SideFX Houdini.

![grafana-1](https://user-images.githubusercontent.com/85954505/191325559-afd7c27e-99a7-436d-a875-552cf7e45286.png)
![grafana-2](https://user-images.githubusercontent.com/85954505/191325576-cdfad3b2-96c9-48d1-bb07-12f899bc0ca9.png)


This reposity is split in two branches, client and server.

## Features

- Customizable through config.json
- Grafana visualization
- Can differentiate between regular activity and viewport activity
- Can collect data from multiple houdini instances and users


## Server Installation

Minimal setup requires docker to be installed. 

- Install docker if missing
- run the docker file, eg: docker-compose up -d --build


### Grafana Configuration

- Add prometheus as data source (default prometheus endpoint in docker = http://prometheus:9090 )
- Import horacle-style.json as template
## Client Installation
- create directory for client and specify the path to it in houdini.env file
- inside directory create 456.py file and python directory
- clone client branch into python directory
- inside 456.py file import main from HOracle and run, eg: 
```
from HOracle import main as entry
entry.main()
```

Some parameters can be customized through config.json file. The client tries to fetch it from env variable "HORACLE_PATH". If not specified default values will be used
### default config.json

| key | values |
| ------ | ------ |
| user | "user" |
| url | "http://localhost:2106/" |
| endpoints | ["ParmTupleChanged","NodeCreated","NodeDeleted","SceneSaved","RenderActivity", "ViewportActivity"] |
| contexts | ["obj","out"] |






