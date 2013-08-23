#!/bin/bash

while true ; do
	sleep 1;
	if [ /tmp/fxsdk-updated -nt /tmp/fxsdk-rebuilt ] ; then
		echo "Rebuilding."
		cd ~/shared/cp-program/fxsdk
		git pull
		cd build
		cmake ..
		make
		touch /tmp/fxsdk-rebuilt
	fi
done
