#!/bin/bash

param=$1

case "$param" in
    "-t")
        python3 ./src/terminal.py
        ;;
    "-w")
        python3 ./src/web.py
        ;;
    "")
        printf 'Error: no parameter given.\n'
        exit 1
        ;;
    *)
        printf 'Error: invalid parameter.\n'
        exit 1
        ;;
esac
