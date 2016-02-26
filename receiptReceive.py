import wx
import os
import subprocess
from lxml import etree as ET
from ftplib import FTP
from ftplib import FTP_TLS
import traceback
import datetime
import shutil
import win32crypt
import binascii
import threading
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from resource_path import resource_path

import antsGUI as gui

def produceReceipt(self, xmlSource):
	
	if not os.path.isfile(os.path.join(self.appData, "receipt.xml")):
		noReceipt = wx.MessageDialog(None, 'Unable to find a receipt. You must transfer files in order to obtain a receipt.', 'No Receipt found', wx.OK | wx.ICON_WARNING)
		noReceipt.ShowModal()
	else:
	
		if xmlSource == True:
			try:
				configXML = os.path.join(self.appData, "config.xml")
				parser = ET.XMLParser(remove_blank_text=True)
				configParse = ET.parse(configXML, parser)
				config = configParse.getroot()
				if config.find("receipt").text is None:
					receipt = "html"
				else:
					receipt = config.find("receipt").text
			except:
				receipt = "html"
		else:
			if self.receiptOption.GetSelection() == 1:
				receipt = "csv"
			elif self.receiptOption.GetSelection() == 2:
				receipt = "xml"
			else:
				receipt = "html"
	
		import tempfile
		tempDir = tempfile.mkdtemp()
		if receipt == "csv":
			import csv
			headLine = ["accession", "submitted", "time", "type", "name", "path", "id"]
			tempCSV = open(os.path.join(tempDir, 'receipt.csv'), 'wb')
			csv = csv.writer(tempCSV)
			csv.writerow(headLine)
			parser = ET.XMLParser(remove_blank_text=True)
			receiptParse = ET.parse(os.path.join(self.appData, "receipt.xml"), parser)
			receiptXML = receiptParse.getroot()
			for accession in receiptXML:
				number = accession.attrib['number']
				submitted = accession.attrib['submitted']
				if "time" in accession.attrib:
					timeType = accession.attrib["time"]
				else:
					timeType = "unknown"
				for item in accession:
					if item.tag == "item":
						itemList = [number, submitted, timeType, item.find('type').text, item.find('name').text, item.find('path').text, item.find('id').text]
						csv.writerow(itemList)
			tempCSV.close()
			subprocess.Popen(os.path.join(tempDir, "receipt.csv"), shell=True)
		elif receipt == "xml":
			shutil.copy2(os.path.join(self.appData, "receipt.xml"), tempDir)
			subprocess.Popen(os.path.join(tempDir, os.path.join(self.appData, "receipt.xml")), shell=True)
		else:
			from html import htmlReceipt
			htmlString = htmlReceipt(self, os.path.join(self.appData, "receipt.xml"), str(datetime.datetime.now()), os.path.join(self.appData, "config.xml"))
			htmlFile = open(os.path.join(tempDir, "receipt.html"), "w")
			htmlFile.write(htmlString)
			htmlFile.close()
			subprocess.Popen(os.path.join(tempDir, "receipt.html"), shell=True)
				
				
###########################################################################################################################


def checkReceiveFiles(self, xmlSource):
	
	try:	
		#get the information needed from config.xml for the splash screen or the GUI from the options tab
		if xmlSource == True:
			#means call was made from welcome screen before GUI, get transfer info directly from config.xml
			try:
				configXML = os.path.join(self.appData, "config.xml")
				parser = ET.XMLParser(remove_blank_text=True)
				configParse = ET.parse(configXML, parser)
				config = configParse.getroot()
			except:
				raise ValueError("Configuration data not found. ANTS needs a transfer method and a receive location to receive files. Please select \"Browse\" to start the application and enter this information in the \"Options\" tab.")
			if config.find("transferMethod").text is None or config.find("receiveLocation").text is None:
				raise ValueError("Configuration data not found. ANTS needs a transfer method and a receive location to receive files. Please select \"Browse\" to start the application and enter this information in the \"Options\" tab.")
			transferMethod = config.find("transferMethod").text
			receiveLocation = config.find("receiveLocation").text
			if transferMethod != "network":
				#get credentials, try XML first, then run loginBox function from ants.py
				try:
					login = config.find("login").text
					if login is None:
						login = ""
				except:
					login = ""
				try:
					getPw = binascii.unhexlify(config.find("pw").text)
					pw = win32crypt.CryptUnprotectData(getPw)[1].replace("\x00", "").encode('ascii', 'replace')
					if pw is None:
						pw = ""
				except:
					pw = ""
				
			
		else:
			#means call was made from GUI, get transfer info from GUI
			#get credentials, try GUI first, then run loginBox function from antsFromBoot.py
			try:
				login = self.loginInput.GetValue()
			except:
				login = ""
			try:
				pw = self.passwordInput.GetValue()
			except:
				pw = ""
		
			receiveLocation = self.receiveInput.GetValue()
			if len(receiveLocation) < 1:
				raise ValueError("Failed to receive files, you must enter a local or network path as your transfer destination")
			
			if self.m_radioBox1.GetSelection() == 0:
				transferMethod = "network"
			elif self.m_radioBox1.GetSelection() == 2:
				transferMethod = "ftptls"
			elif self.m_radioBox1.GetSelection() == 3:
				transferMethod = "googledrive"
			else:
				transferMethod = "ftp"
			
		#login for non-network transfers
		if transferMethod != "network" and transferMethod != "googledrive":
			if len(login) < 1 or len(pw) < 1:
				login, pw = self.loginBox(login, pw)
					
				
				
		#Actual Transfers code
		if transferMethod == "network":
			if not os.path.isdir(receiveLocation): 
				#directory not found, try to make it?
				createDir = wx.MessageDialog(None, "The network or location path \"" + receiveLocation + "\" does not exist. Would you like to try to create this directory?", "Receive Location Not Found", wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)
				if createDir.ShowModal() == wx.ID_YES:
					try:
						os.makedirs(receiveLocation)
					except:
						raise ValueError("Unable to create receive directory. You may not have permission to create this folder. Please make sure the Receive Location on the options tab is correct or contact the Archivist.")
			fileList = []
			def fileToList(dir):
				for item in os.listdir(dir):
					if os.path.isfile(os.path.join(dir, item)):
						fileList.append(os.path.join(dir, item).split(receiveLocation + "\\")[1])
					elif os.path.isdir(os.path.join(dir, item)):
						fileToList(os.path.join(dir, item))
					else:
						raise ValueError("Error reading Receive Location")
			fileToList(receiveLocation)
			selectFiles = wx.MultiChoiceDialog( self, "Select Files to Download", "Download Records from the University Archives", fileList)
			overwriteSwitch = False
			overwriteAsk = False
			if selectFiles.ShowModal() == wx.ID_OK:
				selections = selectFiles.GetSelections()
				if len(selections) > 0:
					strings = [fileList[x] for x in selections]
					saveRequest = wx.DirDialog(None, "Select a folder to save your requested files:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
					if saveRequest.ShowModal() == wx.ID_OK:
						saveLocation =  saveRequest.GetPath()
						saveGoal = len(strings)
						saveCount= 0
						saveProgress = wx.ProgressDialog("Downloading Requested Files", "Downloading files...",  maximum=saveGoal, parent=self, style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)
						for requestedFile in strings:
							saveMsg = "Downloading " + requestedFile + "..."
							saveProgress.Update(saveCount, saveMsg)
							if len(os.path.split(requestedFile)) > 1:
								if not os.path.exists(os.path.join(saveLocation, os.path.dirname(requestedFile))):
									os.makedirs(os.path.join(saveLocation, os.path.dirname(requestedFile)))
							if os.path.isfile(os.path.join(saveLocation, requestedFile)):
								if overwriteAsk == False:
									askOverwrite = wx.MessageDialog(None, "Some of the files you requested were already found. Would you like to overwrite them?", "Overwrite Existing Files?", wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)
									overwriteAsk = True
									if askOverwrite.ShowModal() == wx.ID_YES:
										overwriteSwitch = True
								if overwriteSwitch == True:
									shutil.copy2(os.path.join(receiveLocation, requestedFile), os.path.join(saveLocation, requestedFile))
							shutil.copy2(os.path.join(receiveLocation, requestedFile), os.path.join(saveLocation, requestedFile))
							saveCount = saveCount + 1
							if saveCount >= saveGoal:
								saveProgress.Destroy()
								successNotice = wx.MessageDialog(None, 'The files you requested were downloaded successfully.', 'Request was Successful', wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP)
								successNotice.ShowModal()
							else:
								saveProgress.Update(saveCount, saveMsg)
					saveRequest.Destroy()
			selectFiles.Destroy()
		elif transferMethod =="googledrive":
			
			try:
				try:
					shutil.copy2(resource_path("data.json"), os.path.join(os.getcwd(), "client_secrets.json"))
				except:
					raise ValueError("Client error, might be a permissions issue. Please consult your archivist.")
				
				try:
					#Google Drive login
					def googleLogin(googlePath, gauth, t_stop):
						# Try to load saved client credentials
						gauth.LoadCredentialsFile(os.path.join(self.appData, "gcreds.txt"))
						if gauth.credentials is None:
							# Authenticate if they're not there
							gauth.LocalWebserverAuth()
						elif gauth.access_token_expired:
							# Refresh them if expired
							gauth.Refresh()
						else:
							# Initialize the saved creds
							gauth.Authorize()
						# Save the current credentials to a file
						gauth.SaveCredentialsFile(os.path.join(self.appData, "gcreds.txt"))
						self.drive = GoogleDrive(gauth)			
						self.childFrame.Close()
					
					gauth = GoogleAuth()
					self.t_stop= threading.Event()
					t = threading.Thread(name="GoogleLogin", target=googleLogin, args=(receiveLocation, gauth, self.t_stop))
					t.start()
					try:
						self.childFrame = gui.loginFrame(self)
					except:
						print traceback.format_exc()
					self.childFrame.ShowModal()
				except:
					raise ValueError("GoogleDrive Login Error")
					
				def driveDownload(driveInstance, fileList):
					#ask which files to download
					selectFiles = wx.MultiChoiceDialog( self, "Select Files to Download", "Download Records from the University Archives", fileList)
					overwriteSwitch = False
					overwriteAsk = False
					if selectFiles.ShowModal() == wx.ID_OK:
						selections = selectFiles.GetSelections()
						if len(selections) > 0:
							strings = [fileList[x] for x in selections]
							saveRequest = wx.DirDialog(None, "Select a folder to save your requested files:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
							if saveRequest.ShowModal() == wx.ID_OK:
								saveLocation =  saveRequest.GetPath()
								saveGoal = len(strings)
								saveCount= 0
								saveProgress = wx.ProgressDialog("Downloading Requested Files", "Downloading files...",  maximum=saveGoal, parent=self, style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)
								for requestedFile in strings:
									saveMsg = "Downloading " + requestedFile + "..."
									saveProgress.Update(saveCount, saveMsg)
									if os.path.isfile(os.path.join(saveLocation, requestedFile)):
										if overwriteAsk == False:
											askOverwrite = wx.MessageDialog(None, "Some of the files you requested were already found. Would you like to overwrite them?", "Overwrite Existing Files?", wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)
											overwriteAsk = True
											if askOverwrite.ShowModal() == wx.ID_YES:
												overwriteSwitch = True
										if overwriteSwitch == True:
											for file in check_list:
												if file["title"] == requestedFile:
													fileDownload = driveInstance.CreateFile({'id': file['id']})
													fileDownload.GetContentFile(os.path.join(saveLocation, requestedFile))
									for file in check_list:
										if file["title"] == requestedFile:
											fileDownload = driveInstance.CreateFile({'id': file['id']})
											fileDownload.GetContentFile(os.path.join(saveLocation, requestedFile))
											
									saveCount = saveCount + 1
									if saveCount >= saveGoal:
										saveProgress.Destroy()
										successNotice = wx.MessageDialog(None, 'The files you requested were downloaded successfully.', 'Request was Successful', wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP)
										successNotice.ShowModal()
									else:
										saveProgress.Update(saveCount, saveMsg)
							saveRequest.Destroy()
					selectFiles.Destroy()
					
				try:
					pathList = receiveLocation.split("/")
					if pathList < 2:
						#no subfolders
						
						#get availible files
						fileList = []
						check_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
						for file in check_list:
							fileList.append(file["title"])
						
						#select and download files from list
						driveDownload(self.drive, fileList)
					
					
					else:
						def findSubFolder(pathList, folderId, folderTitle):
							sub_list = self.drive.ListFile({'q': "'" + folderId + "' in parents and trashed=false"}).GetList()
							match = False
							for folder in sub_list:
								if folder["title"] == pathList[0]:
									match = True
									folderId = folder["id"]
									folderTitle = folder["title"]
							if match == True:
								if len(pathList) > 1:
									del pathList[0]
									findSubFolder(pathList, folderId, folderTitle)
								else:
									print "Found GoogleDrive destination path"
									self.childFrame.Destroy()
									return folderId
							else:
								print "Google path failed"
								self.childFrame.Destroy()
								if os.path.isfile(os.path.join(os.getcwd(), "client_secrets.json")):
									os.remove(os.path.join(os.getcwd(), "client_secrets.json"))
								noAuth = wx.MessageDialog(None, 'Google path failed. Login was successful but subfolder ' + folderTitle +  ' was not found.', 'Login Failed', wx.OK | wx.ICON_WARNING)
								noAuth.ShowModal()
								return folderId
								
						first_list = self.drive.ListFile({'q': "sharedWithMe=True"}).GetList()
						match = False
						for folder in first_list:
							if folder["title"] == pathList[0]:
								match = True
								folderId = folder["id"]
								folderTitle = folder["title"]
						if match == True:
							if len(pathList) > 1:
								del pathList[0]
								folderId = findSubFolder(pathList, folderId, folderTitle)
						
						#get availible files
						fileList = []
						check_list = self.drive.ListFile({'q': "'" + folderId + "' in parents and trashed=false"}).GetList()
						for file in check_list:
							fileList.append(file["title"])
						
						#select and download files from list
						driveDownload(self.drive, fileList)
						
						if os.path.isfile(os.path.join(os.getcwd(), "client_secrets.json")):
							os.remove(os.path.join(os.getcwd(), "client_secrets.json"))
					
				except:
					if os.path.isfile(os.path.join(os.getcwd(), "client_secrets.json")):
						os.remove(os.path.join(os.getcwd(), "client_secrets.json"))
					raise ValueError("Access to GoogleDrive failed. Error reading subfolders. Please check settings in the 'Options' tab.")
				
			except:
				raise ValueError("Failed to recieve files from GoogleDrive.")
		
		else:
			
			def isdirFTP(ftp, name):
				try:
					ftp.cwd(name)
					ftp.cwd('..')
					return True
				except:
					return False
					
			def readFTP(ftp, fileList, baseDir):
				listing = []
				listing = ftp.nlst()
				for item in listing:
					if isdirFTP(ftp, item) == True:
						ftp.cwd(item)
						readFTP(ftp, fileList, baseDir)
					else:
						file = item.split(baseDir)[1]
						fileList.append(file[1:])
				return fileList
					
			if receiveLocation.lower().startswith("ftp://"):
				receiveLocation = receiveLocation[6:]
				
			ftpURL = receiveLocation.split("/")
			if transferMethod =="ftptls":
				ftp = FTP_TLS(ftpURL[0])
				try:
					ftp.login(login, pw)
					ftp.prot_p()
				except:
					raise ValueError("Incorrect Login or Password, or incorrect encryption settings in FTP server.")
			else:
				ftp = FTP(ftpURL[0])
				try:
					ftp.login(login, pw)
				except:
					raise ValueError("Incorrect Login or Password.")
			
			ftpURL.pop(0)
			baseDir = ""
			for subdir in ftpURL:
				ftp.cwd(subdir)
				baseDir = baseDir + "/" + subdir
				
			fileList = []
			fileList = readFTP(ftp, fileList, baseDir)
			
			if len(fileList) > 0:
				selectFiles = wx.MultiChoiceDialog( self, "Select Files to Download", "Download Records from the University Archives", fileList)
				overwriteSwitch = False
				overwriteAsk = False
				if selectFiles.ShowModal() == wx.ID_OK:
					selections = selectFiles.GetSelections()
					if len(selections) > 0:
						strings = [fileList[x] for x in selections]
						saveRequest = wx.DirDialog(None, "Select a folder to save your requested files:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
						if saveRequest.ShowModal() == wx.ID_OK:
							saveLocation =  saveRequest.GetPath()
							saveGoal = len(strings)
							saveCount= 0
							saveProgress = wx.ProgressDialog("Downloading Requested Files", "Downloading files...",  maximum=saveGoal, parent=self, style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)
							for requestedFile in strings:
								saveMsg = "Downloading " + requestedFile + "..."
								saveProgress.Update(saveCount, saveMsg)
								localFile = os.path.join(*requestedFile.split("/"))
								if len(os.path.split(localFile)) > 1:
									if not os.path.exists(os.path.join(saveLocation, os.path.dirname(localFile))):
										os.makedirs(os.path.join(saveLocation, os.path.dirname(localFile)))
								if os.path.isfile(os.path.join(saveLocation, localFile)):
									if overwriteAsk == False:
										askOverwrite = wx.MessageDialog(None, "Some of the files you requested were already found. Would you like to overwrite them?", "Overwrite Existing Files?", wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)
										overwriteAsk = True
										if askOverwrite.ShowModal() == wx.ID_YES:
											overwriteSwitch = True
									if overwriteSwitch == True:
										lf = open(os.path.join(saveLocation, localFile), "wb")
										ftp.retrbinary("RETR " + baseDir + "/" + requestedFile, lf.write, 8*1024)
										lf.close()
								lf = open(os.path.join(saveLocation, localFile), "wb")
								ftp.retrbinary("RETR " + baseDir + "/" + requestedFile, lf.write, 8*1024)
								lf.close()
								saveCount = saveCount + 1
								if saveCount >= saveGoal:
									saveProgress.Destroy()
									successNotice = wx.MessageDialog(None, 'The files you requested were downloaded successfully.', 'Request was Successful', wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP)
									successNotice.ShowModal()
								else:
									saveProgress.Update(saveCount, saveMsg)
						saveRequest.Destroy()
				selectFiles.Destroy()
			else:
				noFiles = wx.MessageDialog(None, 'Connection was successful, but there are no files in your Recieve Location available to download. Please contact your archivist for more details.', 'No Files Available', wx.OK | wx.ICON_WARNING | wx.STAY_ON_TOP)
				noFiles.ShowModal()

			ftp.quit()
		
	except (Exception, ValueError) as e:
		#Error message that logs and shows error, but does not exit programs
		exceptMsg = traceback.format_exc()
		errorOutput = "\n" + "#############################################################\n" + str(datetime.datetime.utcnow()) + "\n#############################################################\n" + str(exceptMsg) + "\n********************************************************************************"
		print exceptMsg
		file = open(os.path.join(self.appData, "errorLog.txt"), "a")
		file.write(errorOutput)
		file.close()
		try:
			configXML = os.path.join(self.appData, "config.xml")
			parser = ET.XMLParser(remove_blank_text=True)
			configParse = ET.parse(configXML, parser)
			config = configParse.getroot()
			if config.find("error").text == "verbose":
				pass
			else:
				exceptMsg = e
		except:
			exceptMsg = e
		errorPopup = wx.MessageDialog(None, "Failed to Receive Files" + "\n\n" + str(exceptMsg), "Failed to Receive Files", wx.OK | wx.ICON_ERROR)
		errorPopup.ShowModal()