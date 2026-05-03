---
layout: post
title: Install SyncTERM Linux
---

1. Download <a href="https://sourceforge.net/projects/syncterm/files/latest/download" target="_blank">Here</a>
    - `syncterm-1.8-src.tgz` for example.
1. `sudo apt install wget libncurses5-dev libncursesw5-dev gcc libsdl1.2-dev`
1. `gunzip syncterm-1.8-src.tgz`
1. `cd src/syncterm`
1. `sudo make SRC_ROOT=/home/user/Downloads/syncterm-1.8-src/src`
1. `sudo make install`
1. `which syncterm`, to test the install location.