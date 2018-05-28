#!/usr/bin/env python
#
# Use qrcode to generate a qrcode to take you to the webserver easily
# pypi: https://pypi.org/project/qrcode/
# install command: pip install qrcode[pil]
# from command line: qr "https://www.google.com" > test.png
#
# Using this script allows you more flexibility, but may not be necessary

import qrcode

qr = qrcode.QRCode(
    border=4
)

# the node webserver lives here on port 9000
qr.add_data("http://10.10.10.1:9000")
# qr.add_data("this is a test")

# you could change colors if you want
img = qr.make_image(fill_color="black", back_color="white")
img.save('webpage_qr.png')
