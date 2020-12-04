#!/bin/bash

# Platform init script for Target TG48M-P

# Load required kernel-mode drivers
load_kernel_drivers() {
    # Remove modules loaded during Linux init
    # FIX-ME: This will be removed in the future when Linux init no longer loads these
    rmmod i2c_mux_gpio
    rmmod i2c_dev
    rmmod i2c_mv64xxx

    # Carefully control the load order here to ensure consistent i2c bus numbering
    modprobe i2c_mv64xxx
    modprobe i2c_dev
    modprobe i2c_mux_gpio
    modprobe eeprom
}


target_tg48m-p_profile()
{
    MAC_ADDR=$(sudo decode-syseeprom -m)
    sed -i "s/switchMacAddress=.*/switchMacAddress=$MAC_ADDR/g" /usr/share/sonic/device/arm64-target_tg48m-p_52x-r0/tg48m-p/profile.ini
    echo "Target-tg48m-p: Updating switch mac address ${MAC_ADDR}"
}

# - Main entry

# Install kernel drivers required for i2c bus access
load_kernel_drivers

# LOGIC to enumerate SFP eeprom devices - send 0x50 to kernel i2c driver - initialize devices
# the mux may be enumerated at number 4 or 5 so we check for the mux and skip if needed

# Get list of the mux channels
ismux_bus=$(i2cdetect -l|grep mux|cut -f1)

# Enumerate the SFP eeprom device on each mux channel
for mux in ${ismux_bus}
do
    echo optoe2 0x50 > /sys/class/i2c-adapter/${mux}/new_device
done

# Enumerate system eeprom
echo 24c02 0x57 > /sys/class/i2c-adapter/i2c-0/new_device
sleep 2
chmod 644 /sys/class/i2c-adapter/i2c-0/0-0057/eeprom

# Enumerate fan eeprom devices
echo eeprom 0x54 > /sys/class/i2c-adapter/i2c-0/new_device
echo eeprom 0x55 > /sys/class/i2c-adapter/i2c-0/new_device
echo eeprom 0x56 > /sys/class/i2c-adapter/i2c-0/new_device

# Enumerate psu eeprom devices
echo eeprom 0x5b > /sys/class/i2c-adapter/i2c-0/new_device
echo eeprom 0x5a > /sys/class/i2c-adapter/i2c-0/new_device

# Enable optical SFP Tx
i2cset -y -m 0x0f 0 0x41 0x31 0x00

# Ensure switch is programmed with chassis base MAC addr
target_tg48m-p_profile

echo "Target-tg48m-p - completed platform init script"
exit 0
