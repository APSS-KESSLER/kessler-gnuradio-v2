#!/usr/bin/env bash

# Only using the populer distrobutions
# If you are not using any of these, then you are smart enough to get these dependancies. 
readonly arch="Arch Linux"
readonly fedora="Fedora"
readonly debian="Debian"
readonly ubuntu="Ubuntu"

readonly os_name=$(cat /etc/os-release | grep -w NAME= | awk -F'"' '{print $2}')

if [$? -ne 0]; then
    echo "Unexpected error, exiting..."
    exit 1
fi

if [[ $os_name == $arch ]]; then
    while true; do
        read -p "This will install system wide python packages, do you want to continue? [yN]"
        case "$yn" in 
            [Yy]* ) break;;
            * ) echo "Exiting. Use conda install instead"; exit 1;;
        esac
    done
    yay -S python gnuradio gnuradio-companion gnuradio-osmodr soapyrtlsdr gr-sattlies
    if [$? -eq 127]; then 
        echo "yay is not detected, using pacman and makepkg"
        sudo pacman -S python gnuradio gnuradio-companion gnuradio-osmodr soapyrtlsdr git
        if [$? -ne 0]; then
            echo "Failed to install dependancies, exiting"
        fi
        cd ..
        git clone https://aur.archlinux.org/gr-satellites.git
        cd gr-satellites
        makepkg -si
        if [$? -ne 0]; then
            echo "Failed to build, exiting"
            exit 1
        fi
        cd ..
        rm -r gr-satellites
    fi
    if [$? -ne 0]; then
        echo "Failed to install dependancies, exiting"
        exit 1
    fi
fi
echo "All dependancies have been installed :D"
exit 0



