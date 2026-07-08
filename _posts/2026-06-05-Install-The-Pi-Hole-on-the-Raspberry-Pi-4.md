---
layout: post
title: Install The Pi-Hole on the Raspberry Pi 4
---

# Index

1. Install a supported operating system
Raspberry PI OS
1. Install Pi-Hole
{% highlight diff linenos %}
curl -sSL https://install.pi-hole.net | bash
{% endhighlight %}
1. Use Pi-hole as your DNS server

>Add DNS
{:.filename}
{% highlight diff linenos %}
sudo nmcli con mod CONNECTION-NAME +ipv4.dns "PI-HOLE-PIV4"
{% endhighlight %}

>Remove other DNS, for example ATT
{:.filename}
{% highlight diff linenos %}
nmcli device modify NIC ipv4.ignore-auto-dns yes
{% endhighlight %}

>Restart NetworkManager
{:.filename}
{% highlight diff linenos %}
sudo systemctl restart NetworkManager
{% endhighlight %}