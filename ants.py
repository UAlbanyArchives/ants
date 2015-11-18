#importing wx files
import wx
from lxml import etree as ET
import os
import sys
import uuid
import base64
from threading import Thread
import shutil
import bagit

 
#import the newly created GUI file
import antsGUI as gui
 
 
#inherit from the MainFrame created in wxFormBuilder and create ANTSFrame
class ANTSFrame(gui.mainFrame):
	#constructor
	def __init__(self, parent):
	
	
		#Splash screen/browse instructions
		splashDialog = spashDialog()
		splashDialog.ShowModal()
	
		#initial directory selection
		dialogBrowse = wx.DirDialog(None, "Choose a folder to transfer:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
		if dialogBrowse.ShowModal() == wx.ID_OK:
			sourceDir = dialogBrowse.GetPath()
		else:
			sys.exit()
		dialogBrowse.Destroy()
		
		#read config
		if not os.path.isfile("config.xml"):
			antsConfigXML = ET.Element(antsConfigXML)
			accessionCount = ET.SubElement(antsConfigXML, 'accessionCount')
			creatorXML = ET.SubElement(antsConfigXML, 'creatorXML')
			creatorIdXML = ET.SubElement(antsConfigXML, 'creatorId')
			donorXML = ET.SubElement(antsConfigXML, 'donor')
			roleXML = ET.SubElement(antsConfigXML, 'role')
			emailXML = ET.SubElement(antsConfigXML, 'email')
			officeXML = ET.SubElement(antsConfigXML, 'office')
			address1XML = ET.SubElement(antsConfigXML, 'address1')
			address2XML = ET.SubElement(antsConfigXML, 'address2')
			address3XML = ET.SubElement(antsConfigXML, 'address3')
			transferMethodXML = ET.SubElement(antsConfigXML, 'transferMethod')
			transferLocationXML = ET.SubElement(antsConfigXML, 'transferLocation')
			loginXML = ET.SubElement(antsConfigXML, 'login')
			pwXML = ET.SubElement(antsConfigXML, 'pw')
			configXMLString = ET.tostring(antsConfigXML, pretty_print=True)
			file = open("config.xml", "w")
			file.write(configXMLString)
			file.close()
		configXML = "config.xml"
		parser = ET.XMLParser(remove_blank_text=True)
		configParse = ET.parse(configXML, parser)
		config = configParse.getroot()
		configData = {"creator": self.readXML(config, "creator"), "creatorId": self.readXML(config, "creatorId"), "donor": self.readXML(config, "donor"), "role": self.readXML(config, "role"), "email": self.readXML(config, "email"), "office": self.readXML(config, "office"), "address1": self.readXML(config, "address1"), "address2": self.readXML(config, "address2"), "address3": self.readXML(config, "address3"), "transferMethod": self.readXML(config, "transferMethod"), "transferLocation": self.readXML(config, "transferLocation"), "login": self.readXML(config, "login"), "password": base64.b64decode(self.readXML(config, "pw"))}

		
		#read directory
		try:
			rootXML = ET.Element('accession')
			if config.find('accessionCount').text:
				pass
			else:
				config.find('accessionCount').text = "0"
			accessionCount = int(config.find('accessionCount').text) + 1
			donorNormal = config.find('donor').text.lower().strip().replace(" ", "_")
			rootXML.set('number', config.find('creatorId').text + "-" + donorNormal + "-" + str(accessionCount))
			profileXML = ET.SubElement(rootXML, "profile")
			notesXML = ET.SubElement(profileXML, "notes")
			creatorXML = ET.SubElement(profileXML, "creator")
			creatorIdXML = ET.SubElement(profileXML, "creatorId")
			donotXML = ET.SubElement(profileXML, "donor")
			roleXML = ET.SubElement(profileXML, "role")
			emailXML = ET.SubElement(profileXML, "email")
			officeXML = ET.SubElement(profileXML, "office")
			address1XML = ET.SubElement(profileXML, "address1")
			address2XML = ET.SubElement(profileXML, "address2")
			address3XML = ET.SubElement(profileXML, "address3")
			methodXML = ET.SubElement(profileXML, "method")
			locationXML = ET.SubElement(profileXML, "location")
			folderXML = ET.SubElement(rootXML, "folder")
			folderXML.set('name', os.path.basename(sourceDir))
			folderXML.set('check', 'True')
			folderId = ET.SubElement(folderXML, "id")
			folderId.text = str(uuid.uuid4())
			folderDesc = ET.SubElement(folderXML, "description")
			folderAccess = ET.SubElement(folderXML, "access")
			def dir2XML(path, root):
				for item in os.listdir(path):
					itempath = os.path.join(path, item)
					if os.path.isdir(itempath):
						itemXML = ET.SubElement(root, "folder")
						itemXML.set('name', item)
						itemXML.set('check', "True")
						idXML = ET.SubElement(itemXML, "id")
						idXML.text = str(uuid.uuid4())
						descXML = ET.SubElement(itemXML, "description")
						accessXML = ET.SubElement(itemXML, "access")
						dir2XML(os.path.join(path, item), itemXML)
					elif os.path.isfile(itempath):
						itemXML = ET.SubElement(root, "file")
						itemXML.set('name', item)
						itemXML.set('check', "True")
						idXML = ET.SubElement(itemXML, "id")
						idXML.text = str(uuid.uuid4())
						descXML = ET.SubElement(itemXML, "description")
						accessXML = ET.SubElement(itemXML, "access")
			dir2XML(sourceDir, folderXML)
			dirXMLString = ET.tostring(rootXML, pretty_print=True)
			file = open("directory.xml", "w")
			file.write(dirXMLString)
			file.close()
		except Exception as exceptMsg:
			exceptLine = sys.exc_traceback.tb_lineno
			self.errorDialog("Could not read the directory you selected", exceptMsg, exceptLine)
				
		
		#initialize parent class
		try:
			gui.mainFrame.__init__(self, parent, configData, sourceDir)
		except Exception as exceptMsg:
			exceptLine = sys.exc_traceback.tb_lineno
			self.errorDialog("Could not load GUI", exceptMsg, exceptLine)
 
	def errorDialog(self, errorMsg, exceptMsg, exceptLine):
		errorPopup = wx.MessageDialog(None, errorMsg + "\n\n" + str(exceptMsg) + "\n" + "Line: " + str(exceptLine), "ERROR", wx.OK | wx.ICON_EXCLAMATION)
		errorPopup.ShowModal()
		sys.exit()
	
	
	def readXML(self, element, field):
			if element.find(field).text:
				value = element.find(field).text
			else:
				value =""
			return value
	
	def updateConfig(self, event):
		configXML = "config.xml"
		parser = ET.XMLParser(remove_blank_text=True)
		configParse = ET.parse(configXML, parser)
		config = configParse.getroot()
		config.find('creator').text = self.creatorInput.GetValue()
		config.find('creatorId').text = self.creatorIdInput.GetValue()
		config.find('donor').text = self.donorInput.GetValue()
		config.find('role').text = self.positionInput.GetValue()
		config.find('email').text = self.emailInput.GetValue()
		config.find('office').text = self.officeInput.GetValue()
		config.find('address1').text = self.address1Input.GetValue()
		config.find('address2').text = self.address2Input.GetValue()
		config.find('address3').text = self.address3Input.GetValue()
		if self.m_radioBox1.GetSelection() == 1:
			config.find('transferMethod').text = "ftp"
		else:
			config.find('transferMethod').text = "network"
		config.find('login').text = self.loginInput.GetValue()
		config.find('transferLocation').text = self.transferLocInput.GetValue()
		config.find('pw').text = base64.b64encode(self.passwordInput.GetValue())
		configString = ET.tostring(config, pretty_print=True)
		file = open("config.xml", "w")
		file.write(configString)
		file.close()
		wx.MessageBox('Default has been updated.', 'Info',  wx.OK | wx.ICON_INFORMATION)	
	
	def descRecord(self, event):
		dirFile = "directory.xml"
		parser = ET.XMLParser(remove_blank_text=True)
		dirParse = ET.parse(dirFile, parser)
		dirXML = dirParse.getroot()
		item = self.descDirCtrl.GetSelection()
		filename = self.descDirCtrl.GetItemText(item)
		self.fileNameText.SetLabel(filename)
		for child in dirXML.iter():
			if 'name' in child.attrib:
				if child.attrib['name'] == filename:
					self.rcdDescInput.SetLabel(self.readXML(child, 'description'))
					self.rcdAccessInput.SetLabel(self.readXML(child, 'access'))

	def itemChecked(self, event):
		dirFile = "directory.xml"
		parser = ET.XMLParser(remove_blank_text=True)
		dirParse = ET.parse(dirFile, parser)
		dirXML = dirParse.getroot()
	
		#function to recursively check all parents in TreeCtrl and XML
		def checkAllParents(item, dirXML):
			parent = self.descDirCtrl.GetItemParent(item)
			while parent != None:
				parentId = self.descDirCtrl.GetPyData(parent)
				if self.descDirCtrl.IsItemChecked(parent) is False:
					self.descDirCtrl.CheckItem(parent, checked=True)
					for record in dirXML.iter():
						if "check" in record.attrib:
							if record.find("id").text == parentId:
								record.set('check', str(self.descDirCtrl.IsItemChecked(parent)))
								descString = ET.tostring(dirXML, pretty_print=True)		
								file = open("directory.xml", "w")
								file.write(descString)
								file.close()
				parent = self.descDirCtrl.GetItemParent(parent)
		
		#function to recursively check or uncheck all children in XML, TreeCtrl uses the AutoCheckChild function
		def checkXMLChildren(itemId, state, dirXML):
			for record in dirXML.iter():
				if "name" in record.attrib:
					if record.find("id").text == itemId:
						for childXML in record.iter():
							if "name" in childXML.attrib:
								childXML.set('check', str(state))
						descString = ET.tostring(dirXML, pretty_print=True)		
						file = open("directory.xml", "w")
						file.write(descString)
						file.close()
		#main part of function
		checked = self.descDirCtrl.GetSelection()
		checkedId = self.descDirCtrl.GetPyData(checked)
		for record in dirXML.iter():
			if "check" in record.attrib:
				if record.find("id").text == checkedId:
					record.attrib['check'] = str(self.descDirCtrl.IsItemChecked(checked))
		if checked == self.root:
			if self.descDirCtrl.IsItemChecked(checked) is True:
				self.descDirCtrl.AutoCheckChild(checked, True)
				checkXMLChildren(checkedId, True, dirXML)
			else:
				self.descDirCtrl.AutoCheckChild(checked, False)
				checkXMLChildren(checkedId, False, dirXML)
		else:
			if self.descDirCtrl.IsItemChecked(checked) is True:
				self.descDirCtrl.AutoCheckChild(checked, True)
				checkXMLChildren(checkedId, True, dirXML)
				checkAllParents(checked, dirXML)
			else:
				self.descDirCtrl.AutoCheckChild(checked, False)
				checkXMLChildren(checkedId, False, dirXML)
		#write the xml directory back to file
		descString = ET.tostring(dirXML, pretty_print=True)		
		file = open("directory.xml", "w")
		file.write(descString)
		file.close()
		
					
	def updateRcrdDesc(self, event):
		dirFile = "directory.xml"
		parser = ET.XMLParser(remove_blank_text=True)
		dirParse = ET.parse(dirFile, parser)
		dirXML = dirParse.getroot()
		desc = self.rcdDescInput.GetValue()
		item = self.descDirCtrl.GetSelection()
		filename = self.descDirCtrl.GetItemText(item)
		for child in dirXML.iter():
			if 'name' in child.attrib:
				if child.attrib['name'] == filename:
					child.find("description").text = desc
		descString = ET.tostring(dirXML, pretty_print=True)
		file = open("directory.xml", "w")
		file.write(descString)
		file.close()
		
	def updateRcrdAccess(self, event):
		dirFile = "directory.xml"
		parser = ET.XMLParser(remove_blank_text=True)
		dirParse = ET.parse(dirFile, parser)
		dirXML = dirParse.getroot()
		access = self.rcdAccessInput.GetValue()
		item = self.descDirCtrl.GetSelection()
		filename = self.descDirCtrl.GetItemText(item)
		for child in dirXML.iter():
			if 'name' in child.attrib:
				if child.attrib['name'] == filename:
					child.find("access").text = access
		descString = ET.tostring(dirXML, pretty_print=True)
		file = open("directory.xml", "w")
		file.write(descString)
		file.close()
		
	def updateNotes(self, event):
		dirFile = "directory.xml"
		parser = ET.XMLParser(remove_blank_text=True)
		dirParse = ET.parse(dirFile, parser)
		dirXML = dirParse.getroot()
		notesText = self.notesInput.GetValue()
		dirXML.find("notes").text = notesText
		descString = ET.tostring(dirXML, pretty_print=True)
		file = open("directory.xml", "w")
		file.write(descString)
		file.close()
		
	def transferFiles(self, event):	
		dirFile = "directory.xml"
		parser = ET.XMLParser(remove_blank_text=True)
		dirParse = ET.parse(dirFile, parser)
		dirXML = dirParse.getroot()
		
		#update accession count
		configXML = "config.xml"
		parser = ET.XMLParser(remove_blank_text=True)
		configParse = ET.parse(configXML, parser)
		config = configParse.getroot()
		config.find("accessionCount").text = str(int(config.find("accessionCount").text) + 1)
		configString = ET.tostring(config, pretty_print=True)
		file = open("config.xml", "w")
		file.write(configString)
		file.close()		
		
		notesText = self.notesInput.GetValue()
		dirXML.find("profile/notes").text = notesText
		creatorText = self.creatorInput.GetValue()
		dirXML.find("profile/creator").text = creatorText
		creatorIdText = self.creatorIdInput.GetValue()
		dirXML.find("profile/creatorId").text = creatorIdText
		donorText = self.donorInput.GetValue()
		dirXML.find("profile/donor").text = donorText
		roleText = self.positionInput.GetValue()
		dirXML.find("profile/role").text = roleText
		emailText = self.emailInput.GetValue()
		dirXML.find("profile/email").text = emailText
		officeText = self.officeInput.GetValue()
		dirXML.find("profile/office").text = officeText
		address1Text = self.address1Input.GetValue()
		dirXML.find("profile/address1").text = address1Text
		address2Text = self.address2Input.GetValue()
		dirXML.find("profile/address2").text = address2Text
		address3Text = self.address3Input.GetValue()
		dirXML.find("profile/address3").text = address3Text
		locationText = self.transferLocInput.GetValue()
		dirXML.find("profile/location").text = locationText
		if self.m_radioBox1.GetSelection() == 1:
			methodText = "ftp"
			dirXML.find("profile/method").text = methodText
		else:
			methodText = "network"
			dirXML.find("profile/method").text = methodText
		
		if methodText == "ftp":
			ftpDemo = wx.MessageDialog(None, 'Demo version. FTP module has not yet been written. \nPlease use Network Path or Local Path to test.', 'FTP Not Available', wx.OK | wx.ICON_EXCLAMATION)
			ftpDemo.ShowModal()
		else:
			if len(locationText) < 1:
				netwError = wx.MessageDialog(None, 'You must enter a local or network path as your transfer destination.', 'Transfer Location Error', wx.OK | wx.ICON_EXCLAMATION)
				netwError.ShowModal()
			else:
				recordsCount = dirXML.xpath("count(//folder|//file)")
				progressGoal = recordsCount + 3
				print "stages: " + str(progressGoal)
				progressMsgRoot = "Packaging your records and transferring them to the archives.\n"
				progressMsg = progressMsgRoot + "Copying Files..."
				networkProcessing = wx.ProgressDialog("ANTS: Archives Network Transfer System", progressMsg, maximum=progressGoal, parent=self, style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
				networkProcessing.ShowModal()
				
				#run forensics tools
				
				
				#make a temp directory and move selected files there
				
				
				#bag directory
			
				
				#update bag manifests
				
				
				#copy bag to destination
				
				progressCount = 0
				newPath = locationText + "\\" + dirXML.attrib["number"]
				shutil.copytree(self.sourceDir, newPath)
				progressCount = progressCount + 1
				progressMsg = progressMsgRoot + "Reading directory..."
				networkProcessing.Update(progressCount, progressMsg)
				
				for record in dirXML.iter():
					if 'name' in record.attrib:
						progressCount = progressCount + 1
						progressMsg = progressMsgRoot + "Reading " + record.attrib['name'] + "..."
						networkProcessing.Update(progressCount, progressMsg)
						#remove uncheck records from XML directory
						if record.attrib["check"] == "False":
							for item in os.listdir(newPath):
								itempath = os.path.join(newPath, item)
								if item == record.attrib["name"]:
									if record.tag == "folder":
										if os.path.isdir(itempath):
											shutil.rmtree(itempath)
									elif record.tag == "file":
										if os.path.isfile(itempath):
											os.remove(itempath)
							record.getparent().remove(record)
							#_____________________________________<---loop stops here for some reason
						#else remove check attribute
						elif record.attrib["check"] == "True":
							record.attrib.pop('check')
						else:
							print "XML DIRECTORY ERROR"
				
				bag = bagit.make_bag(newPath, {'Contact-Name': donorText})	
				progressCount = progressCount + 1
				progressMsg = progressMsgRoot + "Bagging files..."
				networkProcessing.Update(progressCount, progressMsg)
				
				#write XML to file
				descString = ET.tostring(dirXML, pretty_print=True)	
				file = open(locationText + "\\" + dirXML.attrib["number"] + ".xml", "w")
				file.write(descString)
				file.close()
				progressCount = progressCount + 1
				networkProcessing.Destroy()
				
				
				if progressCount >= progressGoal:
					self.Close()

				
	
	
		
		
################################################################################################################	
class spashDialog( wx.Dialog ):
	
	def __init__( self ):
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
		
		self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"ANTS packages and transfers records as files while documenting their authenticity \nand integrity using digital forensics tools. Select a folder to transfer below.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_button1 = wx.Button( self.m_panel1, wx.ID_ANY, u"Browse...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"(C) 2015", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_hyperlink1 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, u"http://library.albany.edu/archive/universityarchives", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		bSizer5.Add( self.m_hyperlink1, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_hyperlink2 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, u"GNU Licence", u"http://www.wxformbuilder.org", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		bSizer4.Add( self.m_hyperlink2, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		
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
	
	
	# Virtual event handlers, overide them in your derived class
	def runANTS( self, event ):
		self.Close()

		
 
#mandatory in wx, create an app, False stands for not deteriction stdin/stdout
#refer manual for details
app = wx.App(False)
 
#create an object of ANTSFrame
frame = ANTSFrame(None)
#show the frame
frame.Show(True)
#start the applications
app.MainLoop()