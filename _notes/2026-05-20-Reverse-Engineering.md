---
layout: post
title: Reverse-Engineering
---

# Reverse-Engineering
## Level one | Strings
{% highlight diff linenos %}
xxd /bin/ps
{% endhighlight %}

{% highlight diff linenos %}
strings -n 10 /bin/ps | less
{% endhighlight %}

## Level two | Static analysis
{% highlight diff linenos %}
objdump -d -Mintel ./gatekeeper | less
{% endhighlight %}
### Tools
- <a href="https://hex-rays.com/ida-free">IDA</a>
- <a href="https://github.com/NationalSecurityAgency/ghidra">ghidra</a>

## Level three | Dynamic analysis
- `gdb`, GNU Debugger

## Level four | Symbolic Execution
- `angr`, Python library

## Level five | Finging real bugs in real software
- `binwalk -Me example.bin`