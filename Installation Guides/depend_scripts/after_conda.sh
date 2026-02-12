#!/bin/bash
conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install gnuradio gnuradio-satellites rtl-sdr soapysdr-module-rtlsdr 
#HackRF 
conda install hackrf soapysdr-module-hackrf

