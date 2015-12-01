import admin
import subprocess
import wx
import os

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

	try:
		if os.path.basename(__file__).endswith(".exe"):
			admin.runAsAdmin(["antsFromBoot.exe"])
		else:
			admin.runAsAdmin(["python", "antsFromBoot.py"])
		
		#subprocess.call(['C:\\Projects\\fsTools\\MftRcrd\\MFTRCRD.exe', 'C:\\Projects\\test2.py', '-d', 'indxdump=off', '1024', '-s'])
		#subprocess.call(['python', 'ants.py'])
		print "admin"

	except:
		if os.path.basename(__file__).endswith(".exe"):
			subprocess.call(["antsFromBoot.exe"])
		else:
			subprocess.call(["python", "antsFromBoot.py"])
		print "not admin"