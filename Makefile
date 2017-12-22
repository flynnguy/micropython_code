ESP_PORT ?= '/dev/tty.SLAB_USBtoUART'
ESP_BAUD ?= 115200
ESP_FIRMWARE ?= './esp8266-20171101-v1.9.3.bin'

.PHONY: download
download:
	open 'https://micropython.org/download#esp8266'

.PHONY: flash_esp8266
flash_esp8266:
	esptool.py --port ${ESP_PORT} erase_flash
	esptool.py --port ${ESP_PORT} --baud ${ESP_BAUD} write_flash --flash_size=detect 0 ${ESP_FIRMWARE}
