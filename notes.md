---
title: /notes
layout: page
permalink: /notes/
---

# My basic notes

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
<br>
<ul>
  {% for note in site.notes %}
    <li>[ {{ note.date | date: "%Y-%m-%d" }} ] <a href="{{ note.url | relative_url }}">{{ note.title | escape }}</a></li>
  {% endfor %}
</ul>