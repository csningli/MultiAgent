#! /bin/bash

pos="."

if [[ $# -gt 0 ]]; then
	pos=$1
fi

rm $pos/*.data

