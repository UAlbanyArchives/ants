from lxml import etree as ET
import subprocess
from time import gmtime, strftime

def recordEvents(self, dirXML):
	
	if self.adminTest == True:
		
		for item in dirXML.iter():
			if "name" in item.attrib:
				if item.attrib["check"] == "True":
					self.progressMsg = self.progressMsgRoot + "Reading MFT for " + item.attrib["name"] + "..."
					self.networkProcessing.Update(self.progressCount, self.progressMsg)
					readMFT = subprocess.Popen(["tools\\MFTRCRD.exe", item.find("path").text, '-d', 'indxdump=off', '1024', '-s'], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
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
										timestampXML.text = timestamp.text.split(": ")[1].strip()
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()))
										timestampXML.set("type", "STANDARD_INFORMATION")
										timestampXML.set("label", "File_Create_Time")
									elif timestamp.text.strip().startswith("File Modified Time (ATime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip()
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()))
										timestampXML.set("type", "STANDARD_INFORMATION")
										timestampXML.set("label", "File_Modified_Time")
									elif timestamp.text.strip().startswith("MFT Entry modified Time (MTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip()
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()))
										timestampXML.set("type", "STANDARD_INFORMATION")
										timestampXML.set("label", "MFT_Entry_modified_Time")
									elif timestamp.text.strip().startswith("File Last Access Time (RTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip()
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()))
										timestampXML.set("type", "STANDARD_INFORMATION")
										timestampXML.set("label", "File_Last_Access_Time")
							elif line.text.strip().startswith("$FILE_NAME 1:"):
								FN = line.getparent()
								for timestamp in FN:
									if timestamp.text.strip().startswith("File Create Time (CTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip()
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()))
										timestampXML.set("type", "FILE_NAME")
										timestampXML.set("label", "File_Create_Time")
									elif timestamp.text.strip().startswith("File Modified Time (ATime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip()
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()))
										timestampXML.set("type", "FILE_NAME")
										timestampXML.set("label", "File_Modified_Time")
									elif timestamp.text.strip().startswith("MFT Entry modified Time (MTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip()
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()))
										timestampXML.set("type", "FILE_NAME")
										timestampXML.set("label", "MFT_Entry_modified_Time")
									elif timestamp.text.strip().startswith("File Last Access Time (RTime):"):
										timestampXML = ET.SubElement(recordEvents, "timestamp")
										timestampXML.text = timestamp.text.split(": ")[1].strip()
										timestampXML.set("source", "NTFS")
										timestampXML.set("timezone", strftime("%z", gmtime()))
										timestampXML.set("type", "FILE_NAME")
										timestampXML.set("label", "File_Last_Access_Time")
					except:
						raise ValueError("Failed to parse MFTRCRD output.")
				self.progressCount = self.progressCount + 1
		print "ran MFTRCRD"
		
	else:
		print "run PLASO"

		
	return dirXML