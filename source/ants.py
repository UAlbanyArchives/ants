import admin
import subprocess
import wx
import os
import sys

app = wx.App(False)
app.MainLoop()

systemPass = False
if os.name == "nt":
	systemPass = True
else:
	checkWin = wx.MessageDialog(None, 'ANTS is designed to be run on Windows XP SP2 and later with NTFS filesystems. Other systems are likely to experience errors. Do you want to continue anyway?', 'ANTS is designed for Windows.', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_EXCLAMATION)
	if checkWin.ShowModal() == wx.ID_YES:
		systemPass = True
	else:
		sys.exit()

if systemPass == True:
	if getattr(sys, 'frozen', False):
		boot = ["antsFromBoot.exe"]
	elif __file__:
		boot = ["python", "antsFromBoot.py"]

	try:
		admin.runAsAdmin(boot)	
		print "admin"

	except:
		subprocess.call(boot)
		print "not admin"