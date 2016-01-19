import wx
from lxml import etree as ET
from ftplib import FTP
from ftplib import FTP_TLS
import os
import traceback
import shutil
import time
import calendar
import datetime
import subprocess
import admin
import bagit
import zipfile
import copy
import shortuuid


def transferModule(self):
	
	######################################################################################################################
	
	def packageSIP(pathTransfer, dirXML):
		
		#update accession count
		configXML = os.path.join(self.appData, "config.xml")
		parser = ET.XMLParser(remove_blank_text=True)
		configParse = ET.parse(configXML, parser)
		config = configParse.getroot()
		#adds 1 to accessionCount in config.xml
		accessionCount = str(int(config.find("accessionCount").text) + 1)
		config.find("accessionCount").text = accessionCount
		configString = ET.tostring(config, pretty_print=True)
		file = open(os.path.join(self.appData, "config.xml"), "w")
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
		#update accession number from GUI additions
		updateAccession = creatorIdText + "-" + donorText.replace(" ", "_") + "-" + accessionCount
		dirXML.set("number", updateAccession)
		
		#check transfer location, ask to create
		if pathTransfer == True:
			if len(locationText) < 1:
				netwError = wx.MessageDialog(None, 'You must enter a local or network path as your transfer destination.', 'Transfer Location Error', wx.OK | wx.ICON_EXCLAMATION)
				netwError.ShowModal()
			elif not os.path.isdir(locationText):
				netwError = wx.MessageDialog(None, "The network or location path \"" + locationText + "\" does not exist. Would you like to try to create this directory?", "Transfer Location Not Found", wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING | wx.STAY_ON_TOP)
				if netwError.ShowModal() == wx.ID_YES:
					try:
						os.makedirs(locationText)
						pathTransfer = True
					except:
						raise ValueError("Unable to create directory.")
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
		if config.find("compress").attrib["lock"].lower() == "true":
			compressCheckXML = True
		else:
			if self.compressCheck.IsChecked():
				compressCheckXML = True
			else:
				compressCheckXML = False
		if compressCheckXML is False:
			progressGoal = recordsCount + recordsCount + 11
		else:
			progressGoal = recordsCount + 7
		if self.adminTest == True:
			progressGoal = progressGoal + totalCount
		else:
			if self.timestampOption.GetSelection() == 1:
				progressGoal = progressGoal + 12
			else:
				progressGoal = progressGoal + 1
		print "Anticipated stages: " + str(progressGoal)
		self.progressCount = 0
		self.progressMsgRoot = "Packaging your records and transferring them to the archives.\n"
		self.progressMsg = self.progressMsgRoot
		self.progressBar = wx.ProgressDialog("Transferring Your Records...", self.progressMsg, maximum=progressGoal, parent=self, style=wx.PD_AUTO_HIDE | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
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
			raise ValueError("Failed to run forensics tools.")
		
		#move files to new directory
		try:
			self.progressMsg = self.progressMsgRoot + "Gathering files..."
			self.progressBar.Update(self.progressCount, self.progressMsg)
			accessionNumber = dirXML.attrib['number']
			if accessionNumber.startswith("-"):
				accessionNumber = "accession" + accessionNumber
			if os.path.isdir(os.path.join(self.appData, "staging", accessionNumber)):
				countError = wx.MessageDialog(None, "Previous Accession found in staging area " + os.path.join(self.appData, "staging", accessionNumber) +"\n Do you want to overwrite this data?", "Packaging Error", wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING | wx.STAY_ON_TOP)
				if countError.ShowModal() == wx.ID_YES:
					try:
						shutil.rmtree(os.path.join(self.appData, "staging", accessionNumber))
					except:
						raise ValueError("Unable overwrite previous partial transfer. Try changing the Accession Count in config.xml.")
				else:
					raise ValueError("Unable to transfer files. Try changing the Accession Count in config.xml.")
			os.makedirs(os.path.join(self.appData, "staging", accessionNumber))
			bagDir = os.path.join(self.appData, "staging", accessionNumber)
			countCopyXML(self.sourceDir, bagDir, dirXML)
		except:
			if os.path.isdir(bagDir):
				shutil.rmtree(bagDir)
			raise ValueError("Failed to move files to new directory.")
		
		#bag directory
		try:
			self.progressMsg = self.progressMsgRoot + "Bagging files..."
			self.progressBar.Update(self.progressCount, self.progressMsg)
			bagInfo = {"accession": accessionNumber}
			for profileInfo in dirXML.find("profile"):
				if profileInfo.text:
					bagInfo.update({profileInfo.tag:profileInfo.text})
			if self.hashOption.GetSelection() == 0:
				bag = bagit.make_bag(bagDir, bagInfo)
			elif self.hashOption.GetSelection() == 1:
				bag = bagit.make_bag(bagDir, bagInfo, 1, ['sha256'])
			else:
				raise ValueError("Unable to read checksum selection.")
			
			#update curatorialEvents
			for item in dirXML.iter():
				if "name" in item.attrib:
					if item.attrib["check"] == "True":
						eventBagit = ET.Element("event")
						eventTime = str(calendar.timegm(time.gmtime()))
						eventBagit.set("timestamp", self.timestampOutput(eventTime))
						eventBagit.text = "ran Bagit-python to package accession"
						item.find("curatorialEvents").append(eventBagit)
						if compressCheckXML is True:
							if self.compressOption.GetSelection() == 0:
								eventCompress = ET.Element("event")
								eventTime = str(calendar.timegm(time.gmtime()))
								eventCompress.set("timestamp", self.timestampOutput(eventTime))
								eventCompress.text = "compressed to .zip using shutil.make_archive"
								item.find("curatorialEvents").append(eventCompress)
							else:
								eventCompress = ET.Element("event")
								eventTime = str(calendar.timegm(time.gmtime()))
								eventCompress.set("timestamp", self.timestampOutput(eventTime))
								eventCompress.text = "compressed to .gz using shutil.make_archive"
								item.find("curatorialEvents").append(eventCompress)
						eventTransfer = ET.Element("event")
						eventTime = str(calendar.timegm(time.gmtime()))
						eventTransfer.set("timestamp", self.timestampOutput(eventTime))
						eventTransfer.text = methodText + " transfer"
						item.find("curatorialEvents").append(eventTransfer)
			
			self.progressCount = self.progressCount + 1
			self.progressBar.Update(self.progressCount, self.progressMsg)
		except:
			if os.path.isdir(bagDir):
				shutil.rmtree(bagDir)
			raise ValueError("Failed to bag files.")
		
		
		#write to receipt
		try:
			self.progressMsg = self.progressMsgRoot + "Writing receipt..."
			self.progressBar.Update(self.progressCount, self.progressMsg)
			if os.path.isfile(os.path.join(self.appData, "receipt.xml")):
				parser = ET.XMLParser(remove_blank_text=True)
				recriptParse = ET.parse(os.path.join(self.appData, "receipt.xml"), parser)
				receiptRoot = recriptParse.getroot()
			else:
				receiptRoot = ET.Element('receipt')
			accessionXML = ET.Element("accession")
			accessionXML.set('number', dirXML.attrib['number'])
			if self.timeZoneOption.GetSelection() == 1:
				#submitted time is posix
				accessionXML.set('time', 'posix')
			elif self.timeZoneOption.GetSelection() == 2:
				#submitted time is utc
				accessionXML.set('time', 'utc')
			else:
				#submitted time is local
				accessionXML.set('time', 'local')
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
			if os.path.isdir(bagDir):
				shutil.rmtree(bagDir)
			raise ValueError("Failed to write receipt.")
		
		
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
			if os.path.isdir(bagDir):
				shutil.rmtree(bagDir)
				raise ValueError("Failed to remove unwanted files from XML.")
			
		
		#write XML to file and update bag manifests
		try:
			self.progressMsg = self.progressMsgRoot + "Writing metadata and finalizing manifests..."
			self.progressBar.Update(self.progressCount, self.progressMsg)
			#write submission time to XML
			eventTime = str(calendar.timegm(time.gmtime()))
			dirXML.set('submitted', self.timestampOutput(eventTime))
			#write submission time to receipt
			accessionXML.set('submitted', dirXML.attrib['submitted'])
			bag.info['submitted'] = dirXML.attrib['submitted']
			descString = ET.tostring(dirXML, pretty_print=True)					
			file = open(bagDir + "\\" + accessionNumber + ".xml", "w")
			file.write(descString)
			file.close()
			bag.save(manifests=True)
			self.progressCount = self.progressCount + 1
			self.progressBar.Update(self.progressCount, self.progressMsg)
		except:
			if os.path.isdir(bagDir):
				shutil.rmtree(bagDir)
				raise ValueError("Failed to write XML to file and update bag manifests.")
		
		#compress bag?
		try:
			if compressCheckXML is True:
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
			if os.path.isdir(bagDir):
				shutil.rmtree(bagDir)
			if os.path.isfile(os.path.join(self.sourceDir, accessionNumber,".zip")):
				os.remove(os.path.join(self.sourceDir, accessionNumber,".zip"))
			if os.path.isfile(os.path.join(self.sourceDir, accessionNumber,".tar.gz")):
				os.remove(os.path.join(self.sourceDir, accessionNumber,".tar.gz"))
			raise ValueError("Failed to compress bag.")
		
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
			#check if finalPackage already exists in transfer location, add OVER to prevent error or overwrite
			if os.path.exists(os.path.join(locationText, os.path.basename(finalPackage))):
				transferDir = os.path.dirname(finalPackage)
				packageName = os.path.basename(finalPackage)
				overPackage = os.path.join(transferDir, shortuuid.uuid() + packageName)
				os.rename(os.path.join(transferDir, packageName), overPackage)
				finalPackage = os.path.join(transferDir, overPackage)
			if os.path.isdir(finalPackage):
				os.makedirs(os.path.join(locationText, os.path.basename(finalPackage)))
				destination = os.path.join(locationText, os.path.basename(finalPackage))
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
			raise ValueError("Failed to transfer bag to destination over Network.")
		
		
	##############################################################################################################################################
	
	#def moveOneDrive(finalPackage, locationText):
	
	##############################################################################################################################################
	
	def moveFTP(self, finalPackage, locationText):
	
		def countFTP(ftp, source):
			for item in os.listdir(source):
				path = os.path.join(source, item)
				if os.path.isdir(path):
					pass				
				elif os.path.isfile(path):
					self.progressMsg = self.progressMsgRoot + "Transferring " + item
					self.progressBar.Update(self.progressCount, self.progressMsg)
					
					ftp.storbinary("STOR " + item, open(path, "rb"), 1024)
					
					self.progressCount = self.progressCount + 1
					self.progressBar.Update(self.progressCount, self.progressMsg)
				else:
					print "error: " + path
			for item in os.listdir(source):
				path = os.path.join(source, item)
				if os.path.isdir(path):
					self.progressMsg = self.progressMsgRoot + "Transferring " + item
					self.progressBar.Update(self.progressCount, self.progressMsg)
					self.progressCount = self.progressCount + 1
					self.progressBar.Update(self.progressCount, self.progressMsg)
					
					ftp.mkd(item)
					ftp.cwd(item)
					countFTP(ftp, path)
					
				elif os.path.isfile(path):
					pass
				else:
					print "error: " + path
	
		try:
			self.progressMsg = self.progressMsgRoot + "Transferring to the Archives..."
			self.progressBar.Update(self.progressCount, self.progressMsg)
		
			#remove ftp:// if present
			if locationText.lower().startswith("ftp://"):
					locationText = locationText[6:]
			
			#get credentials
			try:
				login = self.loginInput.GetValue()
			except:
				login = ""
			try:
				pw = self.passwordInput.GetValue()
			except:
				pw = ""
			if len(login) < 1 or len(pw) < 1:
				login, pw = self.loginBox(login, pw)
			
			#FTP login
			ftpURL = locationText.split("/")
			if self.m_radioBox1.GetSelection() == 2:
				#FPT with TLS
				ftp = FTP_TLS(ftpURL[0])
				try:
					ftp.login(login, pw)
				except:
					raise ValueError("Incorrect Login or Password, or incorrect encryption settings in FTP server.")
				try:
					ftp.prot_p() 
				except:
					raise ValueError("Error setting up encryption.")
			else:
				#unencrypted FTP
				ftp = FTP(ftpURL[0])
				try:
					ftp.login(login, pw)
				except:
					raise ValueError("Incorrect Login or Password.")

			
			#FTP navigate to subdirectories
			ftpURL.pop(0)
			for subdir in ftpURL:
				ftp.cwd(subdir)
			
			if os.path.isdir(finalPackage):
				#Upload directory
				try:
					ftp.mkd(os.path.basename(finalPackage))
					ftp.cwd(os.path.basename(finalPackage))
				except:
					ftp.mkd(shortuuid.uuid() + os.path.basename(finalPackage))
					ftp.cwd(shortuuid.uuid() + os.path.basename(finalPackage))
				countFTP(ftp, finalPackage)
				if os.path.isdir(finalPackage):
					shutil.rmtree(finalPackage)
			elif os.path.isfile(finalPackage):
				#Upload compressed file
				fileList = []
				for ftpFile in ftp.nlst():
					fileList.append(os.path.basename(ftpFile))
				if os.path.basename(finalPackage) in fileList:
					ftp.storbinary("STOR " + shortuuid.uuid() + os.path.basename(finalPackage), open(finalPackage, "rb"), 1024)
				else:
					ftp.storbinary("STOR " + os.path.basename(finalPackage), open(finalPackage, "rb"), 1024)
				ftp.quit()
				if os.path.isfile(finalPackage):
					os.remove(finalPackage)
			else:
				raise ValueError("Could not detect if package was file or directory.")				
					
			self.progressCount = self.progressCount + 1
			self.progressBar.Update(self.progressCount, self.progressMsg)		
		except:
			ftp.quit()
			raise ValueError("Failed to transfer bag to destination over FTP.")
		
	
	##############################################################################################################################################

	#open ~directory.xml
	dirFile = os.path.join(self.appData, "~directory.xml")
	parser = ET.XMLParser(remove_blank_text=True)
	dirParse = ET.parse(dirFile, parser)
	dirXML = dirParse.getroot()
	
	#package files in staging area in AppData and make transfer
	try:
		if self.m_radioBox1.GetSelection() == 0:
			#transfer local or network storage
			methodText = "network"
			dirXML.find("profile/method").text = methodText
			pathTransfer = True
			finalPackage, locationText, accessionNumber, receiptRoot, progressGoal = packageSIP(pathTransfer, dirXML)
			moveNetwork(finalPackage, locationText, accessionNumber)
			
		elif self.m_radioBox1.GetSelection() == 3:
			#transfer OneDrive
			pass
			#methodText = "onedrive"
			#dirXML.find("profile/method").text = methodText
			#pathTransfer = True
			#finalPackage, locationText, accessionNumber, receiptRoot, progressGoal = packageSIP(pathTransfer, dirXML)
			#moveOneDrive(finalPackage, locationText, accessionNumber)
			
		else:
			#Tranfer FTP
			methodText = "ftp"
			dirXML.find("profile/method").text = methodText
			
			pathTransfer = False
			finalPackage, locationText, accessionNumber, receiptRoot, progressGoal = packageSIP(pathTransfer, dirXML)
			moveFTP(self, finalPackage, locationText)
			
		#write receipt to file
		try:
			receiptString = ET.tostring(receiptRoot, pretty_print=True)	
			file = open(os.path.join(self.appData, "receipt.xml"), "w")
			file.write(receiptString)
			file.close()
			os.remove(os.path.join(self.appData, "~directory.xml"))
			self.progressCount = self.progressCount + 1
			if self.progressCount == progressGoal:
				self.progressBar.Destroy()
			else:
				self.progressBar.Update(self.progressCount, self.progressMsg)
		except:
			raise ValueError("Failed to write to receipt to file")
			
		if self.progressCount >= progressGoal:
			print "progressGoal reached " + str(self.progressCount)
			self.Close()
		else:
			print "didn't reach processGoal, reached " +str(self.progressCount)
			self.Close()
			
		successNotice = wx.MessageDialog(None, 'The transfer has completed. You can examine the files you transferred in the Receipt.', 'Transfer was Successful', wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP)
		successNotice.ShowModal()
	
	except (Exception, ValueError) as e:
		#error Dialog that doesn't close ANTS
		exceptMsg = traceback.format_exc()
		print exceptMsg
		errorOutput = "\n" + "#############################################################\n" + str(datetime.datetime.utcnow()) + "\n#############################################################\n" + str(exceptMsg) + "\n********************************************************************************"
		file = open(os.path.join(self.appData, "errorLog.txt"), "a")
		file.write(errorOutput)
		file.close()
		self.progressBar.Destroy()
		try:
			configXML = os.path.join(self.appData, "config.xml")
			parser = ET.XMLParser(remove_blank_text=True)
			configParse = ET.parse(configXML, parser)
			config = configParse.getroot()
			if config.find("error").text == "minimal":
				exceptMsg = e
		except:
			pass
		errorPopup = wx.MessageDialog(None, str(exceptMsg), "Transfer Error", wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP)
		errorPopup.ShowModal()
		#ask to save archival package locally
		askSaveLocal = wx.MessageDialog(None, "There was an error transfering files to the archives. ANTS does not modify your original files, so they reminan unchanged in their original location and you can retry the transfer at any time. Would you like to save the archival package that ANTS failed to transfer?", "Save Archival Package?", wx.YES_NO | wx.YES_DEFAULT | wx.ICON_ERROR | wx.STAY_ON_TOP)
		if askSaveLocal.ShowModal() == wx.ID_YES:
			saveLocal = wx.DirDialog(None, "Select a location to save the archival package:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
			if saveLocal.ShowModal() == wx.ID_OK:
				localLocation =  saveLocal.GetPath()
				try:
					if os.path.isdir(finalPackage):
						shutil.copytree(finalPackage, os.path.join(localLocation, os.path.basename(finalPackage)))
						shutil.rmtree(finalPackage)
					elif os.path.isfile(finalPackage):
						shutil.copy2(finalPackage, localLocation)
						os.remove(finalPackage)
				except:
					raise ValueError("Failed to save archival package locally.")
		if os.path.isdir(finalPackage):
			shutil.rmtree(finalPackage)
		elif os.path.isfile(finalPackage):
			os.remove(finalPackage)
		noChange = wx.MessageDialog(None, "Failed to transfer. Your files also remain in their original location and you may retry the transfer at any time.", "Files Remain Unchanged.", wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP)
		noChange.ShowModal()
