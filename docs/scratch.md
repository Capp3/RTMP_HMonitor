# RTMP Application development

I am developing an application to monitor video streams and provide a dashboard. I am only deveolping the data collection. For storage I am choosing InfluxDB, and for dashboard I am using Grafana. I am running InfluxDB and Grafana via docker for ease. I  do want to eventually be able to containerize this app.

I want the configuration of the app to be done using yaml, and preferably a .env file, simular to how docker works.

The intention is to have a system where a "thread" collections information from the streaming hardware, using a REST API to accuire json data. The stream will be analyised by ffprobe, commanded to provide a json output. This will be done for each stream defined. The various json data is then to be assembled into a single json dataset that will be sent to influxdb, as well as be avilable to via a http GET command. This will be repeated frequently.

I would like you to look over my environment and project structure to make sure that I have started in the right direction. I also want to know if you see obvious problems. I do not want you to start coding at this point. I am most interested to know if my "config.yml" file is appropriate and will work. I want to standardize the interface before i dive into the project.

## structure

```bash
|- .github
|    |- dependabot.yml          # Dont know this cute guy yet
|- config                       # Mount tpython container at `/usr/local/bin/rtmpmonitor/config`
|    |- config.yml              # configuration file for the application
|    |- sample.env
|    |- .env                    # .env file
|- docker                       # Docker for backend services, grafana and influxdb
|    |- docker-compose.yml
|- docs
|    |- scratch.md              # notes / prompts / crap
|    |- structure.md            # This here, the only way I can think
|- src                          # The application
|    |- attributes              # configuration information
|    |    |- hardware.py        # definitions for interacting with different hardware models
|    |    |- providers.py       # definitions for interacting with different streaming providers
|    |- main.py                 # Python application basics/ setup logging
|    |- threads.py              # program actions
|- .gitignore                   # Git ignore file
|- LICENSE                      # Pretty straight forward
|- README.md                    # Readme... yep
|- requirements.txt
|- rtmpmonitor.py               # Entry Script
|- RTMP_HMonitor.code-workspace # VS Code Workspace config file
```

## config.yml

```yaml
backend:
  database:
    influxdb:
      host: localhost
      port: 8086
      username: rtmphealthmonitor
      password: rtmphealthmonitor
      org: docs
      reporting_time: 1000 # in milliseconds
  reporting:
    json_output:
      port: 8092
rtmpstreams:
  stream1:
    hardware:
      webpresentor:
        host: 172.16.16.16
    provider:
      vimeo:
        eventid: '1231231'
        vimeo_token: ${vimeo_token}
        vimeo_key: ${vimeo_key}
        vimeo_secret: ${vimeo_secret}
  stream2:
    hardware:
      webpresentor:
        host: 172.16.16.17
    provider:
      vimeo:
        eventid: '1231232'
        vimeo_token: ${vimeo_token}
        vimeo_key: ${vimeo_key}
        vimeo_secret: ${vimeo_secret}
  stream3:
    hardware:
      webpresentor:
        host: 172.16.16.18
    provider:
      vimeo:
        eventid: '1231233'
        vimeo_token: ${vimeo_token}
        vimeo_key: ${vimeo_key}
        vimeo_secret: ${vimeo_secret}
  stream4:
    hardware:
      webpresentor:
        host: 172.16.16.19
    provider:
      vimeo:
        eventid: '1231234'
        vimeo_token: ${vimeo_token}
        vimeo_key: ${vimeo_key}
        vimeo_secret: ${vimeo_secret}
```

## docker-compose.yml

```yaml
name: rtmphm_services
services:
  influxdb2:
    image: influxdb:2
    user: 1000:1000
    restart: unless-stopped
    container_name: influxdb
    ports:
      - 8086:8086
    environment:
      DOCKER_INFLUXDB_INIT_MODE: setup
      DOCKER_INFLUXDB_INIT_USERNAME: rtmphealthmonitor
      DOCKER_INFLUXDB_INIT_PASSWORD: rtmphealthmonitor
      DOCKER_INFLUXDB_INIT_ADMIN_TOKEN: changemetosomethingsecret
      DOCKER_INFLUXDB_INIT_ORG: docs
      DOCKER_INFLUXDB_INIT_BUCKET: home
    volumes:
      - type: volume
        source: influxdb2-data
        target: /var/lib/influxdb2
      - type: volume
        source: influxdb2-config
        target: /etc/influxdb2

  grafana:
    image: grafana/grafana-enterprise
    container_name: grafana
    user: 1000:1000
    restart: unless-stopped
    ports:
     - '3000:3000'
    volumes:
      - grafana-storage:/var/lib/grafana

volumes:
  influxdb2-data:
  influxdb2-config:
  grafana-storage:
  ```
  