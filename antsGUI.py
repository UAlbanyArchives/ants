# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.lib.agw.customtreectrl as CT
import os
import sys
from lxml import etree as ET
from resource_path import resource_path

###########################################################################
## Class mainFrame
###########################################################################

class mainFrame ( wx.Frame ):
	
	def __init__( self, parent, configData, sourceDir ):
		displaySize= wx.DisplaySize()
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"ANTS: Archives Network Transfer System", pos = wx.DefaultPosition, size=(displaySize[0]/1.45, displaySize[1]/1.30), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.SetBackgroundColour(wx.Colour(221, 221, 221, 255))
		self.SetSizeHints(400,450)
		txtSize = displaySize[1]/1.30 / float(6.5)
		self.sourceDir = sourceDir
		
		favicon = wx.Icon(resource_path('A.gif'), wx.BITMAP_TYPE_GIF, 16, 16)
		self.SetIcon(favicon)
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.mainNotebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fileTab = wx.Panel( self.mainNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.fileTab.SetBackgroundColour(wx.Colour(255, 255, 255, 255))
		
		bSizer99 = wx.BoxSizer( wx.VERTICAL )	
		self.instructText = wx.StaticText( self.fileTab, wx.ID_ANY, u"Click on the directory to describe the records you want to transfer:", wx.DefaultPosition, wx.DefaultSize, 0 )
		fileFont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.instructText.SetFont(fileFont)
		self.instructText.Wrap( -1 )
		bSizer99.Add( self.instructText, 0, wx.ALL|wx.ALIGN_LEFT, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		bSizer99.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		self.descDirCtrl = CT.CustomTreeCtrl( self.fileTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, agwStyle= wx.TR_DEFAULT_STYLE | CT.TR_FULL_ROW_HIGHLIGHT)
		self.descDirCtrl.SetBackgroundColour(wx.Colour(255, 255, 255, 255))
		dirFile = os.path.join(self.appData, "~directory.xml")
		parser = ET.XMLParser(remove_blank_text=True)
		dirParse = ET.parse(dirFile, parser)
		dirXML = dirParse.getroot()
		def dir2tree(dir, rootPoint):
			for item in dir:
				if "name" in item.attrib:
					if item.tag.lower() == "folder":
						child = self.descDirCtrl.AppendItem(rootPoint, item.attrib['name'], ct_type=1)
						self.descDirCtrl.SetPyData(child, item.find('id').text)
						if item.attrib["check"] == "True":
							self.descDirCtrl.CheckItem(child)
						dir2tree(item, child)
					elif item.tag.lower() == "file":
						child = self.descDirCtrl.AppendItem(rootPoint, item.attrib['name'], ct_type=1)
						self.descDirCtrl.SetPyData(child, item.find('id').text)
						if item.attrib["check"] == "True":
							self.descDirCtrl.CheckItem(child)
					else:
						print "error: " + item.tag
		self.root = self.descDirCtrl.AddRoot(dirXML.find('folder').attrib['name'], ct_type=1)
		self.descDirCtrl.SetPyData(self.root, dirXML.find('folder/id').text)
		dir2tree(dirXML.find('folder'), self.root)
		if dirXML.find('folder').attrib["check"] == "True":
			self.descDirCtrl.CheckItem(self.root)
		self.descDirCtrl.ExpandAll()
		self.descDirCtrl.ScrollTo(self.root)
		
		
		bSizer4.Add( self.descDirCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		firstFile = os.path.basename(sourceDir)
		self.fileNameText = wx.StaticText( self.fileTab, wx.ID_ANY, firstFile, wx.DefaultPosition, wx.DefaultSize, 0 )
		fileFont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.fileNameText.SetFont(fileFont)
		self.fileNameText.Wrap( -1 )
		bSizer14.Add( self.fileNameText, 0, wx.ALL|wx.ALIGN_LEFT, 5 )
		
		fgSizer6 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText12 = wx.StaticText( self.fileTab, wx.ID_ANY, u"Record Description:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		fgSizer6.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
		self.rcdDescInput = wx.TextCtrl( self.fileTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,txtSize ), wx.TE_MULTILINE )
		fgSizer6.Add( self.rcdDescInput, 0, wx.ALL, 5 )
		
		bSizer91 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText13 = wx.StaticText( self.fileTab, wx.ID_ANY, u"Access Concerns", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		bSizer91.Add( self.m_staticText13, 0, wx.ALL, 5 )
		
		self.m_button6 = wx.Button( self.fileTab, wx.ID_ANY, u"Examples >", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer91.Add( self.m_button6, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		fgSizer6.Add( bSizer91, 1, wx.EXPAND, 5 )
		
		self.rcdAccessInput = wx.TextCtrl( self.fileTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,txtSize ), wx.TE_MULTILINE )
		fgSizer6.Add( self.rcdAccessInput, 0, wx.ALL, 5 )
		
		
		bSizer14.Add( fgSizer6, 1, wx.EXPAND, 5 )
		
		
		bSizer7.Add( bSizer14, 1, wx.EXPAND, 5 )
		
		self.m_staticline3 = wx.StaticLine( self.fileTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer7.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.notesInput = wx.StaticText( self.fileTab, wx.ID_ANY, u"Notes for Archivist", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.notesInput.Wrap( -1 )
		bSizer9.Add( self.notesInput, 0, wx.ALL, 5 )
		
		self.notesInput = wx.TextCtrl( self.fileTab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 320,120 ), wx.TE_MULTILINE )
		bSizer9.Add( self.notesInput, 0, wx.ALL, 5 )
		
		
		bSizer7.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		self.m_staticline4 = wx.StaticLine( self.fileTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer7.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.transferBtn = wx.Button( self.fileTab, wx.ID_ANY, u"Submit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.transferBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.compressCheck = wx.CheckBox( self.fileTab, wx.ID_ANY, u"Compress files", wx.DefaultPosition, wx.DefaultSize, 0 )
		if "compressDefault" in configData:
			if configData["compressDefault"].lower().strip() == "false":
				self.compressCheck.SetValue(False)
			else:
				self.compressCheck.SetValue(True) 
		else:
			self.compressCheck.SetValue(True) 
		bSizer12.Add( self.compressCheck, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		bSizer7.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		
		bSizer4.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		self.fileTab.SetSizer( bSizer99 )
		self.fileTab.Layout()
		bSizer4.Fit( self.fileTab )
		self.mainNotebook.AddPage( self.fileTab, u"Files to Transfer", True )
		self.creatorTab = wx.Panel( self.mainNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.creatorTab.SetBackgroundColour(wx.Colour(255, 255, 255, 255))
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer2 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self.creatorTab, wx.ID_ANY, u"Records Creator", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.creatorInput = wx.TextCtrl( self.creatorTab, wx.ID_ANY, configData["creator"], wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer2.Add( self.creatorInput, 0, wx.ALL, 5 )
		
		self.m_staticText2 = wx.StaticText( self.creatorTab, wx.ID_ANY, u"Creator ID", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer2.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.creatorIdInput = wx.TextCtrl( self.creatorTab, wx.ID_ANY, configData["creatorId"], wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer2.Add( self.creatorIdInput, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.creatorTab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 7, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( self.creatorTab, wx.ID_ANY, u"Donor", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.donorInput = wx.TextCtrl( self.creatorTab, wx.ID_ANY, configData["donor"], wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer3.Add( self.donorInput, 0, wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.creatorTab, wx.ID_ANY, u"Position/Role", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer3.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.positionInput = wx.TextCtrl( self.creatorTab, wx.ID_ANY, configData["role"], wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer3.Add( self.positionInput, 0, wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.creatorTab, wx.ID_ANY, u"Email", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer3.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.emailInput = wx.TextCtrl( self.creatorTab, wx.ID_ANY, configData["email"], wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer3.Add( self.emailInput, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.creatorTab, wx.ID_ANY, u"Office", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer3.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.officeInput = wx.TextCtrl( self.creatorTab, wx.ID_ANY, configData["office"], wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer3.Add( self.officeInput, 0, wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.creatorTab, wx.ID_ANY, u"Address Line 1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		fgSizer3.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.address1Input = wx.TextCtrl( self.creatorTab, wx.ID_ANY, configData["address1"], wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer3.Add( self.address1Input, 0, wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self.creatorTab, wx.ID_ANY, u"Address Line 2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		fgSizer3.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		self.address2Input = wx.TextCtrl( self.creatorTab, wx.ID_ANY, configData["address2"], wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer3.Add( self.address2Input, 0, wx.ALL, 5 )
		
		self.m_staticText9 = wx.StaticText( self.creatorTab, wx.ID_ANY, u"Address Line 3", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		fgSizer3.Add( self.m_staticText9, 0, wx.ALL, 5 )
		
		self.address3Input = wx.TextCtrl( self.creatorTab, wx.ID_ANY, configData["address3"], wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer3.Add( self.address3Input, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		self.creatorUpdateBtn = wx.Button( self.creatorTab, wx.ID_ANY, u"Set as Default", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.creatorUpdateBtn, 0, wx.ALL, 5 )
		
		
		bSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		self.creatorTab.SetSizer( bSizer2 )
		self.creatorTab.Layout()
		bSizer2.Fit( self.creatorTab )
		self.mainNotebook.AddPage( self.creatorTab, u"Creator Profile", False )
		self.transferTab = wx.Panel( self.mainNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.transferTab.SetBackgroundColour(wx.Colour(255, 255, 255, 255))
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer33 = wx.BoxSizer( wx.HORIZONTAL )
		m_radioBox1Choices = [ u"Network Share", u"File Transfer Protocol (FTP)" ]
		self.m_radioBox1 = wx.RadioBox( self.transferTab, wx.ID_ANY, u"Transfer Method", wx.DefaultPosition, wx.DefaultSize, m_radioBox1Choices, 1, wx.RA_SPECIFY_COLS )
		if configData["transferMethod"].lower() == "ftp":
			self.m_radioBox1.SetSelection( 1 )
		else:
			self.m_radioBox1.SetSelection( 0 )
		bSizer33.Add( self.m_radioBox1, 0, wx.ALL, 5 )
		bSizer34 = wx.BoxSizer( wx.VERTICAL )
		bSizer34.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		self.receiveFiles = wx.Button( self.transferTab, wx.ID_ANY, u"Receive Files", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer34.Add( self.receiveFiles, 0, wx.ALL, 5 )
		bSizer34.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		bSizer33.Add( bSizer34, 1, wx.EXPAND, 5 )
		bSizer3.Add( bSizer33, 1, wx.EXPAND, 5 )
		
		fgSizer9 = wx.FlexGridSizer( 4, 3, 0, 0 )
		fgSizer9.SetFlexibleDirection( wx.BOTH )
		fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText18 = wx.StaticText( self.transferTab, wx.ID_ANY, u"Transfer Location (PATH or FTP URL)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		fgSizer9.Add( self.m_staticText18, 0, wx.ALL, 5 )
		
		self.transferLocInput = wx.TextCtrl( self.transferTab, wx.ID_ANY, configData["transferLocation"], wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
		fgSizer9.Add( self.transferLocInput, 0, wx.ALL, 5 )
		
		self.checkLocation = wx.Button( self.transferTab, wx.ID_ANY, u"Test Transfer Location", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer9.Add( self.checkLocation, 0, wx.ALL, 5 )
		
		self.m_staticText21 = wx.StaticText( self.transferTab, wx.ID_ANY, u"Receive Location (PATH or FTP URL)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		fgSizer9.Add( self.m_staticText21, 0, wx.ALL, 5 )
		
		self.receiveInput = wx.TextCtrl( self.transferTab, wx.ID_ANY, configData["receiveLocation"], wx.DefaultPosition, wx.Size( 400,-1 ) )
		fgSizer9.Add( self.receiveInput, 0, wx.ALL, 5 )
		
		self.checkReceiveLocation = wx.Button( self.transferTab, wx.ID_ANY, u"Test Receive Location", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer9.Add( self.checkReceiveLocation, 0, wx.ALL, 5 )
		
		self.m_staticText19 = wx.StaticText( self.transferTab, wx.ID_ANY, u"Login (FTP only)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		fgSizer9.Add( self.m_staticText19, 0, wx.ALL, 5 )
		
		self.loginInput = wx.TextCtrl( self.transferTab, wx.ID_ANY, configData["login"], wx.DefaultPosition, wx.Size( 200,-1 ) )
		fgSizer9.Add( self.loginInput, 0, wx.ALL, 5 )
		
		fgSizer9.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText20 = wx.StaticText( self.transferTab, wx.ID_ANY, u"Password (FTP only)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		fgSizer9.Add( self.m_staticText20, 0, wx.ALL, 5 )
		
		self.passwordInput = wx.TextCtrl( self.transferTab, wx.ID_ANY, configData["password"], wx.DefaultPosition, wx.Size( 200,-1 ), wx.TE_PASSWORD )
		fgSizer9.Add( self.passwordInput, 0, wx.ALL, 5 )
		
		
		
		
		bSizer3.Add( fgSizer9, 1, wx.EXPAND, 5 )
		
		bSizer95 = wx.BoxSizer( wx.HORIZONTAL )
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		timestampChoices = [ u"Python os.stat", u"Plaso Engine" ]
		self.timestampOption = wx.RadioBox( self.transferTab, wx.ID_ANY, u"Non-Admin Timestamp Tool", wx.DefaultPosition, wx.DefaultSize, timestampChoices, 1, wx.RA_SPECIFY_COLS )
		if configData["timestampTool"].lower() == "plaso":
			self.timestampOption.SetSelection( 1 )
		else:
			self.timestampOption.SetSelection( 0 )
		bSizer95.Add( self.timestampOption, 0, wx.ALL, 5 )
		
		timeZoneChoices = [ u"Local Time", u"POSIX time", u"UTC" ]
		self.timeZoneOption = wx.RadioBox( self.transferTab, wx.ID_ANY, u"Timestamp Options", wx.DefaultPosition, wx.DefaultSize, timeZoneChoices, 1, wx.RA_SPECIFY_COLS )
		if configData["timeZone"].lower() == "posix":
			self.timeZoneOption.SetSelection( 1 )
		elif configData["timeZone"].lower() == "utc":
			self.timeZoneOption.SetSelection( 2 )
		else:
			self.timeZoneOption.SetSelection( 0 )
		bSizer95.Add( self.timeZoneOption, 0, wx.ALL, 5 )
		
		compressOptionChoices = [ u"ZIP", u"TAR.GZIP" ]
		self.compressOption = wx.RadioBox( self.transferTab, wx.ID_ANY, u"Compression", wx.DefaultPosition, wx.DefaultSize, compressOptionChoices, 1, wx.RA_SPECIFY_COLS )
		if configData["compress"].lower() == "gzip":
			self.compressOption.SetSelection( 1 )
		else:
			self.compressOption.SetSelection( 0 )
		bSizer10.Add( self.compressOption, 0, wx.ALL, 5 )
		
		hashOptionChoices = [ u"MD5", u"SHA256" ]
		self.hashOption = wx.RadioBox( self.transferTab, wx.ID_ANY, u"Checksum", wx.DefaultPosition, wx.DefaultSize, hashOptionChoices, 1, wx.RA_SPECIFY_COLS )
		if configData["checksum"].lower() == "sha256":
			self.hashOption.SetSelection( 1 )
		else:
			self.hashOption.SetSelection( 0 )
		bSizer10.Add( self.hashOption, 0, wx.ALL, 5 )
		
		receiptOptionChoices = [ u"HTML/Bootstrap", u"CSV", u"XML" ]
		self.receiptOption = wx.RadioBox( self.transferTab, wx.ID_ANY, u"Receipt Format", wx.DefaultPosition, wx.DefaultSize, receiptOptionChoices, 1, wx.RA_SPECIFY_COLS )
		if configData["receipt"].lower() == "csv":
			self.receiptOption.SetSelection( 1 )
		elif configData["receipt"].lower() == "xml":
			self.receiptOption.SetSelection( 2 )
		else:
			self.receiptOption.SetSelection( 0 )
		bSizer10.Add( self.receiptOption, 0, wx.ALL, 5 )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		
		
		self.m_button5 = wx.Button( self.transferTab, wx.ID_ANY, u"View Receipt", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.m_button5, 0, wx.ALL, 5 )
		
		self.m_button61 = wx.Button( self.transferTab, wx.ID_ANY, u"Export Receipt", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.m_button61, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		bSizer3.Add( bSizer95, 1, wx.EXPAND, 5 )
		bSizer3.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		self.m_button9 = wx.Button( self.transferTab, wx.ID_ANY, u"Set as Default", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button9, 0, wx.ALL, 5 )
		
		
		
		
		bSizer3.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		bSizer3.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		self.transferTab.SetSizer( bSizer3 )
		self.transferTab.Layout()
		bSizer3.Fit( self.transferTab )
		self.mainNotebook.AddPage( self.transferTab, u"Options", False )
		
		bSizer1.Add( self.mainNotebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		
		self.Bind( wx.EVT_CLOSE, self.closeWindow )
		self.descDirCtrl.Bind( wx.EVT_TREE_SEL_CHANGED, self.descRecord )
		self.descDirCtrl.Bind( CT.EVT_TREE_ITEM_CHECKED, self.itemChecked )
		self.rcdDescInput.Bind( wx.EVT_TEXT, self.updateRcrdDesc )
		self.rcdAccessInput.Bind( wx.EVT_TEXT, self.updateRcrdAccess )
		self.m_button6.Bind( wx.EVT_BUTTON, self.accessOptions )
		self.transferBtn.Bind( wx.EVT_BUTTON, self.transferFiles )
		self.creatorUpdateBtn.Bind( wx.EVT_BUTTON, self.updateConfig )
		self.m_button5.Bind( wx.EVT_BUTTON, self.viewReceipt )
		self.m_button61.Bind( wx.EVT_BUTTON, self.saveReceipt )
		self.m_button9.Bind( wx.EVT_BUTTON, self.updateConfig )
		self.checkLocation.Bind( wx.EVT_BUTTON, self.testTransferLocation )
		self.receiveFiles.Bind( wx.EVT_BUTTON, self.checkforFiles )
		self.checkReceiveLocation.Bind( wx.EVT_BUTTON, self.testReceiveLocation )
		self.Bind( wx.EVT_CLOSE, self.closeANTS )
		
		#show info from old ~directory.xml on load
		self.descRecord(self)
		
	
	def __del__( self ):
		pass
	

	def closeWindow( self, event ):
		sys.exit()
	
	

