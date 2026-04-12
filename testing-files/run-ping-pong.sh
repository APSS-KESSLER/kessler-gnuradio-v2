#!/usr/bin/env bash

python ./ping-pong.py --tx-port 2000 --rx-port 2004 --send &
python ./ping-pong.py --tx-port 2003 --rx-port 2001 &

wait