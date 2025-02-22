import json
import requests


class hardware_test():

  def __init___(self):
        super().__init__()
        self.init_logging()

  ## Poll hardware
  def encoder_test():

    try:
      # Setting a timeout (in seconds) to avoid indefinite hanging
      response = requests.get(hardware_url, timeout=10)
      # Raise an error for bad HTTP status codes
      response.raise_for_status()
      
      # Process and print the JSON response in a pretty format
      pretty_json = json.dumps(response.json(), indent=4)
      print(pretty_json)
    except requests.exceptions.RequestException as e:
      print(f"Error connecting to the API: {e}")