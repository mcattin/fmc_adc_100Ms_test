# Gnuplot script file for plotting data in file "adc_acq.txt"
set   autoscale                        # scale axes automatically
unset log                              # remove any log-scaling
unset label                            # remove any previous labels
set title "Adc-Fmc-100ks"
set xlabel "Sample number"
set ylabel "ADC raw data"
set yrange [-33000:33000]
#plot "adc_100k_acq.txt" using 1:2 title "Channel 1" with lines, "adc_100k_acq.txt" using 1:3 title "Channel 2" with lines, \
#"adc_100k_acq.txt" using 1:4 title "Channel 3" with lines, "adc_100k_acq.txt" using 1:5 title "Channel 4" with lines, \
#"adc_100k_acq.txt" using 1:6 title "Channel 5" with lines, "adc_100k_acq.txt" using 1:7 title "Channel 6" with lines, \
#"adc_100k_acq.txt" using 1:8 title "Channel 7" with lines, "adc_100k_acq.txt" using 1:9 title "Channel 8" with lines, \
#"adc_100k_acq.txt" using 1:10 title "Channel 9" with lines, "adc_100k_acq.txt" using 1:11 title "Channel 10" with lines, \
#"adc_100k_acq.txt" using 1:12 title "Channel 11" with lines, "adc_100k_acq.txt" using 1:13 title "Channel 12" with lines, \
#"adc_100k_acq.txt" using 1:14 title "Channel 13" with lines, "adc_100k_acq.txt" using 1:15 title "Channel 14" with lines, \
#"adc_100k_acq.txt" using 1:16 title "Channel 15" with lines, "adc_100k_acq.txt" using 1:17 title "Channel 16" with lines
plot "adc_100k_acq.txt" using 1:2 title "Channel" with lines
pause -1 "Hit return to continue"
