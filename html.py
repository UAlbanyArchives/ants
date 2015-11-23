from lxml import etree as ET


def htmlReceipt(file, timestamp, config):
	parser = ET.XMLParser(remove_blank_text=True)
	configParse = ET.parse(config, parser)
	configRoot = configParse.getroot()
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
	link.set("href", "https://maxcdn.bootstrapcdn.com/bootstrap/2.3.2/css/bootstrap.min.css")
	link.set("rel", "stylesheet")
	
	body = ET.SubElement(html, "body")
	
	divMain = ET.SubElement(body, "div")
	divMain.set("class", "row-fluid")
	
	divLeft = ET.SubElement(divMain, "div")
	divLeft.set("valign", "top")
	divLeft.set("style", "position:fixed; height:100%; margin:0px; padding:10px; width:30%;")
	
	divJumbo = ET.SubElement(divLeft, "div")
	divJumbo.set("class", "jumbotron")
	h1 = ET.SubElement(divJumbo, "h1")
	h1.set("class", "h1")
	h1.text = "ANTS Receipt"
	h5 = ET.SubElement(divLeft, "h5")
	h5.set("class", "h5")
	h5.text = "Generated " + timestamp
	
	tableLeft = ET.SubElement(divLeft, "table")
	tableLeft.set("class", "table")
	tr1 = ET.SubElement(tableLeft, "tr")
	th1 = ET.SubElement(tableLeft, "th")
	th1.text = "Accession"
	th2 = ET.SubElement(tableLeft, "th")
	th2.text = "Submitted"
	
	for accessionLeft in xmlRoot:
		number = accessionLeft.attrib['number']
		submitted = accessionLeft.attrib['submitted']
		trLeft = ET.SubElement(tableLeft, "tr")
		trLeft.set("class", "success")
		tdLeft1 = ET.SubElement(trLeft, "td")
		aLink = ET.SubElement(tdLeft1, "a")
		aLink.set("href", "#" + number)
		aLink.text = number
		tdLeft2 = ET.SubElement(trLeft, "td")
		tdLeft2.text = submitted
		
		
	###########################################################
	
	divRight = ET.SubElement(divMain, "div")
	divRight.set("style", "width: 67%; height: auto; position: absolute; right: 0; padding:10px")
	
	for accessionRight in xmlRoot:
		number = accessionRight.attrib['number']
		submitted = accessionRight.attrib['submitted']
		tableRight = ET.SubElement(divRight, "table")
		tableRight.set("id", number)
		tableRight.set("class", "table table-hover")
		tableRight.set("style", "width:100%;border:1px solid #7DA9D4")
		
		trRight1 = ET.SubElement(tableRight, "tr")
		th3 = ET.SubElement(trRight1, "th")
		th3.set("colspan", "5")
		th3.set("style", "background-color:#7DA9D4")
		th3.text = number
		
		trRight2 = ET.SubElement(tableRight, "tr")
		th4 = ET.SubElement(trRight2, "th")
		th4.text = "Name"
		th5 = ET.SubElement(trRight2, "th")
		th5.text = "Type"
		th6 = ET.SubElement(trRight2, "th")
		th6.text = "Path"
		th7 = ET.SubElement(trRight2, "th")
		th7.text = "ID"
		th8 = ET.SubElement(trRight2, "th")
		th8.text = "Request"
		
		for item in accessionRight:
			if item.tag == "item":
				itemRow = ET.SubElement(tableRight, "tr")
				tdRight1 = ET.SubElement(itemRow, "td")
				tdRight2 = ET.SubElement(itemRow, "td")
				tdRight3 = ET.SubElement(itemRow, "td")
				tdRight4 = ET.SubElement(itemRow, "td")
				tdRight5 = ET.SubElement(itemRow, "td")
				tdRight1.text = item.find("name").text
				tdRight2.text = item.find("type").text
				tdRight3.text = item.find("path").text
				tdRight4.text = item.find("id").text
				requestLink = ET.SubElement(tdRight5, "a")
				subject = requestSubject.replace(" ", "%20")
				body = requestBody.replace(" ", "%20")
				requestLink.set("href", "mailto:" + requestEmail + "?subject=" + subject + "&body=" + body)
				requestLink.text = "Request"
				
	
	
	htmlString = ET.tostring(html, pretty_print=True)
	return htmlString