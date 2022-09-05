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