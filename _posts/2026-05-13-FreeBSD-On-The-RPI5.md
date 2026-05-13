---
layout: post
title: FreeBSD On The RPI5
---

- [Install FreeBSD](#install-freebsd)
    - [Configure](#configure)
        - [Default login](#default-login)
        - [Network](#network)
        - [Creating a New User](#creating-a-new-user)
        - [Configuring System Services](#configuring-system-services)
        - [Enabling sudo](#enabling-sudo)
        - [Basic Packages](#basic-packages)
            - [fastfetch](#fastfetch)
- [Basic FreeBSD](#basic-freebsd)
    - [Disks](#disks)
        - [View Disks](#view-disks)
        - [Mount Disks](#mount-disks)

# Install FreeBSD
1. Download a FreeBSD RPI image for Raspberry Pi.
    - [FreeBSD RPI 15.0 IMG](https://download.freebsd.org/releases/arm64/aarch64/ISO-IMAGES/15.0/FreeBSD-15.0-RELEASE-arm64-aarch64-RPI.img.xz)
1. Uncompress the image file, `xz -d`
1. Copy the image to the microSD card, `dd`
1. Download the [RPI5_D0.zip](https://github.com/NumberOneGit/rpi5-uefi/releases/download/v0.1/RPI5_D0.zip) file
1. Uncompress the zip file, `unzip RPI5_D0.zip -d RPI5_D0`
{% highlight diff linenos %}
bcm2712d0-rpi-5-b.dtb
bcm2712-d-rpi-5-b.dtb
bcm2712-rpi-500.dtb
bcm2712-rpi-5-b.dtb
bcm2712-rpi-cm5-cm4io.dtb
bcm2712-rpi-cm5-cm5io.dtb
bcm2712-rpi-cm5l-cm4io.dtb
bcm2712-rpi-cm5l-cm5io.dtb
config.txt
overlays
    bcm2712d0.dtbo
RPI_EFI.fd
{% endhighlight %}
1. Copy the unzipped contents to the root of the microsd card.
1. Turn on the Raspberry Pi

## Configure
### Default login
{% highlight diff linenos %}
+user: root
+Password: root
{% endhighlight %}
### Network
[USB -> Ethernet](https://www.walmart.com/ip/StarTech-USB31000S2H-Gigabit-Ethernet-Card/47739371)

### Creating a New User
`adduser`

Add the user to the wheel group for administrative privileges

`pw usermod [USERNAME] -G wheel`

### Configuring System Services
{% highlight diff linenos %}
ee /etc/rc.conf
{% endhighlight %}

{% highlight diff linenos %}
ntpd_enable="YES"
ntpd_sync_on_start="YES"
{% endhighlight %}

{% highlight diff linenos %}
service ntpd enable
{% endhighlight %}
{% highlight diff linenos %}
service ntpd start
{% endhighlight %}

### Enabling sudo
1. `pkg install sudo`
1. `visudo`

### Basic Packages
{% highlight diff linenos %}
pkg install vim fish fastfetch e2fsprogs
{% endhighlight %}
#### fastfetch
##### fish
>~/.config/fish/config.fish
{:.filename}
{% highlight diff linenos %}
fastfetch
{% endhighlight %}

# Basic FreeBSD
## Disks
### View Disks
{% highlight diff linenos %}
geom
{% endhighlight %}
### Mount Disks
Find the drive, `nda*`, `da*`, etc.
{% highlight diff linenos %}
dmesg

dmesg | grep nda0
{% endhighlight %}
Check file system type, `ufs`, `ext4`, `fat32`, etc.
{% highlight diff linenos %}
gpart show

gpart show nda0
{% endhighlight %}
{% highlight diff linenos %}
fstyp /dev/ndap1

fstyp /dev/da0s1
{% endhighlight %}
Mount the drive
{% highlight diff linenos %}
mount -t ext4fs /dev/nda0 /mnt
{% endhighlight %}