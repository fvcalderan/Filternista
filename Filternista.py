# Filternista
# Author: Felipe V. Calderan
# Version: 1.0
# License:
"""
Copyright 2021, Felipe V. Calderan

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import ui
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import photos
from console import alert

# current image and fx
img = None
fx = None

def tbl_tapped(sender):
	'@type sender: ui.ListDataSource'
	
	global fx
	
	if img is not None:
		# set current fx
		fx = sender.items[sender.selected_row]
		
		# apply current fx and display image
		with BytesIO() as bIO:
			fig = plt.imshow(img.convert('L'), cmap=fx)
			plt.axis('off')
			fig.axes.get_xaxis().set_visible(False)
			fig.axes.get_yaxis().set_visible(False)
			plt.savefig(bIO, bbox_inches='tight', pad_inches = 0)
			cimg = ui.Image.from_data(bIO.getvalue())	
		sender.tableview.superview['imv'].image = cimg
	else:
		sender.items = plt.colormaps()

def save_tapped(sender):
	'@type sender: ui.Button'
	
	# save to camera roll
	if fx is not None and img is not None:
		with BytesIO() as bIO:
			fig = plt.imshow(img.convert('L'), cmap=fx)
			plt.axis('off')
			fig.axes.get_xaxis().set_visible(False)
			fig.axes.get_yaxis().set_visible(False)
			plt.savefig(bIO, format='JPEG', bbox_inches='tight', pad_inches = 0)
			save_im=Image.open(bIO).convert('RGBA')
			photos.save_image(save_im)
	else:
		alert('Error', 'No image and/or FX selected.')
	
def load_tapped(sender):
	'@type sender: ui.Button'
	
	global img
	
	# choose between camera roll or camera
	if sender.name == 'btnLoad':
		img = photos.pick_image()
	else:
		img = photos.capture_image()
	
	# display image
	if img is not None:
		with BytesIO() as bIO:
			img.save(bIO, format='JPEG')
			cimg = ui.Image.from_data(bIO.getvalue())	
		sender.superview['imv'].image = cimg

if __name__ == '__main__':
	v = ui.load_view()
	
	# get all colormaps
	v['tbl'].data_source.items = plt.colormaps()
	
	# present in 'dark theme'
	v.present('fullscreen', title_bar_color='black', title_color='white')
	
