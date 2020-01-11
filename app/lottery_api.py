import wx
import cv2
import os.path
from app.img_display import ImgShow
import signal

from app.config import *
from app.transText import TransparentStaticText

class WindowClass(wx.Frame):
	def __init__(self,parent,title):
	
		wx.Frame.__init__(self, None, -1, "年会")
		dpi = wx.DisplaySize()
		dispApi.set_ratio(dpi[0],dpi[1])
		self.Bind(wx.EVT_CLOSE,self.onClose)
		# panel = wx.Panel(self,-1,size = (dispApi.get_real_pixel_x(BKG_WIDTH),dispApi.get_real_pixel_y(BKG_HEIGH)))
		# panel.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBack)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseFrameBackground)
		self.Bind(wx.EVT_PAINT,self.onFramePaint)

		self.image = None
		self.start_label = False

		self.bkg = cv2.imread(BACKGROUND)

		self.lotter_start =  wx.Button(self, -1, '开始抽奖',pos = (dispApi.get_real_pixel_x(100),dispApi.get_real_pixel_y(100)),size = (dispApi.get_real_pixel_x(200),dispApi.get_real_pixel_y(50)))
		self.lotter_start.SetFont(wx.Font(dispApi.get_real_pixel_y(18),wx.SWISS, wx.NORMAL, wx.BOLD,faceName='微软雅黑'))
		self.lotter_start.SetForegroundColour("#ffe699")
		self.lotter_start.SetBackgroundColour("#152646")
		self.lotter_start_label = True
		self.show_update = False

		self.img_next =  wx.Button(self, -1, '猜猜看',pos = (dispApi.get_real_pixel_x(100),dispApi.get_real_pixel_y(180)),size = (dispApi.get_real_pixel_x(200),dispApi.get_real_pixel_y(50)))
		self.img_next.SetFont(wx.Font(dispApi.get_real_pixel_y(18),wx.SWISS, wx.NORMAL, wx.BOLD,faceName='微软雅黑'))
		self.img_next.SetForegroundColour("#ffe699")
		self.img_next.SetBackgroundColour("#152646")

		self.person_next =  wx.Button(self, -1, '幸运星',pos = (dispApi.get_real_pixel_x(100),dispApi.get_real_pixel_y(260)),size = (dispApi.get_real_pixel_x(200),dispApi.get_real_pixel_y(50)))
		self.person_next.SetFont(wx.Font(dispApi.get_real_pixel_y(18), wx.SWISS, wx.NORMAL, wx.BOLD,faceName='微软雅黑'))
		self.person_next.SetForegroundColour("#ffe699")
		self.person_next.SetBackgroundColour("#152646")

		self.lottery_label = TransparentStaticText(self,-1, '2020年新年年会获奖人员',pos = (dispApi.get_real_pixel_x(BKG_WIDTH//2 - 200),dispApi.get_real_pixel_y(50)),size = (dispApi.get_real_pixel_x(400),dispApi.get_real_pixel_y(50)))
		self.lottery_label.SetFont(wx.Font(dispApi.get_real_pixel_y(30), wx.SWISS, wx.NORMAL, wx.BOLD,faceName='微软雅黑'))
		# self.lottery_label.
		self.lottery_label.SetForegroundColour("#ffe699")

		self.timer = wx.Timer(self)
		self.timer.Start(1000. / 30.)
		self.Bind(wx.EVT_TIMER, self.onTimeUpdate, self.timer)
		# panel.Bind(wx.EVT_PAINT,self.onPaint)

		self.imgShowList = []
		for i in range(3):
			tmp = ImgShow(self,2,i+1)
			self.imgShowList.append(tmp)

		self.imgDisp = ImgShow(self,1,0)

		# self.Bind(wx.EVT_COMBOBOX, self.onCombobox, self.ch1)
		self.Bind(wx.EVT_BUTTON, self.onLottery, self.lotter_start)
		self.Bind(wx.EVT_BUTTON, self.onDispNext, self.img_next)
		self.Bind(wx.EVT_BUTTON, self.onDispContinue, self.person_next)

		self.Center()
		self.Maximize()
		# self.Fit()
		self.Show(True)

	def onEraseFrameBackground(self,event):
		pass

	def onFramePaint(self,event):
		h,w = self.GetSize()
		dc = wx.BufferedPaintDC(self)
		img = cv2.resize(self.bkg, (h, w))
		img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		image = wx.Bitmap.FromBuffer(h, w, img)
		dc.DrawBitmap(image , 0, 0)

	def onCombobox(self,event):
		str_get = event.GetString()
		label = '2020年新年年会'+ str_get +'获奖人员'
		self.lottery_label.SetLabel(label)

	def onLottery(self,event):
		self.start_label = True
		if self.lotter_start_label == True:
			self.lotter_start.SetLabel('停止抽奖')
			self.lotter_start_label = False
			self.imgDisp.set_state(STATE_RUNNING)
			self.imgDisp.disp_over = False			#开始抽奖时更新展示标志
			self.imgDisp.set_target_path()  # 结束时更新抽奖名单
			self.show_update = True
		else:
			self.lotter_start.SetLabel('开始抽奖')
			self.lotter_start_label = True
			self.imgDisp.set_state(STATE_CLOSING)
			self.imgDisp.set_img(DEFAULT_IMG)

		self.imgDisp.set_continue_label(False)

		label = True
		for tmp in self.imgShowList:
			if tmp.isdisp == False:
				label = False
				break

		if label == True:
			for tmp in self.imgShowList:
				tmp.isdisp = False
				tmp.set_img(DEFAULT_IMG)

	def onDispNext(self,event):
		if self.lotter_start.GetLabel() == '开始抽奖' and self.start_label == True:
			self.imgDisp.set_state(STATE_DISPLAY)
			self.imgDisp.set_continue_label(False)

	def onDispContinue(self,event):
		if self.lotter_start.GetLabel() == '开始抽奖' and self.start_label == True:
			self.imgDisp.set_state(STATE_DISPLAY)
			self.imgDisp.set_continue_label(True)

	def onTimeUpdate(self,event):
		if self.show_update == True:
			if self.imgDisp.disp_over == True:
				for tmp in self.imgShowList:
					if tmp.isdisp == False:
						tmp.set_img(self.imgDisp.target)
						f = open(LUCKY_TXT, 'a')
						img_path = os.path.basename(self.imgDisp.target)
						print(img_path)
						f.write(img_path)
						f.write('\n')
						f.close()

						tmp.isdisp = True
						self.show_update = False
						return

	def onFrameClear(self,event):
		label = True
		for tmp in self.imgShowList:
			if tmp.isdisp == False:
				label = False
				break

		if label == True:
			for tmp in self.imgShowList:
				tmp.isdisp = False
				tmp.set_img(DEFAULT_IMG)

	def onClose(self,event):
		self.imgDisp.timer.Stop()
		for tmp in self.imgShowList:
			tmp.timer.Stop()

		self.timer.Stop()
		self.Destroy()
		# os.kill(os.getpid(), signal.SIGTERM)

def main():
	app = wx.App()
	WindowClass(None, 'title')
	app.MainLoop()
