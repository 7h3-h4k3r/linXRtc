PORT="7878"

if [[ -z  $1 ]];then
    echo "scanning... port is missing so i take a default port"
else
    PORT=$1

fi

echo "checking the port ${PORT}...."

PID=$(lsof -t -i :"${PORT}")

if [[ -n "$PID" ]];then
    echo "Found process ${PID} on port ${PORT}. Killing it ..."
    kill -9 "$PID"
else
    echo "Port is already free"
fi