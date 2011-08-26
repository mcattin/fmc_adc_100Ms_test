================================================================================
Directories description
================================================================================

acq/                                   => data acquisitions files (written from the GUI), gnuplot script.
bitstreams/                            => FPGA firmware.
gnurabbit/kernel/                      => PCIe driver.
gnurabbit/kernel/rawrabbit.ko          => kernel module.
gnurabbit/user/                        => User space tools.
gnurabbit/user/rrcmd                   => Simple test program for the PCIe driver.
gnurabbit/user/fpga_loader_spec_test   => Firmware loader for SPEC board.
gnurabbit/python/                      => Python binding for PCIe driver, basic classes, example programs.
gui/                                   => dirty test GUI.
spec_load.sh                           => bash script to:
                                          1) install the driver
                                          2) load the FPGA firmware
                                          3) initialise the board
                                          4) launch the GUI

================================================================================
Tips
================================================================================

To build the driver and test programs run make in /gnurabbit


spec_load.sh script must be run as root.
    sudo ./spec_load.sh

================================================================================
More info
================================================================================
http://www.ohwr.org/projects/fmc-adc-100m14b4cha
http://www.ohwr.org/projects/spec
http://www.ohwr.org/projects/gn4124-core
http://www.ohwr.org/projects/ddr3-sp6-core
http://www.ohwr.org/projects/wishbone-gen
http://www.ohwr.org/projects/hdl-make

or contact: matthieu.cattin
