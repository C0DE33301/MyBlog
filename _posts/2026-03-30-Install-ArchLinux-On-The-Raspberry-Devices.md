---
layout: post
title: Install ArchLinux On The Raspberry Devices
---

- [Raspberry pi 5](#raspberry-pi-5)
- [Raspberry pi zero 2 w](#raspberry-pi-zero-2-w)

# Raspberry pi 5
1. Download a [Arch Linux](http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-aarch64-latest.tar.gz) image for Raspberry Pi
1. Plug SD card into a machine running aarch64 Arch Linux Arm.
1. `fdisk /dev/sdx`
    1. Type `g` to create a new gpt partition table.
    1. Crate the **EFI System** partition
        1. Type `n` to create a new partition.
        1. Press `Enter` to accept the partition number `1`.
        1. Type `65536` 32MiB, first sector
        1. Type `+256M`, last sector.
        1. Type `t` to set the partition type
        1. Type `1` to set the partition type to **EFI System**
    1. Crate the **Linux filesystem** partition
        1. Type `n` to create a new partition.
        1. Press `Enter` to accept the partition number `2`.
        1. Type `Enter` to accept the default first sector.
        1. Type `Enter` to accept the default last sector.
    1. Type `w` to write the changes to the card.
1. format our new partitions

# Raspberry pi zero 2 w
1. Partition the SD card, `fdisk /dev/sdX`
    - **Create W95 FAT32 (LBA) partition**
        - `n`, create partition
        - `p`, primary
        - `1`, first partition
        - `ENTER`, to accept the default first sector
        - `+1G`, the last sector
        - `t`
        - `c` partition to type W95 FAT32 (LBA).
    - **Create Linux partition**
        - `n`, create partition
        - `p`, primary
        - `2`, second partition
        - `ENTER` twice to accept the default first and last sector.
    - `w`, Write the partition table and exit.
1. FAT filesystem
    - `mkfs.vfat /dev/sdX1`
    - `mkdir /mnt/boot`
    - `mount /dev/sdX1 /mnt/boot`
1. ext4 filesystem
    - `mkfs.ext4 /dev/sdX2`
    - `mkdir /mnt/root`
    - `mount /dev/sdX2 /mnt/root`
1. Download
    - `curl -OL http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-armv7-latest.tar.gz`
    - `bsdtar -xpf ArchLinuxARM-rpi-armv7-latest.tar.gz -C /mnt/root`
1. The boot files
    - `mv /mnt/root/boot/* /mnt/boot`
1. Unmount the two partitions
    - `umount /mnt/boot /mnt/root`