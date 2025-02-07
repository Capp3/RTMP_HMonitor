# Application Structure

```bash
|- .gitignore                  # Git ignore file
|- .env                        # dotenv for docker compose
|- sample.env
|- LICENSE                     # Pretty straight forward
|- README.md                   # Readme... yep
|- structure.md                # This here, the only way I can think
|- docker-compose.yml          # The complete docker compose development stack  w/ influxdb & grafana, python container
|- rtmpmonitor.py              # Entry Script
|- app                         # The application and dockerfile, mounted to python container `/usr/local/bin/rtmpmonitor`
|    |- main.py                # Python application basics/ setup logging
|- config                      # Mount tpython container at `/usr/local/bin/rtmpmonitor/config`
|    |- config.yml             # configuration file for the application
```