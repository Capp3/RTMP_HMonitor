import logging
import os

import requests
import yaml
from vimeo import VimeoClient

# Set up logging
logger = logging.getLogger(__name__)


def load_config():
    """
    Load and parse the YAML configuration file
    Returns:
        dict: Parsed configuration
    """
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "config",
        "config.yml",
    )
    logger.debug(f"Loading configuration from: {config_path}")

    try:
        with open(config_path, "r") as file:
            # Load the raw YAML
            yaml_content = file.read()

            # Replace environment variables
            for key in os.environ:
                # Replace simple environment variables
                yaml_content = yaml_content.replace(f"${{{key}}}", os.environ[key])
                # Replace environment variables with default values
                yaml_content = yaml_content.replace(f"${{{key}:-", "${").replace(
                    "}", "}"
                )

            config = yaml.safe_load(yaml_content)
            logger.debug("Configuration loaded successfully")
            return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {e}")
        raise


def vimeolive_url(stream_name):
    """
    Retrieve Vimeo stream information for a specific stream
    Args:
        stream_name: Name of the stream from config
    Returns:
        dict: The JSON response containing stream information or None if not available
    """
    logger.info(f"Retrieving Vimeo stream data for: {stream_name}")

    try:
        config = load_config()

        # Find the specified stream configuration
        stream_config = next(
            (stream for stream in config["streams"] if stream["name"] == stream_name),
            None,
        )

        if not stream_config:
            logger.error(f"Stream '{stream_name}' not found in configuration")
            raise ValueError(f"No configuration found for stream {stream_name}")

        if "vimeolive" not in stream_config["provider"]:
            logger.error(f"Stream '{stream_name}' does not have Vimeo configuration")
            raise ValueError(f"No Vimeo configuration found for stream {stream_name}")

        vimeo_config = stream_config["provider"]["vimeolive"]
        logger.debug(f"Found Vimeo configuration for stream '{stream_name}'")

        # Vimeo API client and authentication setup
        vimeo_client = VimeoClient(
            token=vimeo_config["vimeo_token"],
            key=vimeo_config["vimeo_key"],
            secret=vimeo_config["vimeo_secret"],
        )

        # Build the url to access Vimeo API
        event_id = vimeo_config["eventid"]
        url = f"https://api.vimeo.com/live_events/{event_id}"
        logger.debug(f"Requesting Vimeo API URL: {url}")

        # request stream data from api
        response = vimeo_client.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        logger.info(f"Successfully retrieved stream data for '{stream_name}'")
        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to retrieve Vimeo data for stream '{stream_name}': {e}")
        return None
    except Exception as e:
        logger.error(
            f"Unexpected error retrieving Vimeo data for stream '{stream_name}': {e}"
        )
        return None


def youtube_url(stream_name):
    """
    Retrieve YouTube API data for a specific stream
    Args:
        stream_name: Name of the stream from config
    Returns:
        dict: The JSON response from YouTube API or None if request fails
    """
    logger.info(f"Retrieving YouTube data for stream: {stream_name}")

    try:
        config = load_config()

        # Find the specified stream configuration
        stream_config = next(
            (stream for stream in config["streams"] if stream["name"] == stream_name),
            None,
        )

        if not stream_config:
            logger.error(f"Stream '{stream_name}' not found in configuration")
            raise ValueError(f"No configuration found for stream {stream_name}")

        if "youtube" not in stream_config["provider"]:
            logger.error(f"Stream '{stream_name}' does not have YouTube configuration")
            raise ValueError(f"No YouTube configuration found for stream {stream_name}")

        youtube_config = stream_config["provider"]["youtube"]
        logger.debug(f"Found YouTube configuration for stream '{stream_name}'")

        # YouTube Data API v3 Endpoint
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,liveStreamingDetails&id={youtube_config['video_id']}&key={youtube_config['api_key']}"
        logger.debug("Requesting YouTube API data")

        # Request data from YouTube API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        if response.status_code == 200:
            data = response.json()
            logger.info(
                f"Successfully retrieved YouTube data for stream '{stream_name}'"
            )
            return data

        logger.warning(
            f"YouTube API request failed with status code: {response.status_code}"
        )
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to retrieve YouTube data for stream '{stream_name}': {e}")
        return None
    except Exception as e:
        logger.error(
            f"Unexpected error retrieving YouTube data for stream '{stream_name}': {e}"
        )
        return None


# Future providers

# def facebooklive_url():

# def ST2110():
