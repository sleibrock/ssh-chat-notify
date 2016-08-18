function ssh_chat(){
    mkfifo $SSHOME/$1 # create a FIFO tempfile
    trap "rm $SSHOME/$1;exit" SIGTERM SIGHUP SIGINT # clear the FIFO on kill
    cat -u -e $SSHOME/$1 | while read line; do  # read the file in another thread
	if echo "$line" | grep -q '\^G'; then
	    python $SSHOME/notify.py $1 $2 "$line"
        fi
    done &
    ssh -t $1@chat.shazow.net | tee $SSHOME/$1
    rm $SSHOME/$1 # kill the FIFO when done (should kill other threads)
    killall cat # sorry!
    echo "Cleaned up SSH fifo"
}

