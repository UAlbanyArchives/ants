from lxml import etree as ET
import subprocess
from time import gmtime, strftime
import csv
import os
import sys
from cStringIO import StringIO

def recordEvents(self, dirXML):

	def launchWithoutConsole(command, args):
		#Launches 'command' windowless and waits until finished
		#found at http://code.activestate.com/recipes/409002-launching-a-subprocess-without-a-console-window/
		startupinfo = subprocess.STARTUPINFO()
		startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		return subprocess.Popen([command] + args, startupinfo=startupinfo, shell=False, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	
	if self.adminTest == True:
		
		for item in dirXML.iter():
			if "name" in item.attrib:
				if item.attrib["check"] == "True":
					self.progressMsg = self.progressMsgRoot + "Reading MFT for " + item.attrib["name"] + "..."
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
					readMFT = launchWithoutConsole("tools\\MFTRCRD.exe", [item.find("path").text, '-d', 'indxdump=off', '1024', '-s'])
					out, err = readMFT.communicate()
					recordEvents = ET.Element("recordEvents")
					item.insert(4, recordEvents)
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
										timestampXML.text = timestamp.text.split(": ")[1].strip().replace(" ", "T")
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()).replace("Eastern Standard Time", "EST"))
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "STANDARD_INFORMATION")
										timestampXML.set("label", "File_Create_Time")
									elif timestamp.text.strip().startswith("File Modified Time (ATime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip().replace(" ", "T")
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()).replace("Eastern Standard Time", "EST"))
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "STANDARD_INFORMATION")
										timestampXML.set("label", "File_Modified_Time")
									elif timestamp.text.strip().startswith("MFT Entry modified Time (MTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip().replace(" ", "T")
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()).replace("Eastern Standard Time", "EST"))
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "STANDARD_INFORMATION")
										timestampXML.set("label", "MFT_Entry_modified_Time")
									elif timestamp.text.strip().startswith("File Last Access Time (RTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip().replace(" ", "T")
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()).replace("Eastern Standard Time", "EST"))
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "STANDARD_INFORMATION")
										timestampXML.set("label", "File_Last_Access_Time")
							elif line.text.strip().startswith("$FILE_NAME 1:"):
								FN = line.getparent()
								for timestamp in FN:
									if timestamp.text.strip().startswith("File Create Time (CTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip().replace(" ", "T")
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()).replace("Eastern Standard Time", "EST"))
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "FILE_NAME")
										timestampXML.set("label", "File_Create_Time")
									elif timestamp.text.strip().startswith("File Modified Time (ATime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip().replace(" ", "T")
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()).replace("Eastern Standard Time", "EST"))
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "FILE_NAME")
										timestampXML.set("label", "File_Modified_Time")
									elif timestamp.text.strip().startswith("MFT Entry modified Time (MTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip().replace(" ", "T")
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()).replace("Eastern Standard Time", "EST"))
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "FILE_NAME")
										timestampXML.set("label", "MFT_Entry_modified_Time")
									elif timestamp.text.strip().startswith("File Last Access Time (RTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip().replace(" ", "T")
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()).replace("Eastern Standard Time", "EST"))
										timestampXML.set("parser", "MFTRCRD")
										timestampXML.set("type", "FILE_NAME")
										timestampXML.set("label", "File_Last_Access_Time")
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
						self.networkProcessing.Update(self.progressCount, self.progressMsg)
						(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(item.find("path").text)
						recordEvents = ET.Element("recordEvents")
						item.insert(4, recordEvents)
						atimeXML = ET.SubElement(recordEvents, "timestamp")
						atimeXML.text = str(atime)
						atimeXML.set("source", "NTFS")
						atimeXML.set("timezone", strftime("%z", gmtime()).replace("Eastern Standard Time", "EST"))
						atimeXML.set("parser", "os.path")
						atimeXML.set("type", "STANDARD_INFORMATION")
						atimeXML.set("label", "atime")
						
						mtimeXML = ET.SubElement(recordEvents, "timestamp")
						mtimeXML.text = str(mtime)
						mtimeXML.set("source", "NTFS")
						mtimeXML.set("timezone", strftime("%z", gmtime()).replace("Eastern Standard Time", "EST"))
						mtimeXML.set("parser", "os.path")
						mtimeXML.set("type", "STANDARD_INFORMATION")
						mtimeXML.set("label", "mtime")
						
						ctimeXML = ET.SubElement(recordEvents, "timestamp")
						ctimeXML.text = str(ctime)
						ctimeXML.set("source", "NTFS")
						ctimeXML.set("timezone", strftime("%z", gmtime()).replace("Eastern Standard Time", "EST"))
						ctimeXML.set("parser", "os.path")
						ctimeXML.set("type", "STANDARD_INFORMATION")
						ctimeXML.set("label", "ctime")
			print "ran os.stat for timestamps"
			self.progressCount = self.progressCount + 1
										
		else:
			#run the Plaso Engine to gather record-events
			#try:
			self.progressMsg = self.progressMsgRoot + "Reading timestamps"
			self.networkProcessing.Update(self.progressCount, self.progressMsg)
			if strftime("%z", gmtime()) == "Eastern Standard Time":
				timeZone = "US/Eastern"
			else:
				timeZone = "UTC"
			out = ""
			runLog2timeline = subprocess.Popen(["tools\\plaso\\log2timeline.exe", "~output.plaso", self.sourceDir], shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
			while len(out) < 1:
				nextline = runLog2timeline.stdout.readline()
				self.progressMsg = self.progressMsgRoot + str(nextline)
				self.networkProcessing.Update(self.progressCount, self.progressMsg)
				if nextline == '' and runLog2timeline.poll() != None:
					break
				sys.stdout.write(nextline)
				sys.stdout.flush()
				#count = count + 1
				#self.progressMsg = self.progressMsgRoot + str(count)
				#self.progressCount = self.progressCount + 1
				#self.networkProcessing.Update(self.progressCount, self.progressMsg)
				
			output = runLog2timeline.communicate()[0]
			exitCode = runLog2timeline.returncode
			readTimeline = subprocess.Popen(["tools\\plaso\\psort.exe", "-o", "dynamic", "-w", "~plaso.csv", "-z", timeZone, "~output.plaso"])
			out, err = readTimeline.communicate()
			
			for item in dirXML.iter():
				if "name" in item.attrib:
					if item.attrib["check"] == "True":
						recordEvents = ET.Element("recordEvents")
						item.insert(4, recordEvents)
						output = csv.reader(open("~plaso.csv"), delimiter=",")
						for row in output:
							if row[4].replace("OS:", "") == item.find("path").text:
								timestampXML = ET.SubElement(recordEvents, "timestamp")
								timestampXML.text = row[0]
								timestampXML.set("source", row[2])
								timestampXML.set("timezone", timeZone)
								timestampXML.set("parser", row[5])
								if row[2] == "atime" or row[2] == "ctime" or row[2] == "mtime":
									timestampXML.set("type", "STANDARD_INFORMATION")
								timestampXML.set("label", row[1])
					
				
			if os.path.isfile("~output.plaso"):
				os.remove("~output.plaso")
			#if os.path.isfile("~plaso.csv"):
				#os.remove("~plaso.csv")
			
			print "ran PLASO"
			self.progressCount = self.progressCount + 1
			#except:
				#raise ValueError("Failed to run Plaso.")

		
	return dirXML