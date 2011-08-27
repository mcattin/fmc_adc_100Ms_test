#ifndef __FPGA_REGS_H
#define __FPGA_REGS_H

#define BASE_DMA_CSR 0x0
#define BASE_ADC_CORE_CSR 0x90000

#define DMA_CTL  0x00
#define DMA_CTL_START (1<<0)

#define DMA_STA  0x04
#define DMA_STA_IDLE 0x0
#define DMA_STA_DONE 0x1
#define DMA_STA_BUSY 0x2
#define DMA_STA_ERROR 0x3
#define DMA_STA_ABORTED 0x4
#define DMA_CARRIER_START_ADDR  0x08
#define DMA_HOST_START_ADDR_L  0x0C
#define DMA_HOST_START_ADDR_H  0x10
#define DMA_LENGTH  0x14
#define DMA_NEXT_ITEM_ADDR_L  0x18
#define DMA_NEXT_ITEM_ADDR_H  0x1C
#define DMA_ATTRIB  0x20
#define DMA_ATTRIB_DIR (1<<1)
#define DMA_ATTRIB_NOT_LAST (1<<0)

#define CTL  0x00
#define STA  0x04
#define TRIG_CFG  0x08
#define TRIG_DLY  0x0C
#define SW_TRIG  0x10
#define SHOTS  0x14
#define TRIG_UTC_L  0x18
#define TRIG_UTC_H  0x1C
#define START_UTC_L  0x20
#define START_UTC_H  0x24
#define STOP_UTC_L  0x28
#define STOP_UTC_H  0x2C
#define SRATE  0x30
#define PRE_SAMPLES  0x34
#define POST_SAMPLES  0x38
#define SAMP_CNT  0x3C
#define CH1_SSR  0x40
#define CH1_VALUE  0x44
#define CH2_SSR  0x48
#define CH2_VALUE  0x4C
#define CH3_SSR  0x50
#define CH3_VALUE  0x54
#define CH4_SSR  0x58
#define CH4_VALUE  0x5C

#define FSM_CMD_START  0x1
#define FSM_CMD_STOP  0x2

#define FSM_MASK  0x7
#define FSM_IDLE  0x1
#define FSM_PRE_TRIG  0x2
#define FSM_WAIT_TRIG  0x3
#define FSM_POST_TRIG  0x4
#define FSM_DECR_SHOT  0x5


#endif

