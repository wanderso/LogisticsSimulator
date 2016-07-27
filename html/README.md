# svg_demo

Simple demonstration of using Snap.svg library in a test environment.
It is also a simple example for how to use Bower.

SVG + Javascript + HTML + CSS + Python

This was created to make a minimal example for making a web page with CSS that also uses Snap.

A small python web server is also included.
This project can be tested without Python, though. 
Just point a web browser at the file eyes_example.html.

This repo can be installed with bower, or downloaded with git.

## Git
```bash
git clone "https://github.com/tomacorp/svg_demo.git"
```

On OS X, this is an easy way to open the web page:
```bash
cd svg_demo
open eyes_example.html
```
Otherwise, open the file with the web browser.

There is also a small web server. Requires python and Flask.
```bash
python server.py
```
This opens a web server on localhost port 8003:
http://localhost:8003/

## Bower
```bash
bower install svg_demo
```
This installs things in ```bower_components```, with ```svg_demo```
alongside Snap.svg.

The Bower configuration file lists Snap as a dependency.
It is downloaded automatically as part of the svg_demo installation.
However, the ```eyes_example.html``` test page uses a CDN
to get Snap.

The Python is in ```bower_components/server.py```
and it does not know where to find Snap locally, which is in ```../Snap.svg/dist/snap.svg.js```. If I figure out a way to
configure this better, the CDN will no longer be required.

Since Bower is really the node.js package manager, and I am using
Python instead of Node, it should be no surprise that adjustments
are needed! This is a work in progress. If I learn more about this
topic, it will appear here.

More later!
