#!/bin/bash

fw_uboot_env_cfg()
{
    echo "Setting up U-Boot environment..."

    MACH_FILE="/host/machine.conf"
    PLATFORM=`sed -n 's/onie_platform=\(.*\)/\1/p' $MACH_FILE`

    if [ "$PLATFORM" = "arm64-target-tg48m-p_52x-r0" ]; then
	# TG48M-P  board Uboot ENV offset
        FW_ENV_DEFAULT='/dev/mtd0 0x00100000 0x10000 0x10000'

        demo_part=$(sgdisk -p /dev/sda | grep -e "SONiC-OS")
        if [ -z "$demo_part" ]; then
            # ET6448M Board - For Backward compatibility
            FW_ENV_DEFAULT='/dev/mtd0 0x00500000 0x80000 0x100000 8'
        fi
    else
        FW_ENV_DEFAULT='/dev/mtd0 0x00500000 0x80000 0x100000 8'
    fi

    echo "Using pre-configured uboot env"
    echo $FW_ENV_DEFAULT > /etc/fw_env.config

}


main()
{
    fw_uboot_env_cfg
    echo "Target-TG48M-P: /dev/mtd0 FW_ENV_DEFAULT"
}

main $@
