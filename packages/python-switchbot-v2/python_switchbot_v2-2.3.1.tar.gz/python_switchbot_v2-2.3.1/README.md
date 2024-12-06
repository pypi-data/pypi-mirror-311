This is a fork from [jonghwanhyeon/python-switchbot](https://github.com/jonghwanhyeon/python-switchbot), which seemed
abandoned at the time of the form. The fork was necessary since the package import name conflicts with https://github.com/sblibs/pySwitchbot,
used by home assistant. I will merge any pull requests, but I am not planning on actively developing it.

# python-switchbot
A Python library to control SwitchBot devices connected to SwitchBot Hub.

## Requirements
- Python 3.7+
- [A SwitchBot Token](https://github.com/OpenWonderLabs/SwitchBotAPI#getting-started)

## Installation
```python
pip install python-switchbot-v2
```

## Usage


### Devices

```python
from python_switchbot_v2 import SwitchBot

# To get the token and secret, please refer to https://github.com/OpenWonderLabs/SwitchBotAPI#getting-started
your_switch_bot_token = '98a6732b2ac256d40ffab7db31a82f518969f4d1a64eadff581d45e902327b7c577aa6ead517bda589c19b4ca0b2599b'
your_switch_bot_secret = '222cdc22f049d111c5d0071c131b8b77'
switchbot = SwitchBot(token=your_switch_bot_token, secret=your_switch_bot_secret)
# To list all devices
devices = switchbot.devices()
for device in devices:
    print(device)
# Bot(id=CD0A18B1C291)
# Lock(id=CD0A1221C291)
# HubMini(id=4CAF08629A21)
# Bot(id=5F0B798AEF91)

# If you already know a device id:
device = switchbot.device(id='5F0B798AEF91')
# Device(id=5F0B798AEF91)

# To query a status of a device
print(device.status())
# {'power': 'off'}

# To command actions,
device.command('turn_on')
device.command('turn_off')
device.command('press')
device.command('set_position', parameter='0,ff,80')

# For some device types like Bot:
bot = devices[0]
bot.turn('on')
bot.turn('off')
bot.toggle()
bot.press()

# For some device types like Lock:
lock = devices[1]
lock.lock()
lock.unlock()
lock.toggle()
```

### Remotes
```python
# To list all infra red remotes
remotes = switchbot.remotes()
for remote in remotes:
    print(remote)

# If you already know a remote id:
remote = switchbot.remote(id='')

# Supported devices such as fans, air purifiers:
remote.turn('on')
remote.turn('off')

# To send supported commands,
remote.command('swing')
remote.command('low_speed')

# To send custom commands,
remote.command('MyCustomCommand', customize=True)
```

### Scenes
```python
# To list all infra red remotes
scenes = switchbot.scenes()
for scene in scenes:
    print(scene)

# If you already know a remote id:
scene = switchbot.scene(id='')

# To execute scene
scene.execute()
```
