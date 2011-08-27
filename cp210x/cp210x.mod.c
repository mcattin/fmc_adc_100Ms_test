#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
 .name = KBUILD_MODNAME,
 .init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
 .exit = cleanup_module,
#endif
 .arch = MODULE_ARCH_INIT,
};

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0x60d90935, "module_layout" },
	{ 0xfcb3af24, "usb_serial_disconnect" },
	{ 0x573dd323, "usb_serial_probe" },
	{ 0x677bb305, "param_ops_bool" },
	{ 0xf25aaa6e, "usb_deregister" },
	{ 0xecfcdd1, "usb_serial_deregister" },
	{ 0x52bfbc74, "usb_register_driver" },
	{ 0xc95bc554, "usb_serial_register" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0x2f287f0d, "copy_to_user" },
	{ 0x362ef408, "_copy_from_user" },
	{ 0x2e60bace, "memcpy" },
	{ 0xcc6eaf2e, "dev_printk" },
	{ 0x7f23aa9b, "usb_reset_device" },
	{ 0x1ed6ea1d, "usb_serial_generic_open" },
	{ 0x2b42df66, "mutex_unlock" },
	{ 0x90269879, "mutex_lock" },
	{ 0xe7b9b438, "usb_serial_generic_close" },
	{ 0xc44bf172, "tty_encode_baud_rate" },
	{ 0x409873e3, "tty_termios_baud_rate" },
	{ 0xdd8f5b6c, "tty_get_baud_rate" },
	{ 0x50eedeb8, "printk" },
	{ 0x37a0cba, "kfree" },
	{ 0x97b61c1f, "usb_control_msg" },
	{ 0x12da5bb2, "__kmalloc" },
	{ 0xa40055a9, "dev_err" },
	{ 0xb4390f9a, "mcount" },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=usbserial";

MODULE_ALIAS("usb:v045Bp0053d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v0471p066Ad*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v0489pE000d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v0489pE003d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v0745p1000d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v08E6p5501d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v08FDp000Ad*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v0BEDp1100d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v0BEDp1101d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v0FCFp1003d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v0FCFp1004d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v0FCFp1006d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10A6pAA26d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10ABp10C5d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10B5pAC70d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p0F91d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p1101d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p1601d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p800Ad*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p803Bd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8044d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p804Ed*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8053d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8054d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8066d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p806Fd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p807Ad*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p80CAd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p80DDd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p80F6d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8115d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p813Dd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p813Fd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p814Ad*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p814Bd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8156d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p815Ed*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p818Bd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p819Fd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p81A6d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p81ACd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p81ADd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p81C8d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p81E2d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p81E7d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p81E8d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p81F2d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8218d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p822Bd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p826Bd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8293d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p82F9d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8341d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8382d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p83A8d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p83D8d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8411d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8418d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p846Ed*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8477d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p85EAd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p85EBd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8664d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4p8665d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4pEA60d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4pEA61d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4pEA71d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4pF001d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4pF002d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4pF003d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C4pF004d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10C5pEA61d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v10CEpEA6Ad*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v13ADp9999d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v1555p0004d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v166Ap0303d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v16D6p0001d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v16DCp0010d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v16DCp0011d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v16DCp0012d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v16DCp0015d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v17F4pAAAAd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v1843p0200d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v18EFpE00Fd*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v1BE3p07A6d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v413Cp9500d*dc*dsc*dp*ic*isc*ip*");

MODULE_INFO(srcversion, "D0D095EA0A55498AD565D4C");
