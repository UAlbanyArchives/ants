import admin
import subprocess
from lxml import etree as ET
import wx
import os
import sys
import datetime
import wx.lib.wxpTag

class spashDialog( wx.Dialog ):
	
	def __init__( self ):
	
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
			
			wx.Dialog.__init__ ( self, None, id = wx.ID_ANY, title = "Welcome to ANTS", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
			
			self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
			
			bSizer1 = wx.BoxSizer( wx.VERTICAL )
			
			self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
			bSizer2 = wx.BoxSizer( wx.VERTICAL )
			
			self.m_bitmap1 = wx.StaticBitmap( self.m_panel1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 70,70 ), 0 )
			bSizer2.Add( self.m_bitmap1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
			
			self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"ANTS: Archives Network Transfer System", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText1.Wrap( -1 )
			self.m_staticText1.SetFont( wx.Font( 18, 74, 90, 90, False, "Arial" ) )
			
			bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
			
			self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Select a folder to transfer.", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText3.Wrap( -1 )
			bSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
			
			bSizer22 = wx.BoxSizer( wx.HORIZONTAL )
			
			bSizer22.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
			self.m_button1 = wx.Button( self.m_panel1, wx.ID_ANY, u"Browse...", wx.DefaultPosition, wx.DefaultSize, 0 )
			bSizer22.Add( self.m_button1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
			self.m_button2 = wx.Button( self.m_panel1, wx.ID_ANY, u"View Receipt", wx.DefaultPosition, wx.DefaultSize, 0 )
			bSizer22.Add( self.m_button2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
			self.m_button3 = wx.Button( self.m_panel1, wx.ID_ANY, u"Receive Files", wx.DefaultPosition, wx.DefaultSize, 0 )
			bSizer22.Add( self.m_button3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
			bSizer22.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
			bSizer2.Add( bSizer22, 1, wx.EXPAND, 5 )
			
			
			bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
			
			bSizer5 = wx.BoxSizer( wx.VERTICAL )
			
			self.m_hyperlink1 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, u"http://library.albany.edu/archive/universityarchives", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
			bSizer5.Add( self.m_hyperlink1, 0, wx.ALL, 5 )
			
			
			bSizer3.Add( bSizer5, 1, wx.EXPAND, 5 )
			
			bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
			bSizer48 = wx.BoxSizer( wx.VERTICAL )
			bSizer49 = wx.BoxSizer( wx.VERTICAL )
			bSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
			bSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
			bSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
			bSizer4.Add( bSizer48, 1, wx.EXPAND, 5 )
			bSizer4.Add( bSizer49, 1, wx.EXPAND, 5 )
			
			self.m_hyperlink3 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, u"About", wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
			bSizer48.Add( self.m_hyperlink3, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
			
			self.m_hyperlink2 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, u"Credits", wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
			bSizer49.Add( self.m_hyperlink2, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
			
			self.m_button2.Bind( wx.EVT_BUTTON, self.viewReceipt )
			self.m_button3.Bind( wx.EVT_BUTTON, self.checkforFiles )
			self.m_hyperlink2.Bind( wx.EVT_HYPERLINK, self.openCredits)
			self.m_hyperlink3.Bind( wx.EVT_HYPERLINK, self.aboutBox)
			self.Bind( wx.EVT_CLOSE, self.closeProgram )
			
			
			bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )
			
			
			bSizer2.Add( bSizer3, 1, wx.EXPAND, 5 )
			
			
			self.m_panel1.SetSizer( bSizer2 )
			self.m_panel1.Layout()
			bSizer2.Fit( self.m_panel1 )
			bSizer1.Add( self.m_panel1, 1, wx.ALL|wx.EXPAND, 5 )
			
			
			self.SetSizer( bSizer1 )
			self.Layout()
			bSizer1.Fit( self )
			
			self.Centre( wx.BOTH )
			
			# Connect Events
			self.m_button1.Bind( wx.EVT_BUTTON, self.runANTS )
	
	def viewReceipt(self, event):
		from receiptReceive import produceReceipt
		xmlSource = True
		produceReceipt(self, xmlSource)
	
	def checkforFiles(self, event):
		from receiptReceive import checkReceiveFiles
		xmlSource = True
		checkReceiveFiles(self, xmlSource)
	
	def openCredits(self, event):
		loadCredits = CreditsFrame(self)
		loadCredits.Show(True)
	
		
	def aboutBox(self, event):
		info = wx.AboutDialogInfo()
		info.Name = "ANTS: Archives Network Transfer System"
		info.Version = "0.1 Beta"
		info.Copyright = "(C) 2015 Gregory Wiedeman"
		info.Description = "ANTS gathers metadata and packages files for transfer to an institutional archives."
		info.WebSite = ("http://library.albany.edu/archive/universityarchives", "Learn more about ANTS")
		license = open("LICENSE.txt")
		licenseLines = license.readlines()
		licenseText = "".join(licenseLines)
		info.License = licenseText
		# Show the wx.AboutBox
		wx.AboutBox(info)
	
	def closeProgram(self, event):
		sys.exit()
	
	
	def runANTS( self, event ):
		if getattr(sys, 'frozen', False):
			boot = ["antsFromBoot.exe"]
		elif __file__:
			boot = ["python", "antsFromBoot.py"]
		try:
			admin.runAsAdmin(self, boot)
			print "admin"
		except:
			subprocess.Popen(boot, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			print "not admin"
			self.Close()


##############################################################################################################################

class CreditsFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"ANTS Credits", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"ANTS uses the following tools/scripts:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer2.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"bagit-python was developed by Ed Summers:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		gSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.m_hyperlink1 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, u"bagit-python", u"https://libraryofcongress.github.io/bagit-python/", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		gSizer1.Add( self.m_hyperlink1, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText4 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"MFTRCRD was developed by Joakim Schicht:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		gSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.m_hyperlink2 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, u"MFTRCRD", u"https://github.com/jschicht/MftRcrd", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		gSizer1.Add( self.m_hyperlink2, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText5 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Plaso was developed by Kristinn Gudjonsson:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		gSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.m_hyperlink3 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, u"Plaso", u"https://github.com/log2timeline/plaso/wiki", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		gSizer1.Add( self.m_hyperlink3, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"admin.py UAC elevation script was written by Preston Landers:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		gSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.m_hyperlink4 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, u"admin.py", u"http://stackoverflow.com/questions/19672352/how-to-run-python-script-with-elevated-privilege-on-windows", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		gSizer1.Add( self.m_hyperlink4, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText7 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"resource_path.py script for embedding binaries was found here:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		gSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.m_hyperlink5 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, u"resource_path.py", u"http://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		gSizer1.Add( self.m_hyperlink5, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText8 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"ANTS was built using wxFormBuilder and PyInstaller", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		gSizer1.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		self.m_hyperlink6 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, u"PyInstaller", u"www.pyinstaller.org", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		gSizer1.Add( self.m_hyperlink6, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		
		bSizer2.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		self.m_button2 = wx.Button( self.m_panel1, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button2, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		
		self.m_panel1.SetSizer( bSizer2 )
		self.m_panel1.Layout()
		bSizer2.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_button2.Bind( wx.EVT_BUTTON, self.closeButton )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def closeButton( self, event ):
		self.Close()
		
#######################################################################################################################

#mandatory in wx, create an app, False stands for not deteriction stdin/stdout
#refer manual for details
app = wx.App(False)
 
#create an object of ANTSFrame
frame = spashDialog()
#show the frame
frame.Show(True)
#start the applications
app.MainLoop()