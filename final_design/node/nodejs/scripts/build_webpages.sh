#!/bin/bash

# This uses pandoc (pandoc.org) to convert markdown docs into html for
# the web server
#
# this script is the c++ equivelent of:
#  make clean
#  make
#  make install

BASE=/home/pi/github/r2d2
README=${BASE}/readme.md
PICS=${BASE}/pics

echo "*****************************"
echo "* Cleaning out old files    *"
echo "*****************************"

rm -f ../*.html
rm -fr ../pics

echo "*****************************"
echo "* Generating new HTML files *"
echo "*****************************"

pandoc ${README} -o ../index.html
pandoc templates/video.md -o ../video.html
pandoc templates/ee.md -o ../ee.html
pandoc templates/compe.md -o ../compe.html
pandoc templates/department.md -o ../department.html
pandoc templates/error.md -o ../error.html


echo "*****************************"
echo "* Copying website assets    *"
echo "*****************************"

mkdir -p ../pics
cp ${PICS}/* ../pics
# cp pics/* ../pics
cp templates/footer.html ../
cp templates/header.html ../

# a couple odd stray images
# cp ${BASE}/docs/diagrams/PowerSystem.jpg ../pics
# cp ${BASE}/docs/diagrams/ControlsSystem.jpg ../pics
# cp ${BASE}/docs/diagrams/SoftwareFlowChart.jpg ../pics
# cp ${BASE}/docs/diagrams/Power System.jpg ../pics
# cp ${BASE}/docs/diagrams/Power System.jpg ../pics


echo "*****************************"
echo "*          Done             *"
echo "*****************************"
