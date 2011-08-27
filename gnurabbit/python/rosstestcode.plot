# Gnuplot script file for plotting data in file "adc_acq.txt" 

set   autoscale                         # scale axes automatically 
unset log                               # remove any log-scaling 
unset label                             # remove any previous labels 
set title "Adc-Fmc-100ks" 
set xlabel "Sample number" 
set ylabel "ADC raw data" 

plot "adc_100k_acq.txt" using 1:16 title "Channel 15" with lines,\
"adc_100k_acq.txt" using 1:17 title "Channel 16" with lines

pause -1 "Hit return to continue"