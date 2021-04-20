icons
=====

The icons project is used to create images from PIL for things like route labels on a map.


install:
  1. install python 3.7 (works with py versions >= 2.7), zc.buildout and git
  1. install freetype and jpeg native libs 
    - MAC: brew install freetype libjpeg libpng
    - UNIX: yum install freetype-devel libjpeg-devel libpng-devel
  1. git clone https://github.com/OpenTransitTools/icons.git
  1. cd icons
  1. buildout

run:
  1. bin/one_label
