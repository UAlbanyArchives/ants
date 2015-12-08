import wx
from lxml import etree as ET
import os
import traceback
import shutil
import datetime
import subprocess
import admin
import bagit
import zipfile
import copy


def transferModule(self):
	
	######################################################################################################################
	
	def packageSIP(pathTransfer, dirXML):
		
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
		
		#read options from GUI
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
		
		#check transfer location, ask to create
		if pathTransfer == True:
			if len(locationText) < 1:
				netwError = wx.MessageDialog(None, 'You must enter a local or network path as your transfer destination.', 'Transfer Location Error', wx.OK | wx.ICON_EXCLAMATION)
				netwError.ShowModal()
			elif not os.path.isdir(locationText):
				netwError = wx.MessageDialog(None, "The network or location path \"" + locationText + "\" does not exist. Would you like to try to create this directory?", "Transfer Location Not Found", wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)
				if netwError.ShowModal() == wx.ID_YES:
					try:
						os.makedirs(locationText)
						pathTransfer = True
					except:
						exceptMsg = traceback.format_exc()
						self.errorMessage("Unable to create directory.", exceptMsg)
				else:
					raise ValueError("No destination path entered, please enter a destination in the Options tab.")
		else:
			if len(locationText) < 1:
				netwError = wx.MessageDialog(None, 'You must enter a FTP URL your transfer destination.', 'Transfer Location Error', wx.OK | wx.ICON_EXCLAMATION)
				netwError.ShowModal()
				raise ValueError("No FTP URL entered, please enter a destination in the Options tab.")
			
		
		#setup Progress Dialog
		totalCount = dirXML.xpath("count(//folder|//file)")
		recordsCount = dirXML.xpath("count(//folder[@check='True']|//file[@check='True'])")
		print "Total folders and files: " + str(recordsCount)
		if self.compressCheck.IsChecked() is False:
			progressGoal = recordsCount + recordsCount + 11
		else:
			progressGoal = recordsCount + 7
		if self.adminTest == True:
			progressGoal = progressGoal + totalCount
		else:
			progressGoal = progressGoal + 1
		print "Anticipated stages: " + str(progressGoal)
		self.progressCount = 0
		self.progressMsgRoot = "Packaging your records and transferring them to the archives.\n"
		self.progressMsg = self.progressMsgRoot
		self.progressBar = wx.ProgressDialog("ANTS: Archives Network Transfer System", self.progressMsg, maximum=progressGoal, parent=self, style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
		self.progressBar.ShowModal()
		
			
		#moves directory for each selection in XML while updating progress dialog for every file and folder
		def countCopyXML(source, destination, dirXML):
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
							self.progressBar.Update(self.progressCount, self.progressMsg)
							os.makedirs(os.path.join(destination, item))
							shutil.copystat(path, os.path.join(destination, item))
							self.progressCount = self.progressCount + 1
							self.progressBar.Update(self.progressCount, self.progressMsg)
							countCopyXML(path, os.path.join(destination, item), dirXML)
						elif os.path.isfile(path):
							self.progressMsg = self.progressMsgRoot + "Gathering " + item
							self.progressBar.Update(self.progressCount, self.progressMsg)
							shutil.copy2(path, destination)
							self.progressCount = self.progressCount + 1
							self.progressBar.Update(self.progressCount, self.progressMsg)
						else:
							print "error: " + path
		
		#run forensics tools
		try:
			self.progressMsg = self.progressMsgRoot + "Gathering metadata..."
			self.progressBar.Update(self.progressCount, self.progressMsg)
			from recordEvents import recordEvents
			dirXML = recordEvents(self, dirXML)
			self.progressCount = self.progressCount + 1
		except:
			exceptMsg = traceback.format_exc()
			self.errorMessage("Failed to run forensics tools.", exceptMsg)
		
		#move files to new directory
		try:
			self.progressMsg = self.progressMsgRoot + "Gathering files..."
			self.progressBar.Update(self.progressCount, self.progressMsg)
			accessionNumber = dirXML.attrib['number']
			os.makedirs(os.path.join(self.sourceDir, accessionNumber))
			bagDir = os.path.join(self.sourceDir, accessionNumber)
			countCopyXML(self.sourceDir, bagDir, dirXML)
		except:
			exceptMsg = traceback.format_exc()
			if os.path.isdir(bagDir):
				shutil.rmtree(bagDir)
			self.errorMessage("Failed to move files to new directory.", exceptMsg)
		
		#bag directory
		try:
			self.progressMsg = self.progressMsgRoot + "Bagging files..."
			self.progressBar.Update(self.progressCount, self.progressMsg)
			bagInfo = {'Contact-Name': donorText}
			if self.hashOption.GetSelection() == 0:
				bag = bagit.make_bag(bagDir, bagInfo)
			elif self.hashOption.GetSelection() == 1:
				bag = bagit.make_bag(bagDir, bagInfo, 1, ['sha256'])
			else:
				raise ValueError("Unable to read checksum selection.")
			self.progressCount = self.progressCount + 1
			self.progressBar.Update(self.progressCount, self.progressMsg)
		except:
			exceptMsg = traceback.format_exc()
			if os.path.isdir(bagDir):
				shutil.rmtree(bagDir)
			self.errorMessage("Failed to bag files.", exceptMsg)
		
		
		#write to receipt
		try:
			self.progressMsg = self.progressMsgRoot + "Writing receipt..."
			self.progressBar.Update(self.progressCount, self.progressMsg)
			if os.path.isfile("receipt.xml"):
				parser = ET.XMLParser(remove_blank_text=True)
				recriptParse = ET.parse("receipt.xml", parser)
				receiptRoot = recriptParse.getroot()
			else:
				receiptRoot = ET.Element('receipt')
			accessionXML = ET.Element("accession")
			accessionXML.set('number', dirXML.attrib['number'])
			receiptRoot.append(accessionXML)
			profileXML= copy.deepcopy(dirXML.find("profile"))
			accessionXML.append(profileXML)
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
			self.progressBar.Update(self.progressCount, self.progressMsg)
		except:
			exceptMsg = traceback.format_exc()
			if os.path.isdir(bagDir):
				shutil.rmtree(bagDir)
			self.errorMessage("Failed to write receipt", exceptMsg)
		
		
		#remove unwanted files from XML
		try:
			self.progressMsg = self.progressMsgRoot + "Removing records of unwanted files..."
			self.progressBar.Update(self.progressCount, self.progressMsg)
			deleteList = []
			for record in dirXML.iter():
				if 'name' in record.attrib:
					#create list of elements to remove
					if record.attrib["check"] == "False":
						deleteList.append([record, record.getparent()])
					#else remove check attribute
					elif record.attrib["check"] == "True":
						record.attrib.pop('check')
					else:
						raise  ValueError("XML DIRECTORY ERROR, @check for " + record.attrib["name"] + " is not True or False.")
			#remove unchecked elements from XML
			for element in deleteList:
				element[1].remove(element[0])
			self.progressCount = self.progressCount + 1
			self.progressBar.Update(self.progressCount, self.progressMsg)
		except:
			exceptMsg = traceback.format_exc()
			if os.path.isdir(bagDir):
				shutil.rmtree(bagDir)
			self.errorMessage("Failed to remove unwanted files from XML", exceptMsg)
			
		
		#write XML to file and update bag manifests
		try:
			self.progressMsg = self.progressMsgRoot + "Writing metadata and finalizing manifests..."
			self.progressBar.Update(self.progressCount, self.progressMsg)
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
			self.progressBar.Update(self.progressCount, self.progressMsg)
		except:
			exceptMsg = traceback.format_exc()
			if os.path.isdir(bagDir):
				shutil.rmtree(bagDir)
			self.errorMessage("Failed to write XML to file and update bag manifests.", exceptMsg)
		
		#compress bag?
		try:
			if self.compressCheck.IsChecked() is True:
				self.progressMsg = self.progressMsgRoot + "Compressing data..."
				self.progressBar.Update(self.progressCount, self.progressMsg)
				if self.get_size(bagDir) >= 2000000000:
					raise ValueError("The directory you are trying to transfer is larger than 2GB and cannot be compressed.")
				else:
					if self.compressOption.GetSelection() == 0:
						finalPackage = shutil.make_archive(bagDir, 'zip', bagDir)
					elif self.compressOption.GetSelection() == 1:
						finalPackage = shutil.make_archive(bagDir, 'gztar', bagDir)
					else:
						raise ValueError("Unable to read compression selection.")
					shutil.rmtree(bagDir)
					self.progressCount = self.progressCount + 1
					self.progressBar.Update(self.progressCount, self.progressMsg)
			else:
				finalPackage = bagDir
			return finalPackage, locationText, accessionNumber, receiptRoot, progressGoal
		except:
			exceptMsg = traceback.format_exc()
			if os.path.isdir(bagDir):
				shutil.rmtree(bagDir)
			if os.path.isfile(os.path.join(self.sourceDir, accessionNumber,".zip")):
				os.remove(os.path.join(self.sourceDir, accessionNumber,".zip"))
			if os.path.isfile(os.path.join(self.sourceDir, accessionNumber,".tar.gz")):
				os.remove(os.path.join(self.sourceDir, accessionNumber,".tar.gz"))
			self.errorMessage("Failed to compress bag.", exceptMsg)
		
	#############################################################################################################################
	
	def moveNetwork(finalPackage, locationText, accessionNumber):
		#moves directory for each selection in XML while updating progress dialog for every file and folder
		def countCopy(source, destination):
			for item in os.listdir(source):
				path = os.path.join(source, item)
				if os.path.isdir(path):
					self.progressMsg = self.progressMsgRoot + "Transferring " + item
					self.progressBar.Update(self.progressCount, self.progressMsg)
					os.makedirs(os.path.join(destination, item))
					shutil.copystat(path, os.path.join(destination, item))
					self.progressCount = self.progressCount + 1
					self.progressBar.Update(self.progressCount, self.progressMsg)
					countCopy(path, os.path.join(destination, item))
				elif os.path.isfile(path):
					self.progressMsg = self.progressMsgRoot + "Transferring " + item
					self.progressBar.Update(self.progressCount, self.progressMsg)
					shutil.copy2(path, destination)
					self.progressCount = self.progressCount + 1
					self.progressBar.Update(self.progressCount, self.progressMsg)
				else:
					print "error: " + path
							
		#copy SIP to destination
		try:
			self.progressMsg = self.progressMsgRoot + "Transferring to the Archives..."
			self.progressBar.Update(self.progressCount, self.progressMsg)
			if os.path.isdir(finalPackage):
				os.makedirs(os.path.join(locationText, accessionNumber))
				destination = os.path.join(locationText, accessionNumber)
				countCopy(finalPackage, destination)
				if os.path.isdir(finalPackage):
					shutil.rmtree(finalPackage)
			elif os.path.isfile(finalPackage):
				shutil.copy2(finalPackage, locationText)
				os.remove(finalPackage)
			else:
				raise ValueError("Could not detect if package was file or directory.")
			self.progressCount = self.progressCount + 1
			self.progressBar.Update(self.progressCount, self.progressMsg)
		except:
			exceptMsg = traceback.format_exc()
			if os.path.isdir(finalPackage):
				shutil.rmtree(finalPackage)
			elif os.path.isfile(finalPackage):
				os.remove(finalPackage)
			self.errorMessage("Failed to copy bag to destination.", exceptMsg)
		
		
	##############################################################################################################################################

	#open ~directory.xml
	dirFile = "~directory.xml"
	parser = ET.XMLParser(remove_blank_text=True)
	dirParse = ET.parse(dirFile, parser)
	dirXML = dirParse.getroot()
	
	if self.m_radioBox1.GetSelection() == 1:
		methodText = "ftp"
		dirXML.find("profile/method").text = methodText
		
		#temporaty not FTP dialog
		ftpDemo = wx.MessageDialog(None, 'Demo version. FTP module has not yet been written. \nPlease use Network Path or Local Path to test.', 'FTP Not Available', wx.OK | wx.ICON_EXCLAMATION)
		ftpDemo.ShowModal()
		#pathTransfer = False
		#finalPackage = packageSIP(pathTransfer, dirXML)
		#moveFTP(finalPackage)
		
	else:
		methodText = "network"
		dirXML.find("profile/method").text = methodText
		pathTransfer = True
		finalPackage, locationText, accessionNumber, receiptRoot, progressGoal = packageSIP(pathTransfer, dirXML)
		moveNetwork(finalPackage, locationText, accessionNumber)
	
	#write receipt to file
	try:
		receiptString = ET.tostring(receiptRoot, pretty_print=True)	
		file = open("receipt.xml", "w")
		file.write(receiptString)
		file.close()
		os.remove("~directory.xml")
		self.progressCount = self.progressCount + 1
		if self.progressCount == progressGoal:
			self.progressBar.Destroy()
		else:
			self.progressBar.Update(self.progressCount, self.progressMsg)
	except:
		exceptMsg = traceback.format_exc()
		raise ValueError("Failed to write to receipt to file")
	
	
		
	if self.progressCount >= progressGoal:
		print "progressGoal reached " + str(self.progressCount)
		self.Close()
	else:
		print "didn't reach processGoal, reached " +str(self.progressCount)
		self.Close()
		
	successNotice = wx.MessageDialog(None, 'The transfer has completed. You can examine the files you transfered in the Receipt.', 'Transfer was Successful', wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP)
	successNotice.ShowModal()
