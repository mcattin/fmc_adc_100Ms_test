# Gnuplot script file for plotting data in file "adc_acq.txt"
set   autoscale                        # scale axes automatically
unset log                              # remove any log-scaling
unset label                            # remove any previous labels
set title "Adc-Fmc-100Ms14b4cha"
set xlabel "Sample number"
set ylabel "ADC raw data"
plot "adc_acq.txt" using 1:2 title "Channel 1" with lines, "adc_acq.txt" using 1:3 title "Channel 2" with lines, \
"adc_acq.txt" using 1:4 title "Channel 3" with lines, "adc_acq.txt" using 1:5 title "Channel 4" with lines
pause -1 "Hit return to continue"
