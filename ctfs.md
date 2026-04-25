---
title: /ctfs
layout: page
permalink: /ctfs
---

# CTF Writeups

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
<br>
<ul>
  {% for ctf in site.ctfs %}
    <li>[ {{ ctf.date | date: "%Y-%m-%d" }} ] <a href="{{ ctf.url | relative_url }}">{{ ctf.title | escape }}</a></li>
  {% endfor %}
</ul>