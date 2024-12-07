GatewayAPI

Common entrypoints
- discover()
    List of devices

- turn_on()
- turn_off()

- get_power_state()  
    on/off/standby

- get_device_info() -> Dict
    name, ip, mac, type, model,...

- get_device_status() -> Dict
    power_state, other
        switch      - 
        light       - brightness, color
        receiver    - volume, muted, whats_playing, input_src

- is_available() -> bool
    Is API up, is device online?

- _call_api()
- 