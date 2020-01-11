import wx


class TransparentStaticText(wx.StaticText):
	"""
	重写StaticText控件
	"""

	def __init__(self, parent, id=wx.ID_ANY, label='', pos=wx.DefaultPosition, size=wx.DefaultSize,
				 style=wx.TRANSPARENT_WINDOW, name='TransparentStaticText'):
		wx.StaticText.__init__(self, parent, id, label, pos, size, style, name)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
		self.Bind(wx.EVT_SIZE, self.OnSize)

	def OnPaint(self, event):
		bdc = wx.PaintDC(self)
		dc = wx.GCDC(bdc)
		font_face = self.GetFont()
		font_color = self.GetForegroundColour()
		dc.SetFont(font_face)
		dc.SetTextForeground(font_color)
		dc.DrawText(self.GetLabel(), 0, 0)

	def OnSize(self, event):
		self.Refresh()
		event.Skip()