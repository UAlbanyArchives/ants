import wx
import os
import subprocess
from lxml import etree as ET
import traceback
import datetime
import shutil

def produceReceipt(self, xmlSource):
	
	if not os.path.isfile("receipt.xml"):
		noReceipt = wx.MessageDialog(None, 'Unable to find a receipt. You must tranfer files in order to obtain a receipt.', 'No Receipt found', wx.OK | wx.ICON_WARNING)
		noReceipt.ShowModal()
	else:
	
		if xmlSource == True:
			configXML = "config.xml"
			parser = ET.XMLParser(remove_blank_text=True)
			configParse = ET.parse(configXML, parser)
			config = configParse.getroot()
			if config.find("receipt").text is None:
				receipt = "html"
			else:
				receipt = config.find("receipt").text
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
		elif receipt == "xml":
			shutil.copy2("receipt.xml", tempDir)
			subprocess.Popen(os.path.join(tempDir, "receipt.xml"), shell=True)
		else:
			from html import htmlReceipt
			htmlString = htmlReceipt("receipt.xml", str(datetime.datetime.now()), "config.xml")
			htmlFile = open(os.path.join(tempDir, "receipt.html"), "w")
			htmlFile.write(htmlString)
			htmlFile.close()
			subprocess.Popen(os.path.join(tempDir, "receipt.html"), shell=True)
				
				
###########################################################################################################################


def checkReceiveFiles(self, xmlSource):

	try:	
		#get the information needed from config.xml for the splash screen or the GUI from the options tab
		if xmlSource == True:
			configXML = "config.xml"
			parser = ET.XMLParser(remove_blank_text=True)
			configParse = ET.parse(configXML, parser)
			config = configParse.getroot()
			if config.find("transferMethod").text is None or config.find("receiveLocation").text is None:
				raise ValueError("Failed to receive files, both the transfer method and receive location must be entered in the config file.")
			transferMethod = config.find("transferMethod").text
			receiveLocation = config.find("receiveLocation").text
			if transferMethod != "network":
				if config.find("login").text is None or config.find("pw").text is None:
					print "issue here"
					raise ValueError("Failed to receive files, both the login and password must be entered in the GUI and set as default.")
				login = config.find("login").text
				pw = config.find("pw").text
		else:
			if self.m_radioBox1.GetSelection() == 0:
				transferMethod = "network"
			else:
				transferMethod = "ftp"
			receiveLocation = self.receiveInput.GetValue()
			if len(receiveLocation) < 1:
				raise ValueError("Failed to receive files, you must enter a local or network path as your transfer destination")
		
		
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
									os.mkdir(os.path.join(saveLocation, os.path.dirname(requestedFile)))
							if os.path.isfile(os.path.join(saveLocation, requestedFile)):
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
		else:
			print "receive FTP"
		
	except:
		#Error message that logs and shows error, but does not exit programs
		exceptMsg = traceback.format_exc()
		errorOutput = "\n" + "#############################################################\n" + str(datetime.datetime.now()) + "\n#############################################################\n" + str(exceptMsg) + "\n********************************************************************************"
		print exceptMsg
		file = open("errorLog.txt", "a")
		file.write(errorOutput)
		file.close()
		errorPopup = wx.MessageDialog(None, "Failed to Receive Files" + "\n\n" + str(exceptMsg), "ERROR", wx.OK | wx.ICON_ERROR)
		errorPopup.ShowModal()