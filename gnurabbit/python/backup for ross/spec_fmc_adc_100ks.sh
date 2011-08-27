
echo "Load kernel module."
insmod gnurabbit/kernel/rawrabbit.ko #vendor=0x10DC device=0x018D

lsmod | grep rawrabbit

sleep 1

echo "Load FPGA bitstream."
gnurabbit/user/fpga_loader_spec_test bitstreams/spec_fmc_adc_100ks.bin

sleep 1

echo "Run Python test program."
cd gnurabbit/python/
./spec_adc_100ks_test.py

