---
layout: post
title: Configure ArchLinux WIFI
---

- [wpa_passphrase](#wpa_passphrase)
- [NetworkManager](#networkmanager)
- [iwctl](#iwctl)

# wpa_passphrase
1. `wpa_passphrase WLAN_NAME WLAN_PASSWORD > /etc/wpa_supplicant.conf`
1. `cat /etc/wpa_supplicant.conf`
{% highlight diff linenos %}
network={
    ssid="WLAN_NAME"
    psk="WLAN_PASSWORD"
    psk=26df252bcd9b7be94233691ee676b581028e34052f13aff3c2a73122be1eea0f
}
{% endhighlight %}
1. `wpa_supplicant`
{% highlight diff linenos %}
Successfully initialized wpa_supplicant
wpa_supplicant v2.10
...
usage:
...
drivers:
nl80211 = Linux nl80211/cfg80211
wext = Linux wireless extensions (generic)
wired = Wired Ethernet driver
macsec_linux = MACsec Ethernet driver for Linux
none = no driver (RADIUS server/WPS ER)
options:
...
{% endhighlight %}
1. `wpa_supplicant -B -i wlp3s0 -c /etc/wpa_supplicant.conf -D wext`
1. `dhclient eth0` or `dhcpcd eth0`

# NetworkManager
`pacman -S networkmanager`

# iwctl
`pacman -S iwd`
1. `dhclient eth0` or `dhcpcd eth0`