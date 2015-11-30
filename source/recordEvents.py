from lxml import etree as ET
import subprocess
import admin

def recordEvents(sourceDir, dirXML):

	
	if not admin.isUserAdmin():
		print "run PLASO"
	else:
	
		for item in dirXML.iter():
			if "name" in item.attrib:
				readMFT = subprocess.Popen(['tools\\MFTRCRD.exe', item.find("path").text, '-d', 'indxdump=off', '1024', '-s'], stdout=subprocess.PIPE)
				out, err = readMFT.communicate()
				if not err is None:
					print "Errors: " + str(err)
				else:
					recordEvents = ET.SubElement(item, "recordEvents")
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
								STANDARD_INFORMATION = ET.SubElement(recordEvents, "STANDARD_INFORMATION")
								for timestamp in SI:
									if timestamp.text.strip().startswith("File Create Time (CTime):"):
										CTime = ET.SubElement(STANDARD_INFORMATION, "CTime")
										CTime.text = timestamp.text.split(": ")[1].strip()
										CTime.set("type", "File_Create_Time")
									elif timestamp.text.strip().startswith("File Modified Time (ATime):"):
										ATime = ET.SubElement(STANDARD_INFORMATION, "ATime")
										ATime.text = timestamp.text.split(": ")[1].strip()
										ATime.set("type", "File_Modified_Time")
									elif timestamp.text.strip().startswith("MFT Entry modified Time (MTime):"):
										MTime = ET.SubElement(STANDARD_INFORMATION, "MTime")
										MTime.text = timestamp.text.split(": ")[1].strip()
										MTime.set("type", "MFT_Entry_modified_Time")
									elif timestamp.text.strip().startswith("File Last Access Time (RTime):"):
										RTime = ET.SubElement(STANDARD_INFORMATION, "RTime")
										RTime.text = timestamp.text.split(": ")[1].strip()
										RTime.set("type", "File_Last_Access_Time")
							elif line.text.strip().startswith("$FILE_NAME 1:"):
								FN = line.getparent()
								FILE_NAME = ET.SubElement(recordEvents, "FILE_NAME")
								for timestamp in FN:
									if timestamp.text.strip().startswith("File Create Time (CTime):"):
										CTime = ET.SubElement(FILE_NAME, "CTime")
										CTime.text = timestamp.text.split(": ")[1].strip()
										CTime.set("type", "File_Create_Time")
									elif timestamp.text.strip().startswith("File Modified Time (ATime):"):
										ATime = ET.SubElement(FILE_NAME, "ATime")
										ATime.text = timestamp.text.split(": ")[1].strip()
										ATime.set("type", "File_Modified_Time")
									elif timestamp.text.strip().startswith("MFT Entry modified Time (MTime):"):
										MTime = ET.SubElement(FILE_NAME, "MTime")
										MTime.text = timestamp.text.split(": ")[1].strip()
										MTime.set("type", "MFT_Entry_modified_Time")
									elif timestamp.text.strip().startswith("File Last Access Time (RTime):"):
										RTime = ET.SubElement(FILE_NAME, "RTime")
										RTime.text = timestamp.text.split(": ")[1].strip()
										RTime.set("type", "File_Last_Access_Time")
					except:
						raise ValueError("Failed to parse MFTRCRD output.")
				
	
		#testProc = subprocess.Popen(['C:\\Projects\\fsTools\\MftRcrd\\MFTRCRD.exe', 'C:\\Projects\\test2.py', '-d', 'indxdump=off', '1024', '-s'], stdout=subprocess.PIPE)
		#out, err = testProc.communicate()
		
		print "ran MFTRCRD"

		
	return dirXML