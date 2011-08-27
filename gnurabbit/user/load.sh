#!/bin/bash

cat pfc_top.bin | ./gnurabbit/user/flip > /lib/firmware/pfc_top_flipped.bin
#rmmod rawrabbit
insmod gnurabbit/kernel/rawrabbit.ko  
