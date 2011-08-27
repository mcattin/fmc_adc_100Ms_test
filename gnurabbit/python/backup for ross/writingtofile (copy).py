class Plot_options:
    def __init__(self,numero):
        self.title=raw_input("Enter your Plot title : ")
        self.xlabel=raw_input("Enter the label for your X-Axis : ")
        self.ylabel=raw_input("Enter the label for your Y-Axis : ")
        self.numero=numero
    def area(self):
        return self.numero * 2


def file_write(num_plots,array):
    anotherarray=["Default Settings","New Settings"]
    settings=simple_menu(anotherarray,"\nGNUPLOT OPTIONS")

    if settings==1:
##        simple_menu(gnuplot_options,"GNUPLOT OPTIONS")
        options=["dots","lines","curves"]
        graph_style=simple_menu(options,"Select plot style")
        style=options[graph_style-1]
        filename_choice=simple_menu(["Write to file \"adc_fmc_100k_acq.plot\"","write to a different file"],"Choose write file")
        if filename_choice==1:
            filename="adc_fmc_100k_acq.plot"
        elif filename_choice==2:
            filename=str(raw_input("\n\nGive the name of the file you wish to write to, ending in .plot \n\n"))
        file=open(filename,'w')
        file.write("# Gnuplot script file for plotting data in file \"adc_acq.txt\" \n\n") 
        file.write("set   autoscale                         # scale axes automatically \n")
        file.write("unset log                               # remove any log-scaling \n")
        file.write("unset label                             # remove any previous labels \n")
        file.write("set title \"Adc-Fmc-100ks\" \n") 
        file.write("set xlabel \"Sample number\" \n")
        file.write("set ylabel \"ADC raw data\" \n\n")
        file.write("Plot ")

        
    elif settings==2:
        plotinfo=Plot_options(2)
        options=["dots","lines","curves"]
        graph_style=simple_menu(options,"Select plot style")
        style=options[graph_style-1]
        filename_choice=simple_menu(["Write to file \"adc_fmc_100k_acq.plot\"","write to a different file"],"Choose write file")
        if filename_choice==1:
            filename="adc_fmc_100k_acq.plot"
        elif filename_choice==2:
            filename=str(raw_input("\n\nGive the name of the file you wish to write to, ending in .plot \n\n"))
        file=open(filename,'w')
        file.write("# Gnuplot script file for plotting data in file \"adc_acq.txt\" \n\n")
        file.write("set   autoscale                         # scale axes automatically \n")
        file.write("unset log                               # remove any log-scaling \n")
        file.write("unset label                             # remove any previous labels \n")
        file.write("set title \"%s\" \n" %(plotinfo.title)     )
        file.write("set xlabel \"%s\" \n" %(plotinfo.xlabel)   )
        file.write("set ylabel \"%s\" \n\n" %(plotinfo.ylabel) )
        file.write("plot ")
        
    for i in range(num_plots):
        file.write("\"adc_acq.txt\" using 1:%d title \"Channel %d\" with %s  " %((array[i]+1),array[i],style))
        file.write(",\ \n")
    print "\n\nFile \"%s\" has been written \n\n" % (filename)
    
        
    
def simple_menu(array,Description):
    print Description
    for i in range(len(array)):
        print i+1,")", array[i]
##    print "\n"    
    return int(raw_input("please choose an option : "))


##########################################################################
############################################################ THE BEGINNING

array=[]
num_of_channels=16

channel_selections=["All Channels","First ADC chip","Second ADC chip","Custom"]
print "\nCREATING THE PLOT FILE.....\n"

channel_choice=simple_menu(channel_selections,"Choose which channels to Plot")

if channel_choice==1:
    for chans in range(num_of_channels):
        array.append(chans+1)
    k=num_of_channels
    
if channel_choice==2:
    for chans in range(0,num_of_channels/2,1):
        array.append(chans+1)
    k=num_of_channels/2
    
if channel_choice==3:
    for chans in range(num_of_channels/2,num_of_channels,1):
        array.append(chans+1)
    k=num_of_channels/2
    
if channel_choice==4:
    k=int(raw_input("How many ADC channels do you wish to plot? "))
    print "Select which channels you want to plot"
    for h in range(k):
        array.append(int(raw_input("choice %d :" %(h+1))))
   
print array
file_write(k,array)

