def vimeolive_url():
    # Retrieve Vimeo streaming url for HLS playback to probe

    # Vimeo API client and authentication setup
    vimeo_client = VimeoClient(
        token={{ streams.provider.vimeo.vimeo_token }},
        key={{ streams.provider.vimeo.vimeo_key }},
        secret={{ streams.provider.vimeo.vimeo_secret }}
    )

    # Build the url to access Vimeo API
    vimeo_retrieval_url = 'https://api.vimeo.com/me/live_events/{{ streams.provider.vimeo.vimeo_key }}/m3u8_playback'

    # request url from api and store the data
    response = client.get(vimeo_retrieval_url)
    data = response.json()
    # Record the stream url
    data.get('m3u8_playback_url'):
        return data['m3u8_playback_url']
    # Return url to probe to main thread
        probe_url = data

## These are placeholders for potential future providers
# def facebooklive_url():

# def ST2110():

if __name__ == '__main__':
    main()
