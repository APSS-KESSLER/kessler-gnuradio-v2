trap "kill 0" SIGINT SIGTERM  # kills all child processes on Ctrl+C
python ./async-ping-pong.py --tx-port 2000 --rx-port 2001 --tx-ip "127.0.0.2" --send&

wait
