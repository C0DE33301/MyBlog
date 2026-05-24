---
layout: post
title: Reverse-Engineering 101
---

- [Reverse Engineering 101](#reverse-engineering-101)
    - [Hello World](#hello-world)

# Reverse Engineering 101
## Hello World
>helloworld.c
{:.filename}
{% highlight c linenos %}
#include <stdio.h>
#include <string.h>

void main() {
    printf("Hello World!\n");
}
{% endhighlight %}

{% highlight diff linenos %}
gcc -o helloworld helloworld.c
{% endhighlight %}

{% highlight diff linenos %}
gdb --nx helloworld.c
{% endhighlight %}