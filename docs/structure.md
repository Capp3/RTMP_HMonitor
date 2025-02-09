# Application Structure

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