---
layout: post
title: Arch Linux
---

# Index
- [Raspberry pi 5](#raspberry-pi-5)
- [Raspberry pi zero 2 w](#raspberry-pi-zero-2-w)
- [Basic set up](#basic-set-up)
- [Offline Installation](#offline-installation)
- [Online Installation](#online-install)
- [Configure](#configure)

# Raspberry pi 5
1. Download the <a href="http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-aarch64-latest.tar.gz" target="_blank">ArchLinux RPI</a>
1. Plug SD card into a machine running aarch64 Arch Linux Arm.
1. Partition the SD card, `fdisk /dev/sdx`
    1. Type `g` to create a new gpt partition table.
    1. Crate the **EFI System** partition
        1. Type `n` to create a new partition.
        1. Press `Enter` to accept the partition number `1`.
        1. Press `Enter`, first sector
        1. Type `+256M`, last sector.
        1. Type `t` to set the partition type
        1. Type `1` to set the partition type to **EFI System**
    1. Crate the **Linux filesystem** partition
        1. Type `n` to create a new partition.
        1. Press `Enter` to accept the partition number `2`.
        1. Type `Enter` to accept the default first sector.
        1. Type `Enter` to accept the default last sector.
    1. Type `w` to write the changes to the card.
1. [Format the partitions](#format-the-partitions)
1. `bsdtar -xpfv ArchLinuxARM-rpi-aarch64-latest.tar.gz -C /mnt/root`
1. [Finishing](#finishing)

# Raspberry pi zero 2 w
1. Download the <a href="http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-armv7-latest.tar.gz" target="_blank">ArchLinux RPI</a>
1. Plug SD card into a machine running aarch64 Arch Linux Arm.
1. Partition the SD card, `fdisk /dev/sdX`
    1. **Create W95 FAT32 (LBA) partition**
        - `n`, create partition
        - `p`, primary
        - `1`, first partition
        - `ENTER`, to accept the default first sector
        - `+1G`, the last sector
        - `t`
        - `c` partition to type W95 FAT32 (LBA).
    1. **Create Linux partition**
        - `n`, create partition
        - `p`, primary
        - `2`, second partition
        - `ENTER` twice to accept the default first and last sector.
    1. `w`, Write the partition table and exit.
1. [Format the partitions](#format-the-partitions)
1. `bsdtar -vxpf ArchLinuxARM-rpi-armv7-latest.tar.gz -C /mnt/root`
1. [Finishing](#finishing)

# Basic set up
## Format the partitions
1. FAT filesystem
    - `mkfs.vfat /dev/sdX1`
    - `mkdir /mnt/boot`
    - `mount /dev/sdX1 /mnt/boot`
1. ext4 filesystem
    - `mkfs.ext4 /dev/sdX2`
    - `mkdir /mnt/root`
    - `mount /dev/sdX2 /mnt/root`

## Finishing
1. Move the boot files
    - `mv -v /mnt/root/boot/* /mnt/boot`
1. Unmount the two partitions
    - `umount /mnt/boot /mnt/root`

# Offline Installation
## Create local repository
### Pick specific packages
Only install needed packages. For this part the internet is required, use a separate computer to install the packages with internet connection.

|Type|Package name|
|---|---|
|**Main packages (required)**|`base`, `linux`, `linux-firmware`, `archlinux-keyring`|
|**Authority (required)**|`sudo`<br>------------------------------------------------------------------------------------------------------------------------------------------------------<br>`doas`|
|**Display Server (required)**|**XOrg**<br>`xorg-server` `xorg-apps` `xorg-xinit`<br>------------------------------------------------------------------------------------------------------------------------------------------------------<br>**Wayland**<br>|
|**Graphics Driver (required)**|**VGA Compatible Controller**: `xf86-video-ati`|
|**Display Manager (required)**|**LightDM**<br>`lightdm`, `lightdm-THEME_NAME-greeter`<br><br>**lightdm-THEME_NAME-greeter**<br>`lightdm-gtk-greeter`<br>`lightdm-pantheon-greeter`<br>`lightdm-slick-greeter`<br>`lightdm-webkit2-greeter`<br>`lightdm-webkit-theme-litarvan`<br>------------------------------------------------------------------------------------------------------------------------------------------------------<br>**LY**<br>`ly`|
|**Boot loader (required)**|**GRand Unified Bootloader** <br>`grub`|
|**Boot Manager (optional)**|`efibootmgr`|
|**Microcode (optional)**|**AMD**: `amd-ucode`<br> **Intel**: `intel-ucode`|
|**Network CLI (required)**|`networkmanager`|
|**System Information (optional)**|`fastfetch`|

{% highlight diff %}
pacman -Syw --cachedir /MAIN-LOCAL-REPO-DRIVE --dbpath /tmp PACKAGE-NAMES
{% endhighlight %}

Create a package database
`repo.db.tar.gz`, `repo` is the name of the repo database.
{% highlight diff %}
repo-add repo.db.tar.gz /path/to/main-local-repo-drive/*.pkg.tar.zst
{% endhighlight %}

## Set font size
List of fonts
{% highlight diff %}
ls /usr/share/kbd/consolefonts
{% endhighlight %}

Set font
{% highlight diff %}
setfont sun12x22
{% endhighlight %}

## Partition the disks
### Create partitions
{% highlight diff %}
fdisk /path/to/chosen/drive
{% endhighlight %}

Create a GPT table
{% highlight diff %}
g
{% endhighlight %}

type `n` to create the following partitions, ...

|Partition Type|partiton number|First Sector|Last Sector|
|---|---|---|---|
|EFI                  |[Enter Key]|[Enter Key]|+550M|
|Linux File System    |[Enter Key]|[Enter Key]|+100G|
|Linux Swap (optional)|[Enter Key]|[Enter Key]|+3G  |
|Home (optional)      |[Enter Key]|[Enter Key]|+100G|
|Repo (optional)      |[Enter Key]|[Enter Key]|+100G|

type `t` to change parition type

|Partiton number|partiton type|
|---|---|
|[efi-partition-number]|1|
|[swap-parition-number] (optional)|19|

type `w` to write to disk.

### Format the partitons
EFI
{% highlight diff %}
mkfs.fat -F 32 /dev/EFI
{% endhighlight %}
Linux FileSystem
{% highlight diff %}
mkfs.btrfs -L MAIN /dev/LinuxFileSystem
{% endhighlight %}
Linux Swap (optional)
{% highlight diff %}
mkswap /dev/Swap
{% endhighlight %}
Home (optional)
{% highlight diff %}
mkfs.ext4 -L HOME /dev/home
{% endhighlight %}
Repo (optional)
{% highlight diff %}
mkfs.ext4 -L REPO /dev/repo
{% endhighlight %}

## Swap
{% highlight diff %}
swapon /dev/swap-part
{% endhighlight %}

## Mount the partitions
Linux File System
{% highlight diff %}
mount /dev/Linux-FileSystem /mnt
{% endhighlight %}

EFI
{% highlight diff %}
mount --mkdir /dev/EFI /mnt/boot/efi
{% endhighlight %}

Repo (optional)
{% highlight diff %}
mount --mkdir /dev/Package-Part /mnt/mnt/repo
{% endhighlight %}

Home
{% highlight diff %}
mount --mkdir /dev/home-Part /mnt/home/USERNAME
{% endhighlight %}

## Configure local repo
### Remove other repo sections
>/etc/pacman.conf
{:.filename}
{% highlight diff linenos %}
#[core]
#...

#[extra]
#...

#[community]
#...
{% endhighlight %}

### Add local repo section
`[repo]` is the name if the repo database.
>/etc/pacman.conf
{:.filename}
{% highlight diff linenos %}
[repo]
SigLevel = Optional TrustedOnly
Server = file:///mnt/mnt/REPO
{% endhighlight %}

### Sync the package database
{% highlight diff %}
pacman -Sy
{% endhighlight %}

### Initializing the pacman keyring
{% highlight diff %}
pacman-key --init
{% endhighlight %}

### Verifying the main keys
{% highlight diff %}
pacman-key --populate
{% endhighlight %}


### Stop the reflector python script
This retrieves the latest mirror list from the Arch Linux Mirror Status page.
{% highlight diff %}
systemctl stop reflector.service
{% endhighlight %}

### Other, ...
pacman -S archlinux-keyring

### Install the packages
{% highlight diff %}
pacstrap /mnt base linux linux-firmware archlinux-keyring xorg-server xorg-apps xorg-xinit xf86-video-ati grub efibootmgr sudo networkmanager vi fastfetch amd-ucode
{% endhighlight %}

### Copy the `/etc/pacman.conf`
{% highlight diff %}
cp /etc/pacman.conf /mnt/etc/pacman.conf
{% endhighlight %}

### Generate mount points
{% highlight diff %}
genfstab -L /mnt > /mnt/etc/fstab
{% endhighlight %}

### Chroot into main mount point
{% highlight diff %}
arch-chroot /mnt
{% endhighlight %}

### Clock
{% highlight diff %}
ln -sf /usr/share/zoneinfo/America/Chicago
{% endhighlight %}

{% highlight diff %}
hwclock --systohc
{% endhighlight %}

{% highlight diff %}
vi /etc/locale.gen
#en_US.UTF-8 UTF-8" >> 
locale-gen
{% endhighlight %}

Other, ...
{% highlight diff %}
echo "LANG=en-US.UTF-8" > /etc/local.conf
{% endhighlight %}

### Enable NetworkManager
{% highlight diff %}
systemctl enable NetworkManager
{% endhighlight %}

### Set root password
{% highlight diff %}
passwd
{% endhighlight %}

### Create a new user & set password
{% highlight diff %}
useradd -mG wheel -s /bin/bash USERNAME
passwd USERNAME
{% endhighlight %}

### Give normal user root permissions
{% highlight diff %}
visudo 
%wheel ALL=(ALL:ALL) ALL
{% endhighlight %}

### Install grub
{% highlight diff %}
grub-install --target=x86_64-efi --efi-directory=/boot/efi
grub-mkconfig -o /boot/grub/grub.cfg
{% endhighlight %}

### Ends
{% highlight diff %}
exit
reboot
{% endhighlight %}

# Online Installation

# Configure
## Display Manager
<table>
    <tr>
        <th>Graphical greeters</th>
        <th>Console</th>
    </tr>
    <tr>
        <th>
            LightDM
            <ul>
                <li>lightdm-gtk-greeter</li>
                <li>lightdm-pantheon-greeter</li>
                <li>lightdm-slick-greeter</li>
                <li>lightdm-webkit2-greeter</li>
            </ul>
        </th>
        <th>
            emptty
            <img src="/assets/img/WM/emptty.png" alt="emptty">
        </th>
    </tr>
    <tr>
        <th></th>
        <th>
            Lemurs
            <img src="/assets/img/WM/Lemurs.png" alt="emptty">
        </th>
    </tr>
    <tr>
        <th></th>
        <th>
            ly
            <img src="/assets/img/WM/ly.png" alt="emptty">
        </th>
    </tr>
</table>

### LightDM
Install packages
{% highlight diff %}
pacman -S lightdm lightdm-THEME_NAME-greeter
{% endhighlight %}

>/etc/lightdm/lightdm.conf
{:.filename}
{% highlight diff linenos %}
[Seat]
...
greeter-session=lightdm-THEM-greeter
...
{% endhighlight %}

{% highlight diff %}
sudo systemctl enable lightdm
{% endhighlight %}

List of available greeters
{% highlight diff %}
ls -l /usr/share/xgreeters
{% endhighlight %}

### Ly
Install packages
{% highlight diff %}
pacman -S ly
{% endhighlight %}

Enable Ly: X, number from 1 to 6.
{% highlight diff %}
ly@ttyX.service
{% endhighlight %}

Disable Ly: X, number from 1 to 6.
{% highlight diff %}
getty@ttyX.service
{% endhighlight %}

## Window Manager
<table>
    <tr>
        <th>Dynamic window managers</th>
        <th>Tiling window managers</th>
        <th>Stacking window managers</th>
    </tr>
    <tr>
        <th>qtile</th>
        <th>i3-wm</th>
        <th>fluxbox</th>
    </tr>
    <tr>
        <th>awesome</th>
        <th>.</th>
        <th>Openbox</th>
    </tr>
    <tr>
        <th>xmonad</th>
        <th>.</th>
        <th>.</th>
    </tr>
</table>

## Terminal
<table>
    <tr>
        <th>Terminal emulators</th>
        <th>VTE-based</th>
    </tr>
    <tr>
        <th>xterm</th>
        <th>.</th>
    </tr>
    <tr>
        <th>.</th>
        <th>.</th>
    </tr>
    <tr>
        <th>.</th>
        <th>.</th>
    </tr>
</table>