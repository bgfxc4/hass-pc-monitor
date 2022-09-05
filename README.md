# hass-pc-monitor

This project enables you to be able to control your PC, Server or similar, remotely by using [Home Assistant](https://www.home-assistant.io/).
Controlling your machine includes reading system data (such as CPU usage per core, total and used memory/swap and more) and executing predefined commands, for example sending a notification or powering your machine of.

## Installation

### Home Assistant

For installing Home Assistant head over to their [installation guide](https://www.home-assistant.io/installation/).

### Home Assistant integration

The Home Assistant integration is what enables Home Assistant to talk to your machine and display the data within itself.
```
Stop your Home Assistant instance
cd /your-homeassistant-user-home-path/.homeassistant    # for example /home/homeassistant/.homeassistant
cd custom_components    # you may need to create this directory first with 'mkdir custom_components'
git clone https://github.com/bgfxc4/hass-pc-monitor
cp -r hass-pc-monitor/hass_pc_monitor ./
rm -rf hass-pc-monitor
Start your Home Assistant instance
```

### The daemon

The daemon will be running all the time on the machines you want to monitor, so you need to perform this installation on all machines you want to be monitored.

Requirements: `cargo`
```
git clone https://github.com/bgfxc4/hass-pc-monitor
cd hass-pc-monitor/daemon
cargo build --release
cd target/release
The 'daemon' file is the executable. When executing, make sure that there is a config.json file in the directory you are executing it in.
```

## Setup in Home Assistant

In the Home Assistant web interface, go to Settings > Devices & Services > Add Integration (in the lower left corner).
Search for `PC Monitor`, click on it and continue with entering the IP of the machine you want to monitor and the port and password you configured in the `config.json`.
Make sure that the daemon is running on the machine, that is to be monitored and click on `Submit`.
If evering went ok, you should now be prompted with a success message. You can select the area you want your machine to be in and click `Finish`.

For any occuring issues, don't hesitate and open an issue on GitHub.

## Config

To configure the daemon on the machine, you have to create the file `$HOME/.config/hass-pc-monitor/config.json` on Linux, `C:\Users\USER\AppData\Roaming\hass-pc-monitor\config.json` on Windows or `$/Users/USER/Library/Application Support/hass-pc-monitor/config.json` on Mac.

The config.json file should contain something similar to the following.
```
{
    "port": 5573,   # The port your daemon should run on
    "update_interval": 30,  # After how many seconds the data should be fetched
    "commands": {   # List of predefined commands, that can be executed by Home Assistant
        "test_notify": {    # Example definition of a command. The key ("test_notify") is the identifier of the command. It should not be used twice
            "display_name": "Test notification",    # The name that is displayed in Home Assistant
            "command": "notify-send",   # The executable that should be executed (Without parameters!)
            "args": ["asdasd1", "222asdad"] # List of parameters for the command
        }
    }
}
```

## Systemd service

To really use this system, the daemon has to be running at all times. On Linux you can use an own Systemd service to achieve that.
Just create the file `/etc/systemd/system/hass-pc-monitor.service` with the content
```
Description=Daemon to send data to the Home Assistant integration
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=YourUserName
ExecStart=/the/path/to/your/daemon/executable

[Install]
WantedBy=multi-user.target
```
Now you can execute `sudo systemctl start hass-pc-monitor` to start the service and `sudo systemctl status hass-pc-monitor` to get the status of the service.

If you want the service to be run on system startup, execute `sudo systemctl enable hass-pc-monitor`.