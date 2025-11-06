#!/usr/bin/env bash

# Only using the populer distrobutions
# If you are not using any of these, then you are smart enough to get these dependancies. 
readonly arch="arch"
readonly fedora="fedora"
readonly debian="debian"
readonly ubuntu="ubuntu"

readonly os_name=$(cat /etc/os-release | grep -w ID | awk -F = '{print $2}')

if [ $? -ne 0 ]; then
    echo "Unexpected error, exiting..."
    exit 1
fi

read -r -p "RECOMMENDED: Do you want to use conda [Yn]: " conda
conda=${conda,,}
if [[ "$conda" =~ ^([yes|y])$ ]]; then
    echo "Installing conda"
    if [[ "$(arch)" == "aarch64" ]]; then                                                              
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
        chmod +x ./Miniconda3-latest-Linux-aarch64.sh
        ./Miniconda3-latest-Linux-aarch64.sh
    elif [[ "$(arch)" == "x86_64" ]]; then
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
        chmod +x ./Miniconda3-latest-Linux-x86_64.sh
        ./Miniconda3-latest-Linux-x86_64.sh
    else
        echo "Cannot detect architecture, exiting."
        exit 1
    fi
    echo "Conda is installed"
    echo "Please execute the second script in depend_scripts: after_conda.sh"
    echo "Ensure you execute the following before execution"
    echo "eval \"\$(/home/paul/miniconda3/bin/conda shell.bash hook)\" "
    rm Mini*
    exit 0
fi



echo "Installing via system packages..."

if [[ $os_name == $arch ]]; then
    while true; do
        read -p "(Arch Linux) This will install system wide python packages, do you want to continue? [yN]" yn
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
            exit 1
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
