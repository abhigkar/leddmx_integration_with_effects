# LEDDMX BLE Light Integration with Effects

Custom Home Assistant integration for LEDDMX-03 BLE lights.  
Supports ESPHome Bluetooth Proxy and local host Bluetooth.

### Features
- Auto-discovery of LEDDMX-03 devices
- Config Flow support
- On/Off, RGB, brightness
- Effects: fade, flash, jump
- Uses characteristic UUID `0xFFE1`

### Installation
1. Copy `leddmx` folder to `config/custom_components/`
2. Restart Home Assistant
3. Go to **Settings → Devices & Services → Add Integration → LEDDMX BLE Light**
4. Select the discovered device
5. Effects can be applied via `effect` attribute in services