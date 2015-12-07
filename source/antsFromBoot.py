#importing wx files
import wx
from lxml import etree as ET
import os
import sys
import traceback
import uuid
import base64
import shutil
import datetime
import subprocess
import admin
from transfer import transferModule
 
#import the newly created GUI file
import antsGUI as gui
 
 
#inherit from the MainFrame created in wxFormBuilder and create ANTSFrame
class ANTSFrame(gui.mainFrame):
	#constructor
	def __init__(self, parent):
		
		#checks if booted with admin privileges
		self.adminTest = False
		if not admin.isUserAdmin():
			self.adminTest = False
		else:
			self.adminTest = True
				
		#read config
		try:
			if not os.path.isfile("config.xml"):
				antsConfigXML = ET.Element('antsConfig')
				accessionCount = ET.Element('accessionCount')
				accessionCount.text = "0"
				antsConfigXML.append(accessionCount)
				creatorXML = ET.SubElement(antsConfigXML, 'creator')
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
				receiveLocationXML = ET.SubElement(antsConfigXML, 'receiveLocation')
				loginXML = ET.SubElement(antsConfigXML, 'login')
				pwXML = ET.SubElement(antsConfigXML, 'pw')
				timeZoneXML = ET.SubElement(antsConfigXML, 'timeZone')
				timestampXML = ET.SubElement(antsConfigXML, 'timestampTool')
				compressXML = ET.SubElement(antsConfigXML, 'compress')
				checksumXML = ET.SubElement(antsConfigXML, 'checksum')
				checksumXML.set("default", "true")
				receiptXML = ET.SubElement(antsConfigXML, 'receipt')
				requestEmailXML = ET.SubElement(antsConfigXML, 'requestEmail')
				requestSubjectXML = ET.SubElement(antsConfigXML, 'requestSubject')
				requestBodyXML = ET.SubElement(antsConfigXML, 'requestBody')
				configXMLString = ET.tostring(antsConfigXML, pretty_print=True)
				file = open("config.xml", "w")
				file.write(configXMLString)
				file.close()
			configXML = "config.xml"
			parser = ET.XMLParser(remove_blank_text=True)
			configParse = ET.parse(configXML, parser)
			config = configParse.getroot()
			configData = {"creator": self.readXML(config, "creator"), "creatorId": self.readXML(config, "creatorId"), "donor": self.readXML(config, "donor"), "role": self.readXML(config, "role"), "email": self.readXML(config, "email"), "office": self.readXML(config, "office"), "address1": self.readXML(config, "address1"), "address2": self.readXML(config, "address2"), "address3": self.readXML(config, "address3"), "transferMethod": self.readXML(config, "transferMethod"), "transferLocation": self.readXML(config, "transferLocation"), "receiveLocation": self.readXML(config, "receiveLocation"), "login": self.readXML(config, "login"), "password": base64.b64decode(self.readXML(config, "pw")), "timestampTool": self.readXML(config, "timestampTool"), "timeZone": self.readXML(config, "timeZone"), "compress": self.readXML(config, "compress"), "checksum": self.readXML(config, "checksum"), "receipt": self.readXML(config, "receipt")}
			if "default" in config.find('compress').attrib:
				configData.update({"compressDefault": config.find('compress').attrib["default"]})
		except:
			exceptMsg = traceback.format_exc()
			self.errorDialog("Failed to read config.xml.", exceptMsg)
			
		def readDirectory():
			#initial directory selection
			try:
				dialogBrowse = wx.DirDialog(None, "Choose a folder to transfer:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
				if dialogBrowse.ShowModal() == wx.ID_OK:
					self.sourceDir = dialogBrowse.GetPath()
				else:
					os._exit(1)
				dialogBrowse.Destroy()
			except:
				exceptMsg = traceback.format_exc()
				self.errorDialog("Failed to browse for directory.", exceptMsg,)

			#read directory to ~directory.xml with updated accession count from config.xml
			try:
				rootXML = ET.Element('accession')
				if config.find('accessionCount') is None:
					config.find('accessionCount').text = "0"
				elif config.find('accessionCount').text:
					pass
				else:
					config.find('accessionCount').text = "0"
				accessionCount = int(config.find('accessionCount').text) + 1
				donorNormal = self.readXML(config, "donor").lower().strip().replace(" ", "_")
				rootXML.set('number', self.readXML(config, "creatorId") + "-" + donorNormal + "-" + str(accessionCount))
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
				folderXML.set('name', os.path.basename(self.sourceDir))
				folderXML.set('check', 'True')
				folderId = ET.SubElement(folderXML, "id")
				folderId.text = str(uuid.uuid4())
				folderPath = ET.SubElement(folderXML, "path")
				folderPath.text = self.sourceDir
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
							pathXML = ET.SubElement(itemXML, "path")
							pathXML.text = itempath
							descXML = ET.SubElement(itemXML, "description")
							accessXML = ET.SubElement(itemXML, "access")
							dir2XML(os.path.join(path, item), itemXML)
						elif os.path.isfile(itempath):
							itemXML = ET.SubElement(root, "file")
							itemXML.set('name', item)
							itemXML.set('check', "True")
							idXML = ET.SubElement(itemXML, "id")
							idXML.text = str(uuid.uuid4())
							pathXML = ET.SubElement(itemXML, "path")
							pathXML.text = itempath
							descXML = ET.SubElement(itemXML, "description")
							accessXML = ET.SubElement(itemXML, "access")
				dir2XML(self.sourceDir, folderXML)
				dirXMLString = ET.tostring(rootXML, pretty_print=True)
				file = open("~directory.xml", "w")
				file.write(dirXMLString)
				file.close()
			except:
				exceptMsg = traceback.format_exc()
				self.errorDialog("Could not read the directory you selected", exceptMsg,)
			
	
		#check for old accession info from last error
		if os.path.isfile("~directory.xml"):
			tryRefresh = wx.MessageDialog(None, "Found transfer information from last transfer. This may be from an aborted transfer. Would you like to attempt to retry the last transfer.", "Refresh Last Transfer?", wx.YES_NO | wx.ICON_INFORMATION)
			refreshResult = tryRefresh.ShowModal()
			if refreshResult == wx.ID_YES:
				#check to see if ~directory.xml is still valid
				parser = ET.XMLParser(remove_blank_text=True)
				dirParse = ET.parse("~directory.xml", parser)
				refDirectory = dirParse.getroot()
				self.noItemCount = 0
				pathIndex = []
				#check that every file and folder listed in XML is present
				for item in refDirectory.iter():
					if "name" in item.attrib:
						#creates simple index to check files
						pathIndex.append(item.find("path").text)
						itemPath = item.find("path").text
						if item.tag == "folder":
							if not os.path.isdir(itemPath):
								self.noItemCount = self.noItemCount + 1
						elif item.tag =="file":
							if not os.path.isfile(itemPath):
								self.noItemCount = self.noItemCount + 1
						else:
							self.noItemCount = self.noItemCount + 1
				#check that every file and folder in directory is in ~directory.xml
				oldSource = refDirectory.find("folder/path").text
				def matchXML(rootDir):
					for item in os.listdir(rootDir):
						itemPath = os.path.join(rootDir, item)
						if os.path.isfile(itemPath):
							if not itemPath in pathIndex:
								self.noItemCount = self.noItemCount + 1
						elif os.path.isdir(itemPath):
							if not itemPath in pathIndex:
								self.noItemCount = self.noItemCount + 1
							matchXML(itemPath)
				matchXML(oldSource)
				if self.noItemCount == 0:
					#~directory.xml is good
					self.sourceDir = refDirectory.find("folder/path").text
				else:
					#there is a problem with ~directory.xml
					refreshError = wx.MessageDialog(None, "Could not verify that all the files from the last transfer are still present in their original location. Transfer directory must be exactly the same as last transfer to restore data. ANTS is unable to retry the last transfer. Please select a directory and start the transfer from the beginning.", "Failed To Retry Last Transfer", wx.OK | wx.ICON_ERROR)
					refreshError.ShowModal()
					readDirectory()
			else:
				#use does not want to retry last transfer
				readDirectory()
		else:
			#no previous ~directory.xml file found
			readDirectory()
			
			
		#initialize parent class
		try:
			gui.mainFrame.__init__(self, parent, configData, self.sourceDir)
		except:
			exceptMsg = traceback.format_exc()
			self.errorDialog("Could not load GUI", exceptMsg)
 
	#Runs the transferModule to package and move SIP
	def transferFiles(self, event):
		try:
			transferModule(self)
		except:
			#error Dialog that doesn't close ANTS
			print "transfer Failed"
			exceptMsg = traceback.format_exc()
			print exceptMsg
			errorOutput = "\n" + "#############################################################\n" + str(datetime.datetime.now()) + "\n#############################################################\n" + str(exceptMsg) + "\n********************************************************************************"
			file = open("errorLog.txt", "a")
			file.write(errorOutput)
			file.close()
			self.progressBar.Destroy()
			errorPopup = wx.MessageDialog(None, "Transfer Failed" + "\n\n" + str(exceptMsg), "ERROR", wx.OK | wx.ICON_ERROR)
			errorPopup.ShowModal()
	
	def errorDialog(self, errorMsg, exceptMsg):
		#Error message that deletes directory info, cannot retry transfer with same data
		errorOutput = "\n" + "#############################################################\n" + str(datetime.datetime.now()) + "\n#############################################################\n" + str(exceptMsg) + "\n********************************************************************************"
		print exceptMsg
		file = open("errorLog.txt", "a")
		file.write(errorOutput)
		file.close()
		if os.path.isfile("~directory.xml"):
			os.remove("~directory.xml")
		errorPopup = wx.MessageDialog(None, errorMsg + "\n\n" + str(exceptMsg), "ERROR", wx.OK | wx.ICON_ERROR)
		errorPopup.ShowModal()
		sys.exit()
		
	def errorMessage(self, errorMsg, exceptMsg):
		#Error message that keeps directory info, enables retry of transfer with same data
		errorOutput = "\n" + "#############################################################\n" + str(datetime.datetime.now()) + "\n#############################################################\n" + str(exceptMsg) + "\n********************************************************************************"
		print exceptMsg
		file = open("errorLog.txt", "a")
		file.write(errorOutput)
		file.close()
		errorPopup = wx.MessageDialog(None, errorMsg + "\n\n" + str(exceptMsg), "ERROR", wx.OK | wx.ICON_ERROR)
		errorPopup.ShowModal()
		sys.exit()
	
	def closeANTS(self, event):
		self.Destroy()
	
	def readXML(self, element, field):
		if element.find(field).text:
			value = element.find(field).text
		else:
			value =""
		return value
	
	def updateConfig(self, event):
		sureUpdate = wx.MessageDialog(None, 'Are your sure you want to update the default configuration?', 'Update Default Configuration', wx.YES_NO | wx.ICON_QUESTION)
		updateResult = sureUpdate.ShowModal()
		if updateResult == wx.ID_YES:
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
			config.find('receiveLocation').text = self.receiveInput.GetValue()
			config.find('pw').text = base64.b64encode(self.passwordInput.GetValue())
			if self.timeZoneOption.GetSelection() == 0:
				config.find('timeZone').text = "utc"
			else:
				config.find('timeZone').text = "local"
			if self.timestampOption.GetSelection() == 0:
				config.find('timestampTool').text = "os.stat"
			else:
				config.find('timestampTool').text = "plaso"
			if self.compressOption.GetSelection() == 0:
				config.find('compress').text = "zip"
			else:
				config.find('compress').text = "gzip"
			if self.hashOption.GetSelection() == 0:
				config.find('checksum').text = "md5"
			else:
				config.find('checksum').text = "sha256"
			if self.receiptOption.GetSelection() == 0:
				config.find('receipt').text = "html"
			elif self.receiptOption.GetSelection() == 1:
				config.find('receipt').text = "csv"
			else:
				config.find('receipt').text = "xml"
			configString = ET.tostring(config, pretty_print=True)
			file = open("config.xml", "w")
			file.write(configString)
			file.close()
			wx.MessageBox('Default has been updated.', 'Info',  wx.OK | wx.ICON_INFORMATION)	
	
	def descRecord(self, event):
		dirFile = "~directory.xml"
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
		dirFile = "~directory.xml"
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
								file = open("~directory.xml", "w")
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
						file = open("~directory.xml", "w")
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
		file = open("~directory.xml", "w")
		file.write(descString)
		file.close()
		
					
	def updateRcrdDesc(self, event):
		dirFile = "~directory.xml"
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
		file = open("~directory.xml", "w")
		file.write(descString)
		file.close()
		
	def updateRcrdAccess(self, event):
		dirFile = "~directory.xml"
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
		file = open("~directory.xml", "w")
		file.write(descString)
		file.close()
		
	def accessOptions(self, event):
		#access concerns written by Chris Prom, "Email Transfer Form" on his blog Practical E-Records:  http://e-records.chrisprom.com/email-transfer-form/#more-2809
		options = ['Student records protected by FERPA', 'Personnel or employment records', 'Protected intellectual property or reseach', 'Records protected by attorney client privilege', 'Social Security numbers, Passwords or PINs', 'Credit Card numbers', 'Financial records', 'Medical records/HIPPA protected records', 'Licensed or pirated software', 'Other materials that have privacy concerns (please specify)']
		recordName = self.fileNameText.GetLabel()
		optionsMenu = wx.MultiChoiceDialog( self, recordName + " might contain:", "Access Concerns for this Record", options)
		if optionsMenu.ShowModal() == wx.ID_OK:
			selections = optionsMenu.GetSelections()
			selectionList = []
			for selection in selections:
				selectionText = options[selection]
				selectionList.append(selectionText)
			selectionsOutput = ", \n".join(selectionList)
			self.rcdAccessInput.AppendText(selectionsOutput)
					
	def testLocation(self, event):
		location = self.transferLocInput.GetValue()
		if not len(location) > 0:
			noLoc = wx.MessageDialog(None, 'You must enter a local or network path as your transfer destination.', 'Location Test Error', wx.OK | wx.ICON_ERROR)
			noLoc.ShowModal()
		else:
			if self.m_radioBox1.GetSelection() == 0:
				if os.path.isdir(location):
					goodDir = wx.MessageDialog(None, 'The directory you entered is correct.', 'Found Directory', wx.OK | wx.ICON_INFORMATION)
					goodDir.ShowModal()
				else:
					badDir = wx.MessageDialog(None, 'Invalid location, did not find the directory you entered.', 'Incorrect Directory', wx.OK | wx.ICON_EXCLAMATION)
					badDir.ShowModal()
			else:
				print location
				
	def testRecieveLocation(self, event):
		location = self.receiveInput.GetValue()
		if not len(location) > 0:
			noLoc = wx.MessageDialog(None, 'You must enter a local or network path as your transfer destination.', 'Location Test Error', wx.OK | wx.ICON_ERROR)
			noLoc.ShowModal()
		else:
			if self.m_radioBox1.GetSelection() == 0:
				if os.path.isdir(location):
					goodDir = wx.MessageDialog(None, 'The directory you entered is correct.', 'Found Directory', wx.OK | wx.ICON_INFORMATION)
					goodDir.ShowModal()
				else:
					badDir = wx.MessageDialog(None, 'Invalid location, did not find the directory you entered.', 'Incorrect Directory', wx.OK | wx.ICON_EXCLAMATION)
					badDir.ShowModal()
			else:
				print location
	
	def updateNotes(self, event):
		dirFile = "~directory.xml"
		parser = ET.XMLParser(remove_blank_text=True)
		dirParse = ET.parse(dirFile, parser)
		dirXML = dirParse.getroot()
		notesText = self.notesInput.GetValue()
		dirXML.find("notes").text = notesText
		descString = ET.tostring(dirXML, pretty_print=True)
		file = open("~directory.xml", "w")
		file.write(descString)
		file.close()
		
	def buildReceipt(self, event):
		import tempfile
		tempDir = tempfile.mkdtemp()
		if self.receiptOption.GetSelection() == 1:
			import csv
			headLine = ["accession", "submitted", "type", "name", "path", "id"]
			tempCSV = open(os.path.join(tempDir, 'receipt.csv'), 'wb')
			csv = csv.writer(tempCSV)
			csv.writerow(headLine)
			parser = ET.XMLParser(remove_blank_text=True)
			receiptParse = ET.parse("receipt.xml", parser)
			receiptXML = receiptParse.getroot()
			for accession in receiptXML:
				number = accession.attrib['number']
				submitted = accession.attrib['submitted']
				for item in accession:
					if item.tag == "item":
						itemList = [number, submitted, item.find('type').text, item.find('name').text, item.find('path').text, item.find('id').text]
						csv.writerow(itemList)
			tempCSV.close()
			receiptFile = os.path.join(tempDir, "receipt.csv")
			wildcard = "*.csv"
			defaultFile = "receipt.csv"
		elif self.receiptOption.GetSelection() == 2:
			shutil.copy2("receipt.xml", tempDir)
			receiptFile = os.path.join(tempDir, "receipt.xml")
			wildcard = "*.xml"
			defaultFile = "receipt.xml"
		else:
			from html import htmlReceipt
			htmlString = htmlReceipt("receipt.xml", str(datetime.datetime.now()), "config.xml")
			htmlFile = open(os.path.join(tempDir, "receipt.html"), "w")
			htmlFile.write(htmlString)
			htmlFile.close()
			receiptFile = os.path.join(tempDir, "receipt.html")
			wildcard = "*.htm;*.html"
			defaultFile = "receipt.html"
		return receiptFile, wildcard, defaultFile
	
	def viewReceipt(self, event):
		if not os.path.isfile("receipt.xml"):
			noReceipt = wx.MessageDialog(None, 'Unable to find a receipt. You must tranfer files in order to obtain a receipt.', 'Ne Receipt found', wx.OK | wx.ICON_WARNING)
			noReceipt.ShowModal()
		else:
			receiptFile,  wildcard, defaultFile = self.buildReceipt(self)
			subprocess.Popen(receiptFile, shell=True)
		
	def saveReceipt(self, event):
		if not os.path.isfile("receipt.xml"):
			noReceipt = wx.MessageDialog(None, 'Unable to find a receipt. You must tranfer files in order to obtain a receipt.', 'Ne Receipt found', wx.OK | wx.ICON_WARNING)
			noReceipt.ShowModal()
		else:
			receiptFile, wildcard, defaultFile = self.buildReceipt(self)
			saveFile = wx.FileDialog(self, message="Save receipt as ...", defaultFile=defaultFile, wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT )
			if saveFile.ShowModal() == wx.ID_OK:
				path = saveFile.GetPath()
				shutil.copy2(receiptFile, path)
			saveFile.Destroy()
		
	def get_size(self, dir):
		total_size = 0
		for dirpath, dirnames, filenames in os.walk(dir):
			for f in filenames:
				fp = os.path.join(dirpath, f)
				total_size += os.path.getsize(fp)
		return total_size
		
 
#mandatory in wx, create an app, False stands for not deteriction stdin/stdout
#refer manual for details
app = wx.App(False)
 
#create an object of ANTSFrame
frame = ANTSFrame(None)
#show the frame
frame.Show(True)
#start the applications
app.MainLoop()