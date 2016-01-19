from lxml import etree as ET
import subprocess
import time
import csv
import os
import sys
import calendar
import datetime
from cStringIO import StringIO

def recordEvents(self, dirXML):

	def launchWithoutConsole(command, args):
		#Launches 'command' windowless and waits until finished
		#found at http://code.activestate.com/recipes/409002-launching-a-subprocess-without-a-console-window/
		startupinfo = subprocess.STARTUPINFO()
		startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		return subprocess.Popen([command] + args, startupinfo=startupinfo, shell=False, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	
	#get time option
	if self.timeZoneOption.GetSelection() == 1:
		#posix time
		timeType = "posix"
	elif self.timeZoneOption.GetSelection() == 2:
		#utc time
		timeType = "utc"
	else:
		#local time
		if time.daylight == 1:
			timeType = "local+" + str(time.altzone / 3600) + ":00"
		else:
			timeType = "local+" + str(time.timezone / 3600) + ":00"
	
	if self.adminTest == True:
		
		for item in dirXML.iter():
			if "name" in item.attrib:
				if item.attrib["check"] == "True":
					self.progressMsg = self.progressMsgRoot + "Reading MFT for " + item.attrib["name"] + "..."
					self.progressBar.Update(self.progressCount, self.progressMsg)
					readMFT = launchWithoutConsole("tools\\MFTRCRD.exe", [item.find("path").text, '-d', 'indxdump=off', '1024', '-s'])
					out, err = readMFT.communicate()
					recordEvents = ET.Element("recordEvents")
					item.insert(5, recordEvents)
					out2 = out.replace("\n", "</line><line>")
					out3 = out2.replace("<line>\r</line>", "</block><block>")
					out4 = "<root><block><line>" + out3 + "</line></block></root>"
					out5 = out4.replace("\n", "")
					out6 = out5.replace("\r", "")
					out7 = out6.replace("<line></line>", "")
					try:
						output = ET.fromstring(out7)
						for line in output.iter("line"):
							if line.text.strip().startswith("$STANDARD_INFORMATION 1:"):
								SI = line.getparent()
								for timestamp in SI:
									if timestamp.text.strip().startswith("File Create Time (CTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										mftrcrdTime = timestamp.text.split(": ")[1].strip()[:-9]
										mftrcrdPattern = "%Y-%m-%d %H:%M:%S"
										timeString = str(calendar.timegm(time.strptime(mftrcrdTime, mftrcrdPattern)))
										timestampXML.text = self.timestampOutput(timeString)
										timestampXML.set("source", "NTFS")
										timestampXML.set("timeType", timeType)
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "STANDARD_INFORMATION")
										timestampXML.set("label", "File_Create_Time")
									elif timestamp.text.strip().startswith("File Modified Time (ATime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										mftrcrdTime = timestamp.text.split(": ")[1].strip()[:-9]
										mftrcrdPattern = "%Y-%m-%d %H:%M:%S"
										timeString = str(calendar.timegm(time.strptime(mftrcrdTime, mftrcrdPattern)))
										timestampXML.text = self.timestampOutput(timeString)
										timestampXML.set("source", "NTFS")
										timestampXML.set("timeType", timeType)
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "STANDARD_INFORMATION")
										timestampXML.set("label", "File_Modified_Time")
									elif timestamp.text.strip().startswith("MFT Entry modified Time (MTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										mftrcrdTime = timestamp.text.split(": ")[1].strip()[:-9]
										mftrcrdPattern = "%Y-%m-%d %H:%M:%S"
										timeString = str(calendar.timegm(time.strptime(mftrcrdTime, mftrcrdPattern)))
										timestampXML.text = self.timestampOutput(timeString)
										timestampXML.set("source", "NTFS")
										timestampXML.set("timeType", timeType)
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "STANDARD_INFORMATION")
										timestampXML.set("label", "MFT_Entry_modified_Time")
									elif timestamp.text.strip().startswith("File Last Access Time (RTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										mftrcrdTime = timestamp.text.split(": ")[1].strip()[:-9]
										mftrcrdPattern = "%Y-%m-%d %H:%M:%S"
										timeString = str(calendar.timegm(time.strptime(mftrcrdTime, mftrcrdPattern)))
										timestampXML.text = self.timestampOutput(timeString)
										timestampXML.set("source", "NTFS")
										timestampXML.set("timeType", timeType)
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "STANDARD_INFORMATION")
										timestampXML.set("label", "File_Last_Access_Time")
							elif line.text.strip().startswith("$FILE_NAME 1:"):
								FN = line.getparent()
								for timestamp in FN:
									if timestamp.text.strip().startswith("File Create Time (CTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										mftrcrdTime = timestamp.text.split(": ")[1].strip()[:-9]
										mftrcrdPattern = "%Y-%m-%d %H:%M:%S"
										timeString = str(calendar.timegm(time.strptime(mftrcrdTime, mftrcrdPattern)))
										timestampXML.text = self.timestampOutput(timeString)
										timestampXML.set("source", "NTFS")
										timestampXML.set("timeType", timeType)
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "FILE_NAME")
										timestampXML.set("label", "File_Create_Time")
									elif timestamp.text.strip().startswith("File Modified Time (ATime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										mftrcrdTime = timestamp.text.split(": ")[1].strip()[:-9]
										mftrcrdPattern = "%Y-%m-%d %H:%M:%S"
										timeString = str(calendar.timegm(time.strptime(mftrcrdTime, mftrcrdPattern)))
										timestampXML.text = self.timestampOutput(timeString)
										timestampXML.set("source", "NTFS")
										timestampXML.set("timeType", timeType)
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "FILE_NAME")
										timestampXML.set("label", "File_Modified_Time")
									elif timestamp.text.strip().startswith("MFT Entry modified Time (MTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										mftrcrdTime = timestamp.text.split(": ")[1].strip()[:-9]
										mftrcrdPattern = "%Y-%m-%d %H:%M:%S"
										timeString = str(calendar.timegm(time.strptime(mftrcrdTime, mftrcrdPattern)))
										timestampXML.text = self.timestampOutput(timeString)
										timestampXML.set("source", "NTFS")
										timestampXML.set("timeType", timeType)
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "FILE_NAME")
										timestampXML.set("label", "MFT_Entry_modified_Time")
									elif timestamp.text.strip().startswith("File Last Access Time (RTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										mftrcrdTime = timestamp.text.split(": ")[1].strip()[:-9]
										mftrcrdPattern = "%Y-%m-%d %H:%M:%S"
										timeString = str(calendar.timegm(time.strptime(mftrcrdTime, mftrcrdPattern)))
										timestampXML.text = self.timestampOutput(timeString)
										timestampXML.set("source", "NTFS")
										timestampXML.set("timeType", timeType)
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "FILE_NAME")
										timestampXML.set("label", "File_Last_Access_Time")
						eventMFTRCRD = ET.Element("event")
						eventTime = str(calendar.timegm(time.gmtime()))
						eventMFTRCRD.set("timestamp", self.timestampOutput(eventTime))
						eventMFTRCRD.text = "ran MFTRCRD to gather NTFS timestamps"
						item.find("curatorialEvents").append(eventMFTRCRD)
					except:
						raise ValueError("Failed to parse MFTRCRD output.")
				self.progressCount = self.progressCount + 1
		print "ran MFTRCRD"
		
	else:
		if self.timestampOption.GetSelection() == 0:
			#use os.stat to gather timestamps
			for item in dirXML.iter():
				if "name" in item.attrib:
					if item.attrib["check"] == "True":
						self.progressMsg = self.progressMsgRoot + "Reading timestamps for " + item.attrib["name"] + "..."
						self.progressBar.Update(self.progressCount, self.progressMsg)
						(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(item.find("path").text)
						recordEvents = ET.Element("recordEvents")
						item.insert(5, recordEvents)
						atimeXML = ET.SubElement(recordEvents, "timestamp")
						atimeXML.text = self.timestampOutput(str(atime))
						atimeXML.set("source", "NTFS")
						atimeXML.set("timeType", timeType)
						atimeXML.set("parser", "os.path")
						atimeXML.set("type", "STANDARD_INFORMATION")
						atimeXML.set("label", "atime")
						
						mtimeXML = ET.SubElement(recordEvents, "timestamp")
						mtimeXML.text = self.timestampOutput(str(mtime))
						mtimeXML.set("source", "NTFS")
						mtimeXML.set("timeType", timeType)
						mtimeXML.set("parser", "os.path")
						mtimeXML.set("type", "STANDARD_INFORMATION")
						mtimeXML.set("label", "mtime")
						
						ctimeXML = ET.SubElement(recordEvents, "timestamp")
						ctimeXML.text = self.timestampOutput(str(ctime))
						ctimeXML.set("source", "NTFS")
						ctimeXML.set("timeType", timeType)
						ctimeXML.set("parser", "os.path")
						ctimeXML.set("type", "STANDARD_INFORMATION")
						ctimeXML.set("label", "ctime")
						
						eventOsStat = ET.Element("event")
						eventTime = str(calendar.timegm(time.gmtime()))
						eventOsStat.set("timestamp", self.timestampOutput(eventTime))
						eventOsStat.text = "ran os.stat to gather NTFS timestamps"
						item.find("curatorialEvents").append(eventOsStat)
			print "ran os.stat to gather NTFS timestamps"
			self.progressCount = self.progressCount + 1
										
		else:
			#run the Plaso Engine to gather record-events
			try:
				self.progressMsg = self.progressMsgRoot + "Reading timestamps"
				self.progressBar.Update(self.progressCount, self.progressMsg)
				
				#remove old files is present
				if os.path.isfile(os.path.join(self.appData, "~output.plaso")):
					os.remove(os.path.join(self.appData, "~output.plaso"))
				if os.path.isfile(os.path.join(self.appData, "~plaso.csv")):
					os.remove(os.path.join(self.appData, "~plaso.csv"))
				
				timeZone = "UTC"
				out = ""
				self.progressMsg = self.progressMsgRoot + "Running Plaso Engine...(may take up to 1 minute)"
				self.progressCount = self.progressCount + 1
				self.progressBar.Update(self.progressCount, self.progressMsg)
				runLog2timeline = subprocess.Popen(["tools\\plaso\\log2timeline.exe", os.path.join(self.appData, "~output.plaso"), self.sourceDir], shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
				self.progressCount = self.progressCount + 1
				self.progressBar.Update(self.progressCount, self.progressMsg)
					
				output = runLog2timeline.communicate()[0]
				exitCode = runLog2timeline.returncode
				readTimeline = subprocess.Popen(["tools\\plaso\\psort.exe", "-o", "dynamic", "-w", os.path.join(self.appData, "~plaso.csv"), "-z", timeZone, os.path.join(self.appData, "~output.plaso")])
				out, err = readTimeline.communicate()
				
				for item in dirXML.iter():
					if "name" in item.attrib:
						if item.attrib["check"] == "True":
							recordEvents = ET.Element("recordEvents")
							item.insert(4, recordEvents)
							output = csv.reader(open(os.path.join(self.appData, "~plaso.csv")), delimiter=",")
							for row in output:
								if row[4].replace("OS:", "") == item.find("path").text:
									timestampXML = ET.SubElement(recordEvents, "timestamp")
									plasoTime = row[0].split("+")[0]
									plasoPattern = "%Y-%m-%dT%H:%M:%S"
									timeString = str(calendar.timegm(time.strptime(plasoTime, plasoPattern)))
									timestampXML.text = self.timestampOutput(timeString)
									timestampXML.set("source", row[2])
									timestampXML.set("timeType", timeType)
									timestampXML.set("parser", row[5])
									if row[2] == "atime" or row[2] == "ctime" or row[2] == "mtime":
										timestampXML.set("type", "STANDARD_INFORMATION")
									timestampXML.set("label", row[1])
									
							eventPlaso = ET.Element("event")
							eventTime = str(calendar.timegm(time.gmtime()))
							eventPlaso.set("timestamp", self.timestampOutput(eventTime))
							eventPlaso.text = "ran Plaso engine to gather record-events"
							item.find("curatorialEvents").append(eventPlaso)
						
					
				if os.path.isfile(os.path.join(self.appData, "~output.plaso")):
					os.remove(os.path.join(self.appData, "~output.plaso"))
				#if os.path.isfile(os.path.join(self.appData, "~plaso.csv")):
					#os.remove(os.path.join(self.appData, "~plaso.csv"))
				
				print "ran PLASO"
				self.progressCount = self.progressCount + 1
			except:
				raise ValueError("Failed to run Plaso.")

		
	return dirXML