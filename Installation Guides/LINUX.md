# Linux installation
This guide will help you install all the dependencies for this project

There will be an install script that will run the following commands for your distribution, no huss, no fuss.

**WARNING**

Do not blindly run scripts, we are not responsible for any breakage of the system.

## Arch Linux
### Dependencies 
`python >= 3.11`

`gnuradio`

`gnuradio-companion`

`gnuradio-osmodr` (Has HackRF and RTL-SDR drivers)

`soapyrtlsdr` (Using soapy for this)

`gr-sattlites` (AUR)

**Warning**:
This will require you to install arch python packages i.e `python-gnuradio`

If you don't want to do this see the Conda installation however still grab the drivers for the HackRF and RTL-SDR.

### Install

**Using yay**

`yay -S python gnuradio gnuradio-companion gnuradio-osmodr soapyrtlsdr gr-sattlies`

**Using pacman with manual AUR Install**

```bash
sudo pacman -S python gnuradio gnuradio-companion gnuradio-osmodr soapyrtlsdr
```
Clone the repository and install the through the AUR
```bash
git clone https://aur.archlinux.org/gr-satellites.git
cd gr-satellites
makepkg -si
```


## Debian

### Install
`sudo apt install gnuradio`

## Fedora/RHEL

### Install
```bash
sudo dnf install gnuradio
# OR
sudo yum install gnuradio
```

## Import YML files for GRC

We use custom blocks in our GRC and as a result, there are certain blocks that the user needs to import for GRC usage.

Copy and paste the yml files (including the directories) into either 

`~/.local/state/gnuradio`

*or*
	
`/usr/share/gnuradio/grc/blocks`

```bash
cp * ~/.local/state/gnuradio
# OR
cp * /usr/share/gnuradio/grc/blocks
```





