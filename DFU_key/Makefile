## required
APP = nrf52832_xxaa.hex
KEY = private.key
BOOT = boot.hex
SOFTDEVICE = s132_nrf52_6.1.0_softdevice.hex

## output
ZIP = ADG725_output.zip
SETTING = app_setting.hex
MERGED = merged.hex

## copy path
COPY_PATH = ..\nRF5_SDK_15.2.0_9412b96\examples\ble_peripheral\ADG725_DFU\pca10040\s132\arm5_no_packs\_build\nrf52832_xxaa.hex

## temp file
TMP = tmp3to1.hex


.PHONY: all clean zip setting merged

all: clean copy zip setting merged

copy:
	copy $(COPY_PATH) .

zip: $(APP) $(KEY)
	nrfutil pkg generate --hw-version 52 --application-version 1 --application $(APP) --sd-req 0xaf --key-file $(KEY) $(ZIP)

setting: $(APP)
	nrfutil settings generate --family NRF52 --application-version 1 --application $(APP) --bootloader-version 1 --bl-settings-version 1 $(SETTING)

merged: $(APP) $(SOFTDEVICE) $(BOOT) $(SETTING)
	mergehex --merge $(SOFTDEVICE) $(BOOT) $(APP) --output $(TMP)
	mergehex --merge $(TMP) $(SETTING) --output $(MERGED)

clean:
	-del $(ZIP) $(SETTING) $(MERGED) $(TMP)

