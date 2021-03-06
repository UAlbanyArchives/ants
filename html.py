from lxml import etree as ET
import datetime
import calendar
import time
import os
import traceback
import wx


def htmlReceipt(self, file, timestamp, config):
	try:
		parser = ET.XMLParser(remove_blank_text=True)
		try:
			configParse = ET.parse(config, parser)
			configRoot = configParse.getroot()
		except:
			raise ValueError("Error reading configuration data. Please start ANTS by clicking \"Browse\" and try again." )
		if configRoot.find("requestEmail").text:
			requestEmail = configRoot.find("requestEmail").text
		else:
			requestEmail = ""
		if configRoot.find("requestSubject").text:
			requestSubject = configRoot.find("requestSubject").text
		else:
			requestSubject = ""
		if configRoot.find("requestBody").text:
			requestBody = configRoot.find("requestBody").text
		else:
			requestBody = ""

		parser = ET.XMLParser(remove_blank_text=True)
		xmlParse = ET.parse(file, parser)
		xmlRoot = xmlParse.getroot()
		
		html = ET.Element('html')
		
		head = ET.SubElement(html, "head")
		title = ET.SubElement(head, "title")
		title.text = "ANTS Receipt"
		link = ET.SubElement(head, "link")
		link.set("href", "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css")
		link.set("rel", "stylesheet")
		script1 = ET.SubElement(head, "script")
		script1.set("src", "https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js")
		script1.text = ""
		script2 = ET.SubElement(head, "script")
		script2.text = "$(document).ready(function(){$('.profile').hide();$('.clickHead').click(function(){$(this).siblings('.info').children().children('.profile').slideToggle('slow');$(this).children().children().toggleClass('glyphicon glyphicon-triangle-bottom glyphicon glyphicon-triangle-top')});});"
		
		body = ET.SubElement(html, "body")
		
		divMain = ET.SubElement(body, "div")
		divMain.set("class", "row-fluid")
		
		divLeft = ET.SubElement(divMain, "div")
		divLeft.set("valign", "top")
		divLeft.set("style", "position:fixed; height:100%; margin:0px; padding:10px; width:30%;overflow-y: scroll;direction: rtl;")
		
		divJumbo = ET.SubElement(divLeft, "div")
		h1 = ET.SubElement(divJumbo, "h1")
		h1.set("class", "h1")
		h1.text = "ANTS Receipt"
		h5 = ET.SubElement(divLeft, "h5")
		h5.set("class", "h5")
		h5.text = "Generated " + timestamp
		
		tableLeft = ET.SubElement(divLeft, "table")
		tableLeft.set("class", "table")
		tableLeft.set("style", "direction:ltr;")
		tr1 = ET.SubElement(tableLeft, "tr")
		th1 = ET.SubElement(tr1, "th")
		th1.text = "Accession"
		th2 = ET.SubElement(tr1, "th")
		th2.text = "Submitted"
		
		for accessionLeft in xmlRoot:
			number = accessionLeft.attrib['number']
			submitted = accessionLeft.attrib['submitted']
			if "time" in accessionLeft.attrib:
				if accessionLeft.attrib["time"] == "posix":
					localSubmit = datetime.datetime.fromtimestamp(int(submitted)).strftime('%Y-%m-%d %H:%M:%S')
				elif accessionLeft.attrib["time"] == "utc":
					timePattern = "%Y-%m-%d %H:%M:%S"
					posixTime = str(calendar.timegm(time.strptime(submitted, timePattern)))
					localSubmit = datetime.datetime.fromtimestamp(int(posixTime)).strftime('%Y-%m-%d %H:%M:%S')
				else:
					localSubmit = submitted
			else:
				localSubmit = submitted
			trLeft = ET.SubElement(tableLeft, "tr")
			trLeft.set("class", "success")
			tdLeft1 = ET.SubElement(trLeft, "td")
			aLink = ET.SubElement(tdLeft1, "a")
			aLink.set("href", "#" + number)
			if len(number) > 15:
				aLink.text = number[0:15] + "..."
			else:
				aLink.text = number
			tdLeft2 = ET.SubElement(trLeft, "td")
			tdLeft2.text = localSubmit
			
			
		###########################################################
		
		divRight = ET.SubElement(divMain, "div")
		divRight.set("style", "width: 67%; height: auto; position: absolute; right: 0; padding:10px")
		
		for accessionRight in xmlRoot:
			number = accessionRight.attrib['number']
			submitted = accessionRight.attrib['submitted']
			if "time" in accessionRight.attrib:
				if accessionRight.attrib["time"] == "posix":
					localSubmit = datetime.datetime.fromtimestamp(int(submitted)).strftime('%Y-%m-%d %H:%M:%S')
				elif accessionRight.attrib["time"] == "utc":
					timePattern = "%Y-%m-%d %H:%M:%S"
					posixTime = str(calendar.timegm(time.strptime(submitted, timePattern)))
					localSubmit = datetime.datetime.fromtimestamp(int(posixTime)).strftime('%Y-%m-%d %H:%M:%S')
				else:
					localSubmit = submitted
			else:
				localSubmit = submitted
			tableRight = ET.SubElement(divRight, "table")
			tableRight.set("id", number)
			tableRight.set("class", "table")
			tableRight.set("style", "width:100%;border:1px solid #7DA9D4")
			
			trRight1 = ET.SubElement(tableRight, "tr")
			trRight1.set("class", "clickHead")
			th3 = ET.SubElement(trRight1, "th")
			th3.set("colspan", "4")
			th3.set("style", "background-color:#7DA9D4; cursor:pointer;")
			th3.text = number + " <span class=\"glyphicon glyphicon-triangle-bottom\" />"
			
			trProfile = ET.SubElement(tableRight, "tr")
			trProfile.set("class", "info")
			tdProfile = ET.SubElement(trProfile, "td")
			tdProfile.set("colspan", "4")
			divProfile = ET.SubElement(tdProfile, "div")
			divProfile.set("class", "profile")
			divProfile.set("display", "block")
			tableProfile = ET.SubElement(divProfile, "table")
			tableProfile.set("width", "100%")
			trRight2 = ET.SubElement(tableProfile, "tr")			
			trRight2.set("class", "info")				
			thLabel2 = ET.SubElement(trRight2, "th")
			thLabel2.set("width", "10%")
			trData2 = ET.SubElement(trRight2, "td")
			trData2.set("width", "80%")
			trData2.set("colspan", "4")
			thLabel2.text = "submitted:"
			trData2.text = localSubmit
			for profile in accessionRight.find("profile"):
				trRight3 = ET.SubElement(tableProfile, "tr")			
				trRight3.set("class", "info")				
				thLabel3= ET.SubElement(trRight3, "th")
				thLabel3.set("width", "10%")
				trData3 = ET.SubElement(trRight3, "td")
				trData3.set("width", "80%")
				trData3.set("colspan", "4")
				thLabel3.text = profile.tag + ":"
				trData3.text = profile.text
			
			trRight14 = ET.SubElement(tableRight, "tr")
			th4 = ET.SubElement(trRight14, "th")
			th4.text = "Name"
			th5 = ET.SubElement(trRight14, "th")
			th5.text = "Type"
			th7 = ET.SubElement(trRight14, "th")
			th7.text = "ID"
			th8 = ET.SubElement(trRight14, "th")
			th8.text = "Request"
			
			for item in accessionRight:
				if item.tag == "item":
					itemRow = ET.SubElement(tableRight, "tr")
					tdRight1 = ET.SubElement(itemRow, "td")
					tdRight2 = ET.SubElement(itemRow, "td")
					tdRight4 = ET.SubElement(itemRow, "td")
					tdRight5 = ET.SubElement(itemRow, "td")
					tdRight1.text = item.find("name").text
					tdRight2.text = item.find("type").text
					tdRight4.text = item.find("id").text
					requestLink = ET.SubElement(tdRight5, "a")
					subject = requestSubject.replace(" ", "%20")
					requestBodyItem = requestBody + "%0D%0AAccession: " + accessionRight.attrib["number"] + "%0D%0ASubmitted: " + accessionRight.attrib["submitted"] + "%0D%0A%0D%0AName: " + item.find("name").text + "%0D%0AType: " + item.find("type").text + "%0D%0AID: " + item.find("id").text
					body = requestBodyItem.replace(" ", "%20")
					if len(subject) > 0:
						requestLink.set("href", "mailto:" + requestEmail + "?subject=" + subject + "&body=" + body)
					else:
						requestLink.set("href", "mailto:" + requestEmail + "?body=" + body)
					requestLink.text = "Request"
					
		
		
		htmlString = ET.tostring(html, pretty_print=True)
		stringFix = htmlString.replace("&lt;", "<")
		stringFix2 = stringFix.replace("&gt;", ">")
		return stringFix2
	except (Exception, ValueError) as e:
		#Error message that logs and shows error, but does not exit program
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