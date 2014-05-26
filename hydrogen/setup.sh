#!/bin/sh
path=$(pwd)
mkdir $path"/log"
touch $path"/log/out.log"
touch $path"/log/in.log"
touch $path"/log/err.log"
touch $path"/log/boot.log"
bootlog=$path"/log/boot.log" 
sed -i "/cd/c\cd $path" alligator_server.sh
file_path=$path"/alligator_server.sh"
echo $file_path
is_auto_run=$(sed -n '/alligator_server.sh/p' /etc/init.d/rc.local)
echo "start"
echo $is_auto_run
echo "end"
if [ "$is_auto_run" ]
then 
	exit 1
else
	echo $file_path" >> $bootlog 2>&1">>/etc/init.d/rc.local
fi
