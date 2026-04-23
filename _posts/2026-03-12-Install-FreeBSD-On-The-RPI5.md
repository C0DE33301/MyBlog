---
layout: post
---

- [Install FreeBSD](#install-freebsd)
    - [Configure](#configure)
        - [Default login](#default-login)
        - [Network](#network)
        - [Creating a New User](#creating-a-new-user)
        - [Configuring System Services](#configuring-system-services)
        - [Enabling sudo](#enabling-sudo)
        - [fastfetch](#fastfetch)

# Install FreeBSD
1. Download a [FreeBSD](https://www.freebsd.org/where) image for Raspberry Pi
1. Uncompress the image file, `xz -d`
1. Copy the image to the microSD card, `dd`
1. Download the [RPI5_D0.zip](https://github.com/NumberOneGit/rpi5-uefi/releases) file
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
`ee /etc/rc.conf`
{% highlight diff linenos %}
ntpd_enable="YES"
ntpd_sync_on_start="YES"
{% endhighlight %}

### Enabling sudo
1. `pkg install sudo`
1. `visudo`

### fastfetch
fish

`vim .config/fish/config.fish`
{% highlight diff linenos %}
fastfetch
{% endhighlight %}