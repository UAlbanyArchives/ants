#importing wx files
import wx
from lxml import etree as ET
import os
import sys
import traceback
import uuid
import base64
import shutil
import bagit
import zipfile
import datetime
import subprocess

 
#import the newly created GUI file
import antsGUI as gui
 
 
#inherit from the MainFrame created in wxFormBuilder and create ANTSFrame
class ANTSFrame(gui.mainFrame):
	#constructor
	def __init__(self, parent):
	
	
		#Splash screen/browse instructions
		try:
			splashDialog = spashDialog()
			splashDialog.ShowModal()
		except:
			exceptMsg = traceback.format_exc()
			self.errorDialog("Could not load splash dialog", exceptMsg)
	
		#initial directory selection
		dialogBrowse = wx.DirDialog(None, "Choose a folder to transfer:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
		if dialogBrowse.ShowModal() == wx.ID_OK:
			sourceDir = dialogBrowse.GetPath()
		else:
			sys.exit()
		dialogBrowse.Destroy()
		
		#read config
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
			compressXML = ET.SubElement(antsConfigXML, 'compress')
			checksumXML = ET.SubElement(antsConfigXML, 'checksum')
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
		configData = {"creator": self.readXML(config, "creator"), "creatorId": self.readXML(config, "creatorId"), "donor": self.readXML(config, "donor"), "role": self.readXML(config, "role"), "email": self.readXML(config, "email"), "office": self.readXML(config, "office"), "address1": self.readXML(config, "address1"), "address2": self.readXML(config, "address2"), "address3": self.readXML(config, "address3"), "transferMethod": self.readXML(config, "transferMethod"), "transferLocation": self.readXML(config, "transferLocation"), "receiveLocation": self.readXML(config, "receiveLocation"), "login": self.readXML(config, "login"), "password": base64.b64decode(self.readXML(config, "pw")), "compress": self.readXML(config, "compress"), "checksum": self.readXML(config, "checksum"), "receipt": self.readXML(config, "receipt")}

		
		#read directory
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
			folderXML.set('name', os.path.basename(sourceDir))
			folderXML.set('check', 'True')
			folderId = ET.SubElement(folderXML, "id")
			folderId.text = str(uuid.uuid4())
			folderPath = ET.SubElement(folderXML, "path")
			folderPath.text = sourceDir
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
			dir2XML(sourceDir, folderXML)
			dirXMLString = ET.tostring(rootXML, pretty_print=True)
			file = open("directory.xml", "w")
			file.write(dirXMLString)
			file.close()
		except:
			exceptMsg = traceback.format_exc()
			self.errorDialog("Could not read the directory you selected", exceptMsg,)
				
		
		#initialize parent class
		try:
			gui.mainFrame.__init__(self, parent, configData, sourceDir)
		except:
			exceptMsg = traceback.format_exc()
			self.errorDialog("Could not load GUI", exceptMsg)
 
	def errorDialog(self, errorMsg, exceptMsg):
		#except line is wrong
		errorOutput = "\n" + str(exceptMsg) + "\n********************************************************************************"
		print exceptMsg
		file = open("errorLog.txt", "a")
		file.write(errorOutput)
		file.close()
		errorPopup = wx.MessageDialog(None, errorMsg + "\n\n" + str(exceptMsg), "ERROR", wx.OK | wx.ICON_ERROR)
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
		config.find('receiveLocation').text = self.receiveInput.GetValue()
		config.find('pw').text = base64.b64encode(self.passwordInput.GetValue())
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
		
	def accessOptions(self, event):
		#access concerns written by Chris Prom, "Email Transfer From" on his blog Practical E-Records:  http://e-records.chrisprom.com/email-transfer-form/#more-2809
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
		receiptFile,  wildcard, defaultFile = self.buildReceipt(self)
		subprocess.Popen(receiptFile, shell=True)
		
	def saveReceipt(self, event):
		receiptFile, wildcard, defaultFile = self.buildReceipt(self)
		saveFile = wx.FileDialog(self, message="Save receipt as ...", defaultFile=defaultFile, wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT )
		if saveFile.ShowModal() == wx.ID_OK:
			path = saveFile.GetPath()
			shutil.copy2(receiptFile, path)
		saveFile.Destroy()
		
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
			elif not os.path.isdir(locationText):
				netwError = wx.MessageDialog(None, 'The network or location path you entered does not exist.', 'Transfer Location Error', wx.OK | wx.ICON_EXCLAMATION)
				netwError.ShowModal()
			else:
				recordsCount = dirXML.xpath("count(//folder[@check='True']|//file[@check='True'])")
				progressGoal = recordsCount + 10
				print "stages: " + str(progressGoal)
				
				self.progressCount = 0
				self.progressMsgRoot = "Packaging your records and transferring them to the archives.\n"
				self.progressMsg = self.progressMsgRoot
				self.networkProcessing = wx.ProgressDialog("ANTS: Archives Network Transfer System", self.progressMsg, maximum=progressGoal, parent=self, style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
				self.networkProcessing.ShowModal()
				
				#moves directory while updating progress dialog for every file and folder
				def countCopy(source, destination, dirXML):
					for item in os.listdir(source):
						path = os.path.join(source, item)
						if path != destination:
							pathFromSource = path.split(self.sourceDir + "\\")[1]
							pathList = pathFromSource.split("\\")
							pathLength = len(pathList)
							pathString = "/accession/folder[@name='" + dirXML.find('folder').attrib['name'] + "']"
							for pathPart in pathList:
								if pathPart != pathList[pathLength - 1]:
									pathString = pathString +  "/folder[@name=\"" + pathPart + "\"]"
								else:
									if os.path.isdir(path):
										pathString = pathString +  "/folder[@name=\"" + pathPart + "\"]"
									else:
										pathString = pathString +  "/file[@name=\"" + pathPart + "\"]"							
							itemXML = dirXML.xpath(pathString)[0]
							if itemXML.attrib['check'] == "True":							
								if os.path.isdir(path):
									self.progressMsg = self.progressMsgRoot + "Gathering " + item
									self.networkProcessing.Update(self.progressCount, self.progressMsg)
									os.makedirs(os.path.join(destination, item))
									shutil.copystat(path, os.path.join(destination, item))
									self.progressCount = self.progressCount + 1
									self.networkProcessing.Update(self.progressCount, self.progressMsg)
									countCopy(path, os.path.join(destination, item), dirXML)
								elif os.path.isfile(path):
									self.progressMsg = self.progressMsgRoot + "Gathering " + item
									self.networkProcessing.Update(self.progressCount, self.progressMsg)
									shutil.copy2(path, destination)
									self.progressCount = self.progressCount + 1
									self.networkProcessing.Update(self.progressCount, self.progressMsg)
								else:
									print "error: " + path
				
				#run forensics tools
				try:
					self.progressMsg = self.progressMsgRoot + "Gathering metadata..."
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
					#do stuff
					self.progressCount = self.progressCount + 1
				except:
					exceptMsg = traceback.format_exc()
					if os.path.isfile("directory.xml"):
						os.remove("directory.xml")
					self.errorDialog("Failed to run forensics tools.", exceptMsg)
				
				#move files to new directory
				try:
					self.progressMsg = self.progressMsgRoot + "Gathering files..."
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
					accessionNumber = dirXML.attrib['number']
					os.makedirs(os.path.join(self.sourceDir, accessionNumber))
					bagDir = os.path.join(self.sourceDir, accessionNumber)
					countCopy(self.sourceDir, bagDir, dirXML)
				except:
					exceptMsg = traceback.format_exc()
					if os.path.isdir(bagDir):
						shutil.rmtree(bagDir)
					if os.path.isfile("directory.xml"):
						os.remove("directory.xml")
					self.errorDialog("Failed to move files to new directory.", exceptMsg)
				
				#bag directory
				try:
					self.progressMsg = self.progressMsgRoot + "Bagging files..."
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
					bagInfo = {'Contact-Name': donorText}
					if self.hashOption.GetSelection() == 0:
						bag = bagit.make_bag(bagDir, bagInfo)
					elif self.hashOption.GetSelection() == 1:
						bag = bagit.make_bag(bagDir, bagInfo, 1, ['sha256'])
					else:
						raise ValueError("Unable to read checksum selection.")
					self.progressCount = self.progressCount + 1
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
				except:
					exceptMsg = traceback.format_exc()
					if os.path.isdir(bagDir):
						shutil.rmtree(bagDir)
					if os.path.isfile("directory.xml"):
						os.remove("directory.xml")
					self.errorDialog("Failed to bag files.", exceptMsg)
				
				#write to receipt
				try:
					self.progressMsg = self.progressMsgRoot + "Writing receipt..."
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
					if os.path.isfile("receipt.xml"):
						parser = ET.XMLParser(remove_blank_text=True)
						recriptParse = ET.parse("receipt.xml", parser)
						receiptRoot = recriptParse.getroot()
					else:
						receiptRoot = ET.Element('receipt')
					accessionXML = ET.Element("accession")
					accessionXML.set('number', dirXML.attrib['number'])
					receiptRoot.append(accessionXML)
					accessionXML.append(dirXML.find("profile"))
					for item in dirXML.iter():
						if "name" in item.attrib:
							if item.attrib['check'] == "True":
								itemXML = ET.Element('item')
								typeXML = ET.SubElement(itemXML, 'type')
								typeXML.text = item.tag
								nameXML = ET.SubElement(itemXML, 'name')
								nameXML.text = item.attrib['name']
								pathXML = ET.SubElement(itemXML, 'path')
								pathXML.text = item.find("path").text
								idXML = ET.SubElement(itemXML, 'id')
								idXML.text = item.find('id').text
								accessionXML.append(itemXML)
					self.progressCount = self.progressCount + 1
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
				except:
					exceptMsg = traceback.format_exc()
					if os.path.isdir(bagDir):
						shutil.rmtree(bagDir)
					if os.path.isfile("directory.xml"):
						os.remove("directory.xml")
					self.errorDialog("Failed to write receipt", exceptMsg)
				
				
				#remove unwanted files from XML
				try:
					self.progressMsg = self.progressMsgRoot + "Removing records of unwanted files..."
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
					for record in dirXML.iter():
						if 'name' in record.attrib:
							#remove uncheck records from XML directory
							if record.attrib["check"] == "False":
								record.getparent().remove(record)
							#else remove check attribute
							elif record.attrib["check"] == "True":
								record.attrib.pop('check')
							else:
								raise  ValueError("XML DIRECTORY ERROR, @check for " + record.attrib["name"] + " is not True or False.")
					self.progressCount = self.progressCount + 1
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
				except:
					exceptMsg = traceback.format_exc()
					if os.path.isdir(bagDir):
						shutil.rmtree(bagDir)
					if os.path.isfile("directory.xml"):
						os.remove("directory.xml")
					self.errorDialog("Failed to remove unwanted files from XML", exceptMsg)
							
				#write XML to file and update bag manifests
				try:
					self.progressMsg = self.progressMsgRoot + "Writing metadata and finalizing manifests..."
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
					#write submission time to XML
					dirXML.set('submitted', str(datetime.datetime.now()))
					#write submission time to receipt
					accessionXML.set('submitted', dirXML.attrib['submitted'])
					descString = ET.tostring(dirXML, pretty_print=True)	
					file = open(bagDir + "\\" + dirXML.attrib["number"] + ".xml", "w")
					file.write(descString)
					file.close()
					bag.save(manifests=True)
					self.progressCount = self.progressCount + 1
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
				except:
					exceptMsg = traceback.format_exc()
					if os.path.isdir(bagDir):
						shutil.rmtree(bagDir)
					if os.path.isfile("directory.xml"):
						os.remove("directory.xml")
					self.errorDialog("Failed to write XML to file and update bag manifests.", exceptMsg)
				
				#compress bag?
				try:
					if self.compressCheck.IsChecked() is True:
						self.progressMsg = self.progressMsgRoot + "Compressing data..."
						self.networkProcessing.Update(self.progressCount, self.progressMsg)
						if self.compressOption.GetSelection() == 0:
							finalPackage = shutil.make_archive(bagDir, 'zip', bagDir)
						elif self.compressOption.GetSelection() == 1:
							finalPackage = shutil.make_archive(bagDir, 'gztar', bagDir)
						else:
							raise ValueError("Unable to read compression selection.")
						shutil.rmtree(bagDir)
						self.progressCount = self.progressCount + 1
						self.networkProcessing.Update(self.progressCount, self.progressMsg)
					else:
						finalPackage = bagDir
				except:
					exceptMsg = traceback.format_exc()
					if os.path.isdir(bagDir):
						shutil.rmtree(bagDir)
					if os.path.isfile("directory.xml"):
						os.remove("directory.xml")
					self.errorDialog("Failed to compress bag.", exceptMsg)
				
				
				#copy bag to destination
				try:
					self.progressMsg = self.progressMsgRoot + "Transfering to the Archives..."
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
					if os.path.isdir(finalPackage):
						#copyCmd = "xcopy \"" + finalPackage + "\" \"" + os.path.join(locationText, accessionNumber) + "\""
						#print copyCmd
						#proc = subprocess.Popen(copyCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						shutil.copytree(finalPackage, locationText)
						shutil.rmtree(finalPackage)
					elif os.path.isfile(finalPackage):
						shutil.copy2(finalPackage, locationText)
						os.remove(finalPackage)
					self.progressCount = self.progressCount + 1
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
				except:
					exceptMsg = traceback.format_exc()
					if os.path.isdir(finalPackage):
						shutil.rmtree(finalPackage)
					if os.path.isfile("directory.xml"):
						os.remove("directory.xml")
					self.errorDialog("Failed to copy bag to destination.", exceptMsg)
				
				
				#write receipt to file
				try:
					receiptString = ET.tostring(receiptRoot, pretty_print=True)	
					file = open("receipt.xml", "w")
					file.write(receiptString)
					file.close()
					os.remove("directory.xml")
					self.progressCount = self.progressCount + 1
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
				except:
					exceptMsg = traceback.format_exc()
					if os.path.isfile("directory.xml"):
						os.remove("directory.xml")
					self.errorDialog("Failed to write to receipt to file", exceptMsg)
				
				
				if self.progressCount >= progressGoal:
					self.Close()
				else:
					print "didn't reach processGoal"
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
		
		self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"ANTS gathers metadata and packages files for transfer to an institutional archives.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Select a folder to transfer.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText3.Wrap( -1 )
		bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		bSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer22.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		self.m_button1 = wx.Button( self.m_panel1, wx.ID_ANY, u"Browse...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.m_button1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		self.m_button2 = wx.Button( self.m_panel1, wx.ID_ANY, u"View Receipt", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.m_button2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		bSizer22.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		bSizer2.Add( bSizer22, 1, wx.EXPAND, 5 )
		
		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"(C) 2015", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
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
		
		self.m_hyperlink3 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, u"Credits", wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		bSizer48.Add( self.m_hyperlink3, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_hyperlink2 = wx.HyperlinkCtrl( self.m_panel1, wx.ID_ANY, u"Licence", wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		bSizer49.Add( self.m_hyperlink2, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_button2.Bind( wx.EVT_BUTTON, self.viewReceipt )
		self.m_hyperlink2.Bind( wx.EVT_HYPERLINK, self.openLicence)
		self.m_hyperlink3.Bind( wx.EVT_HYPERLINK, self.openCredits)
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
		parser = ET.XMLParser(remove_blank_text=True)
		configParse = ET.parse("config.xml", parser)
		configXML = configParse.getroot()
		import tempfile
		tempDir = tempfile.mkdtemp()
		if configXML.find("receipt").text.lower().strip() == "csv":
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
			subprocess.Popen(os.path.join(tempDir, "receipt.csv"), shell=True)
		elif configXML.find("receipt").text.lower().strip() == "xml":
			shutil.copy2("receipt.xml", tempDir)
			subprocess.Popen(os.path.join(tempDir, "receipt.xml"), shell=True)
		else:
			from html import htmlReceipt
			htmlString = htmlReceipt("receipt.xml", str(datetime.datetime.now()), "config.xml")
			htmlFile = open(os.path.join(tempDir, "receipt.html"), "w")
			htmlFile.write(htmlString)
			htmlFile.close()
			subprocess.Popen(os.path.join(tempDir, "receipt.html"), shell=True)
	
	def openLicence(self, event):
		os.system("LICENSE.txt")
	
	def openCredits(self, event):
		wx.MessageBox('Credits here', 'Info',  wx.OK | wx.ICON_INFORMATION)
		
	def closeProgram(self, event):
		sys.exit()
	
	
	# Virtual event handlers, overide them in your derived class
	def runANTS( self, event ):
		self.Destroy()

		
 
#mandatory in wx, create an app, False stands for not deteriction stdin/stdout
#refer manual for details
app = wx.App(False)
 
#create an object of ANTSFrame
frame = ANTSFrame(None)
#show the frame
frame.Show(True)
#start the applications
app.MainLoop()