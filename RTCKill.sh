PORT="7878"

if [[ -z  $1 ]];then
    echo "scanning... port is missing so i take a default port"
else
    PORT=$1

fi

echo "checking the port ${PORT}...."

PIDS=$(lsof -t -i :"${PORT}")

if [[ -n "$PIDS" ]];then
    for PID in $PIDS;do
        echo "Killing PID : $PID"
        kill -9 "$PID"
    done
        
else
    echo "Port is already free"
fi



for i in {1..100};do
    python3 main.py
    if [[ $? -eq 0 ]];then
        echo "Server started successfully"
        break
    else
        echo "Server failed to start, retrying... ($i/100)"
    fi
    sleep 1
done