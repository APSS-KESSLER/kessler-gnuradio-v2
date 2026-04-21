trap "kill 0" SIGINT SIGTERM

python ./async-ping-pong.py --tx-port 2000 --rx-port 2003 --rx-ip "127.0.0.1" --tx-ip "127.0.0.2"