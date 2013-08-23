#!/bin/bash

echo $0
touch /tmp/war-date
while true ; do
	sleep 1;
	if [ /tmp/fxsdk-updated -nt /tmp/fxsdk-rebuilt ] ; then
		( # New scope (so we automatically go back to the old wd afterwards)
		echo "Rebuilding."
		cd ~/shared/cp-program/fxsdk
		git pull
		cd build
		cmake ..
		make
		touch /tmp/fxsdk-rebuilt
		)
	fi
	if [ "$0" -nt /tmp/war-date ] ; then
		exec $0 # Basically, reload the script
	fi
done
