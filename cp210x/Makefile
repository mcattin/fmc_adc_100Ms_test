#KERNEL_DIR=/home/mvanga/dev/cern/linux/linux-torvalds
KERNEL_DIR=/lib/modules/`uname -r`/build/

obj-m += cp210x.o

all:
	make -C $(KERNEL_DIR) M=$(PWD) modules
clean:
	make -C $(KERNEL_DIR) M=$(PWD) clean
