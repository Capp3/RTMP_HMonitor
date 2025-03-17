def bmd_webpresentorhd():
    hardware_url = "http://{{ streams.hardware.webpresentor.ip_address }}/control/api/v1/livestreams/0"

    response = requests.get(hardware_url)
    data = response.json()
    print(json.dumps(data, indent=4))
