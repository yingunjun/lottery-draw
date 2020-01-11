import wx
import cv2
import os.path

import random
from app.config import *


class ImgShow(object):
	def __init__(self,parent,ratio,id):
		self.img = cv2.imread(DEFAULT_IMG)
		self.ratio = ratio
		if id == 0:
			position = (dispApi.get_real_pixel_x(BKG_WIDTH//2 - 320),dispApi.get_real_pixel_y(140))
		elif id ==1:
			position = (dispApi.get_real_pixel_x(BKG_WIDTH//2 - 510),dispApi.get_real_pixel_y(670))
		elif id ==2:
			position = (dispApi.get_real_pixel_x(BKG_WIDTH//2 - 160),dispApi.get_real_pixel_y(670))
		elif id ==3:
			position = (dispApi.get_real_pixel_x(BKG_WIDTH//2 + 190),dispApi.get_real_pixel_y(670))

		self.panel = wx.Panel(parent,-1,pos = position ,size = (dispApi.get_real_pixel_x(self.img.shape[1]//self.ratio),dispApi.get_real_pixel_y(self.img.shape[0]//self.ratio)))

		self.timer = wx.Timer(self.panel)
		self.timer.Start(1000. / 30.)
		self.panel.Bind(wx.EVT_TIMER, self.onUpdate, self.timer)
		self.panel.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBack)
		self.panel.Bind(wx.EVT_PAINT, self.onPaint)

		self.updating = False
		self.state = STATE_CLOSING
		self.img_cnt = 1
		self.disp_step = 0
		self.img_record = []
		self.target = ''
		self.continue_label = False
		self.disp_over = False

		self.isdisp = False
		self.pic_lst = None

		self.disp_method = 0

	def get_panel(self):
		return self.panel

	def cross_show(self,img):
		h, w = img.shape[:2]
		i = self.img_cnt

		pic = img * 0 + 100
		p = int(w * i // 30)
		q = int(h * i // 30)
		pic[:q, :p] = img[:q, :p]
		pic[h - q:, :p] = img[h - q:, :p]
		pic[:q, w - p:] = img[:q, w - p:]
		pic[h - q:, w - p:] = img[h - q:, w - p:]

		return pic

	def coutour_show(self,img):
		i = self.img_cnt
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		lowThreshold = 60 - i*30//5
		detected_edges = cv2.GaussianBlur(gray, (3, 3), 0)
		detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold * 3,apertureSize=3)
		pic = cv2.bitwise_and(img, img, mask=detected_edges)
		return pic

	def blur_show(self,img):
		i = self.img_cnt
		if i % 2 != 0:
			pic = cv2.GaussianBlur(img, (76 - i*5, 76 - i*5), sigmaX=1000, sigmaY=1000)
			self.pic_lst = pic
		else:
			pic = self.pic_lst

		return pic

	def onUpdate(self, event):
		if self.state == STATE_RUNNING:
			img_names = os.listdir(sample_dir)
			random.shuffle(img_names)
			img_path = os.path.join(os.path.abspath(sample_dir), img_names[0])
			self.img = cv2.imread(img_path)
			self.img_cnt = 1
		elif self.state == STATE_DISPLAY:
			img = cv2.imread(self.target)
			if self.disp_method == 1:
				pic = self.cross_show(img)
			elif self.disp_method == 2:
				pic = self.blur_show(img)
			elif self.disp_method == 3:
				pic = self.coutour_show(img)

			if self.continue_label == True:
				if self.img_cnt < 15:
					self.img_cnt += 1
				else:
					pic = img
					self.disp_over = True
			else:
				if self.disp_step == 1:
					if self.img_cnt < 5:
						self.img_cnt += 1
				elif self.disp_step == 2:
					if self.img_cnt < 10:
						self.img_cnt += 1
				elif self.disp_step == 3:
					if self.img_cnt < 15:
						self.img_cnt += 1
					else:
						pic = img
						self.disp_over = True

			self.img = pic
			self.img_record.append(self.target)

		self.panel.Refresh()

	def onPaint(self, event):
		img = self.img
		h, w = img.shape[:2]
		pic = cv2.resize(img,(dispApi.get_real_pixel_x(w//self.ratio),dispApi.get_real_pixel_y(h//self.ratio)))
		pic = cv2.cvtColor(pic,cv2.COLOR_BGR2RGB)
		image = wx.Bitmap.FromBuffer(dispApi.get_real_pixel_x(w//self.ratio), dispApi.get_real_pixel_y(h//self.ratio), pic)
		dc = wx.BufferedPaintDC(self.panel)
		dc.DrawBitmap(image, 0, 0)

	def set_img(self,img_path):
		img = cv2.imread(img_path)
		self.img = img

	def set_state(self,state):
		self.state = state
		if state == STATE_DISPLAY:
			self.disp_step += 1
		else:
			self.disp_step = 0

	def set_target_path(self):
		if not os.path.exists(LUCKY_TXT):
			#os.mknod(lucky_txt)
			f = open(LUCKY_TXT,'w')
			f.close()

		f = open(LUCKY_TXT,'r')
		lucky_list = f.readlines()
		lucky_list = [tmp.strip('\n') for tmp in lucky_list]
		f.close()

		while True:
			img_names = os.listdir(sample_dir)
			random.shuffle(img_names)
			img_path = os.path.join(os.path.abspath(sample_dir), img_names[0])
			tmp_img_path = os.path.basename(img_path)
			if tmp_img_path not in lucky_list:
				self.target = img_path
				if len(lucky_list) + 1 < 3:
					self.disp_method = 1
				elif len(lucky_list) + 1 < 5:
					self.disp_method = 2
				else:
					self.disp_method = 3
				break

	def set_continue_label(self,label):
		self.continue_label = label

	def onEraseBack(self, event):
		return

	def distory(self):
		self.timer.Stop()



























