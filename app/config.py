import sys
import os

video_src = 1

file_ab_dir = sys.argv[0]
file_dir,file_name = os.path.split(os.path.abspath(file_ab_dir))

STATE_RUNNING = 1
STATE_CLOSING = 0
STATE_DISPLAY = 3

sample_dir = os.path.join(file_dir,'samples')
DEFAULT_IMG = os.path.join(file_dir,'default.png')
LUCKY_TXT =  os.path.join(file_dir,'lucky.txt')
BACKGROUND = os.path.join(file_dir,'background.jpeg')

BKG_WIDTH = 1920
BKG_HEIGH = 1080

global dpi_ratio_x ,dpi_ratio_y

def get_real_pixel_x(data):
	global dpi_ratio_x
	return int(data*dpi_ratio_x)

def get_real_pixel_y(data):
	global dpi_ratio_y
	return int(data*dpi_ratio_y)


class dpi_handle():
	def __init__(self):
		self.dpi_ratio_x = 1
		self.dpi_ratio_y = 1

	def set_ratio(self,x,y):
		self.dpi_ratio_x = x/BKG_WIDTH
		self.dpi_ratio_y = y/BKG_HEIGH

	def get_real_pixel_x(self,data):
		return int(data * self.dpi_ratio_x)

	def get_real_pixel_y(self,data):
		return int(data * self.dpi_ratio_y)

dispApi = dpi_handle()
