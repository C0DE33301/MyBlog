---
layout: post
title: Manually Install Linux
---

# Manually Install Linux
* [Arch Linu](#arch-linux)
    * Connect To The Internet
    * [Partitions](#partitions)
        * [Partition the disks](#partition-the-disks)
        * [EFI System Partition](#efi-system-partition)
        * [Swap Partition](#swap-partition)
        * [Home Partition](#home-partition)
        * [Linux File System](#linux-file-system)
        * [Write To Disk](#write-to-disk)
    * [Format The Partitions](#format-the-partitions)
    * [Install The Arch Base](#install-the-arch-base)
    * [Chroot](#chroot)
    * [Timezone](#timezone)
    * [Localization](#localization)
    * [Hostname & Hosts File](#hostname--hosts-file)
    * [Root User](#root-user)
    * [Normal User](#normal-user)
    * [Give Normal User Root](#give-normal-user-root)
    * [Normal User Home Directory](#normal-user-home-directory)
    * [Create EFI Directory](#create-efi-directory)
    * [Generate The Fstab File](#generate-the-fstab-file)
    * [Modify The Fstab File](#modify-the-fstab-file)
    * [Grub](#grub)
    * [Get Network Manager](#get-network-manager)
    * Temporary Terminal
    * Reboot The System
* [Debian](#debian)
* [openSUSE Leap](#opensuse-leap)

# [Arch Linux](https://archlinux.org/download)
## Connect To The Internet
## Partitions
### Partition the disks
List available block device
{% highlight diff %}
$ fdisk -l
{% endhighlight %}

Modify partition tables
{% highlight diff %}
$ fdisk /dev/main_disk
{% endhighlight %}

Create a new empty GTP partition table
{% highlight diff %}
g
{% endhighlight %}
### EFI System Partition
Add a new partition
{% highlight diff %}
n
{% endhighlight %}

Partition number
{% highlight diff %}
Default NUM, [Enter Key]
{% endhighlight %}

First sector
{% highlight diff %}
Default, [Enter Key]
{% endhighlight %}

Last sector
{% highlight diff %}
+500M
{% endhighlight %}

Change partition type
{% highlight diff %}
t
{% endhighlight %}

Partition number
{% highlight diff %}
EFI_NUM
{% endhighlight %}

Partition type of alias
{% highlight diff %}
1
{% endhighlight %}

### Swap Partition
Add a new partition
{% highlight diff %}
n
{% endhighlight %}

Partition number
{% highlight diff %}
Default Num, [Enter Key]
{% endhighlight %}

First sector
{% highlight diff %}
Default, [Enter Key]
{% endhighlight %}

Last sector
{% highlight diff %}
+3G
{% endhighlight %}

Change partition type
{% highlight diff %}
t
{% endhighlight %}

Partition number
{% highlight diff %}
SWAP_NUMBER
{% endhighlight %}

Partition type of alias
{% highlight diff %}
19
{% endhighlight %}

### Home Partition
Add a new partition
{% highlight diff %}
n
{% endhighlight %}

Partition number
{% highlight diff %}
Default NUM, [Enter Key]
{% endhighlight %}

First Sector
{% highlight diff %}
Default [Enter]
{% endhighlight %}

Last Sector
{% highlight diff %}
+100G
{% endhighlight %}

### Linux File System
Add a new partition
{% highlight diff %}
n
{% endhighlight %}

Partition number
{% highlight diff %}
Default NUM, [Enter Key]
{% endhighlight %}

First Sector
{% highlight diff %}
Default [Enter]
{% endhighlight %}

Last Sector
{% highlight diff %}
+100G
{% endhighlight %}

### Write To Disk
Write table to disk & exit
{% highlight diff %}
w
{% endhighlight %}

## Format The Partitions
EFI System
{% highlight diff %}
mkfs.fat -F 32 /dev/efi_part
{% endhighlight %}

EXT4 Linux File System
{% highlight diff %}
mkfs.ext4 /dev/file_system_part
{% endhighlight %}

EXT4 Home
{% highlight diff %}
mkfs.ext4 /dev/home_part
{% endhighlight %}

## Install The Arch Base
Install pacstrap
{% highlight diff %}
packman -S arch-install-scripts
{% endhighlight %}

Mount Linux File System
{% highlight diff %}
mount /dev/linux-file-system /mnt
{% endhighlight %}

Install essential packages
{% highlight diff %}
pacstrap -k /mnt base linux linux-firmware
{% endhighlight %}

## Chroot
{% highlight diff %}
arch-chroot /mnt
{% endhighlight %}

## Timezone
Set timezone
{% highlight diff %}
ln -sf /usr/share/zoneinfo/America/Chicago /etc/localtime
{% endhighlight %}

Generate /etc/adjtime
{% highlight diff %}
hwclock --systohc
{% endhighlight %}

## Localization
Edit /etc/localegen file
{% highlight diff %}
nano /etc/localegen
{% endhighlight %}

Uncomment
{% highlight diff %}
#en_US.UTF-8 UTF-8
{% endhighlight %}

Generate the locales
{% highlight diff %}
locale-gen
{% endhighlight %}

## Hostname & Hosts File
Edit hostname file
{% highlight diff %}
nano /etc/hostname

USERNAME
{% endhighlight %}

Edit hosts file
{% highlight diff %}
nano /etc/hosts

127.0.0.1   localhost
::1         localhost
127.0.1.1   USERNAME.localdomain    USERNAME
{% endhighlight %}

## Root User
Create root password
{% highlight diff %}
passwd
{% endhighlight %}

## Normal User
Create normal user
{% highlight diff %}
useradd USER
{% endhighlight %}

Create password for normal user
{% highlight diff %}
passwd USER
{% endhighlight %}

## Give Normal User Root
{% highlight diff %}
visudo

#%wheel ALL=(ALL:ALL)ALL
{% endhighlight %}

## Normal User Home Directory
Mount /home
{% highlight diff %}
mount /dev/home_part /home
{% endhighlight %}

Create normal user home dir
{% highlight diff %}
mkdir /home/USER
{% endhighlight %}

Chown normal user home dir
{% highlight diff %}
chown USER:USER /home/USER
{% endhighlight %}

## Create EFI Directory
{% highlight diff %}
mkdir /boot/efi
{% endhighlight %}

Mount EFI partition
{% highlight diff %}
mount /dev/efi_part /boot/efi
{% endhighlight %}

## Generate The Fstab File
Fstab generate fstab file
{% highlight diff %}
genfstab -U /mnt >> /mnt/etc/fstab
{% endhighlight %}

## Modify The Fstab File
Get /home UUID partition
{% highlight diff %}
blkid /dev/home_part
{% endhighlight %}

Modify fstab file /home
{% highlight diff %}
nano /etc/fstab

UUID=UUID   /home   ext4    dafaults    0   2
{% endhighlight %}

## Grub
Install packages
{% highlight diff %}
pacman -S efibootmgr dosfstools os-prober mtools grub
{% endhighlight %}

Edit grub
{% highlight diff %}
nano /etc/dafult/grub

#GRUB_DISABLE_OS_PROBER=false
{% endhighlight %}

{% highlight diff %}
grub-install --target=x86_64-ef --bootloader_id=ARCH --recheck
{% endhighlight %}

## Get Network Manager
{% highlight diff %}
pacman -S networkmanager
{% endhighlight %}

Enable NetworkManager
{% highlight diff %}
systemctl enable NetworkManager
{% endhighlight %}

## Temporary Terminal
## Reboot The System

# Debian
# openSUSE Leap