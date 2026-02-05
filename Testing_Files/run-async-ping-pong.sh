python ./zmq-ping-pong.py --tx-port 2000 --rx-port 2001 --tx-ip "127.0.0.2" --send &
python ./zmq-ping-pong.py --tx-port 2002 --rx-port 2003 --rx-ip "127.0.0.1" &

wait