# ANTS: Archives Network Transfer System

for executables to run without dependencies, see [http://library.albany.edu/archive/universityarchives/ants](http://library.albany.edu/archive/universityarchives/ants)

##Project Status

ANTS is offered as an open beta for external testing. Development is ongoing, but near-completion. further documentation will be available soon. Version 0.6+ includes:

* Support for GoogleDrive transfers from the GUI using the GoogleDrive API
* Email notifications

ANTS is available publicly primarily as a proof of concept and a tool for experimentation. While we hope to implement ANTS at the University at Albany, SUNY, any external users should plan to require their own development and support.

Comments, bug reports, and feature requests are welcome.

##Features

* Developed for records creators to describe, package, and transfer unstructured files to a university archives.
* GUI desktop application, runs on any Windows XP SP2+ and later without any dependencies.
* Makes use of basic digital forensics tools to gather filesystem metadata and create a robust SIP in records' native environment before transfer.
* Gathers MFT $STANDARDINFORMATION and $FILENAME MAC timestamps of each file.
* Designed to send reference requests and receive files from within the GUI.
* Transfers over network shares with existing LDAP authentication, FTP (with or without TLS), and GoogleDrive.
* Can be configured remotely prior to user installation.
* Maintains local receipt for all transferred materials with identification for easy future requests.
* Developed for Windows and NTFS filesystems.
* Can gather local, UTC, or POSIX timestamps.

#Quick Start Guide
___________
ANTS runs on a Windows desktop and is designed to package digital records with contextual metadata and transfer them to an institutional archives.

###Requirements
ANTS requires Windows XP SP2 or later. It has been tested on Windows 7 and Windows 10.

##Installing ANTS

ANTS can be set up in three different ways:

* Setup Installer with config.xml
* Setup Installer
* Portable .EXE files with tools folder

##### Setup Installer with config.xml
![](http://library.albany.edu/libdru/files/images/installerConfig.png)

ANTS is designed to be set up remotely with an XML configuration file. If you have been provided a link to a .zip file, extract the contents and you should see two files:

* setup-ANTS-X.X.exe
* config.xml

Just make sure the config.xml file is in the same directory as the .EXE installer and run the .EXE to install ANTS with configuration settings. This may already contain details on the method of transfer, configuration, user metadata, etc., so you won't have to enter this information while running ANTS. Continue below for more details on the setup installer process.

##### Setup Installer
![](http://library.albany.edu/libdru/files/images/installer.png)

Just download the 32-bit .EXE installer and use the wizard to install ANTS. You will be asked to provide the installer with elevated privileges. If you are not able to use the installer because of this, download the Portable .ZIP and follow the instructions below.

The installer gives you three options:

![](http://library.albany.edu/libdru/files/images/installerOptions.png)

* You can add a short cut in your Start Menu (default on)
* You can add a link to ANTS in your Context Menu, this is the "right-click" menu. If you select this option, you can right-click on any file or folder and send it to the Archives in two clicks or more. (default on)
* You can add a shortcut on your desktop (default off)

The installer will let you pick an installation and then extract its contents there. This will install ANTS with MFTRCRD and Plaso. ANTS also comes with an uninstaller that removes ANTS and all the shortcuts you installed. It is located in the installation directory you selected.


##### Portable .ZIP package
![](http://library.albany.edu/libdru/files/images/portableZip.png)

Ants also comes in and portable package for users without administrative privileges. Download the .ZIP package and extract it to wherever you would like to run ANTS. Run ANTS.exe to start the program. If a config.xml file is present in the same directory, it will be used to configure ANTS just as with the installer.


##Transferring Records

Run ANTS.exe to start the program. If you setup ANTS with an installer, a shortcut may be in you Start Menu or on your Desktop if you selected that option. You will see the ANTS welcome screen:

![](http://library.albany.edu/libdru/files/images/splash.png)

Select "Browse..." to select the records you want to transfer. ANTS will ask you to elevate privileges to run antsFromBoot.exe. This will enable ANTS to gather detailed about the records that will enable us to demonstrate their authenticity years in the future. If you are unable to provide administrative privileges, you will not be prompted and you can still run ANTS to transfer your records.

#####Opening ANTS from the Context Menu
If you set up ANTS with the installer and selected the appropriate option, you will be able to access ANTS from your "right-click" menu. Just navigate to the records you want to transfer and right-click on a file or folder and select "Send to the Archives with ANTS." This will open the main window as detailed below.

![](http://library.albany.edu/libdru/files/images/contextMenu.png)

#####Selecting Records

Select the directory that contains your records. Keep in mind that ANTS transfers folders, not individual files, so you will not see any files that may be present in the folder you select. You are encouraged to select the folder where you typically store and use your records, instead of organizing or relabeling them. This will help us preserve the authenticity of the records. If there are files in the directory that you do not want to transfer, don't worry, you will be able to omit them later.

Once you select the folder containing the records you want to transfer, ANTS will open its main window and list the contents of the directory:

![](http://library.albany.edu/libdru/files/images/mainWindow.png)

The left side will list every file and folder within the directory you selected. The right side will provide text boxes where you can enter information about you records as you see fit. You can add record descriptions and access concerns for any file or folder in the directory. Just select the item you want to describe on the left and enter information in the boxes on the right. It is assumed that descriptions for folders apply to their contents as well.

#####Describing Records

You do not have to describe every record, instead think of any information that may not be gained from reading the file names, what do you know about these records that isn't shown? If you would like to prevent the transfer of some records, just uncheck the boxes to the left of each item. Unchecking folders also unchecks their contents, and re-checking files also checks their parent folders. 

You can also list any access or information security concerns for each record. This could notify archivists if there is personally identifiable information or other restricted data present. Archivists will not rely on this information, but it may help to let them know you are concerned about certain records. There is also a general "Notes for Archivist" text box which applies to the entire transfer. Here, enter any information that you would like to tell the archivist.

#####Transferring Records

This assumes that ANTS was configured during installation with a config.xml file. If you did not set up ANTS with config.xml, and this is your first transfer, follow the instructions below that show how to configure ANTS from within the GUI.

Once you have selected and described your records, click the "Submit" button to transfer your records. Depending on your configuration, you may be prompted for a username and password.

![](http://library.albany.edu/libdru/files/images/progressBar.png)

ANTS will then gather and package metadata for each of the records your selected and transfer them to the archives. If you selected to compress your files (that option may not have been available) or are transferring a large amount of records, the progress bar may slow near the end as the package is transferred. ANTS will inform you that your transfer was successful, and then close.

![](http://library.albany.edu/libdru/files/images/transferSuccess.png)

##Configure ANTS from within the GUI

If you did not set up ANTS with a config.xml file, you can configure ANTS through the GUI. First open ANTS and browse to the folder you want to transfer as described above. When the main window that displays a list of you files opens, navigate to the "Creator Profile" tab to enter information about the creator of the records.

![](http://library.albany.edu/libdru/files/images/creatorConfig.png)

On this tab you may enter information about the creator of the records and your contact information. Contact your archivist to see what information you should enter. None of this metadata is required, but by default ANTS uses the Creator ID and the Donor as part of the package name. Once you are done you may click "Set as Default" to prevent having to enter this information again during the next transfer. This will update ANTS's entire configuration.

Next, navigate to the "Options" tab to enter information about the transfer process.

![](http://library.albany.edu/libdru/files/images/transferConfig_0.png)

Here you must select a transfer method, location, and credentials. If you wish to receive records from the archives using ANTS, then you will also need to enter a Receive Location. If "Network Share" is selected, ANTS will transfer your records over networked storage and rely on external authentication. If you select this method, ANTS requires a local path (say "C:\Users\username\Desktop") or a UNC path to a file server (say "\\Server\Archives\subfolder). This is where ANTS will output your records as an archival package.

If you which to transfer your records over File Transfer Protocol (FTP), then you must enter the destination URL as the Transfer Location (and Receive Location if applicable). An example would be "ftp://www.mycompany.com/archives/subfolder" (the "ftp://" is not necessary). FTP transfers probably require a Login and a Password, so those must be entered as well. Depending on your configuration, the Login and Password fields may not be shown. In this case ANTS will prompt you for your password when you make a transfer. You may use the buttons on the right to test if your connections are valid:

![](http://library.albany.edu/libdru/files/images/testSuccess.png)

ANTS also features some custom options which are displayed in the bottom of the tab. If you are configuring ANTS yourself, ask your archivist what settings you should select. Once you have finished configuring ANTS, click the "Set as Default" button to store the information, so you don't have to enter it again next time.

Also, keep in mind that you can receive files and view or export a receipt from this tab as well. This will be discussed below.

##Viewing Receipt of Transfers and Making Requests

ANTS keeps a running record of all the files you transfer. This is stored locally on you computer and can be viewed through ANTS or exported. The "View Receipt" button is located on the welcome screen, or in the "Options" tab in the main window.

![](http://library.albany.edu/libdru/files/images/splash.png)

By default, clicking "View Receipt" will open up your browser and display a webpage that details each transfer you have made.

![](http://library.albany.edu/libdru/files/images/viewReceipt.png)

Each transfer is listed as an "accession" on the left and as a blue table on the right. Click on the blue table headings to reveal information about each transfer. The table lists each file and folder you transferred with an ID and a "Request" link. This link opens an email message that list the record, the ID, and information about the specific transfer. ANTS can be configured so that this message is sent directly to the archives to request the return of any record.

If you would like to export the receipt, open ANTS, select a folder just to open the main window, and navigate to the "Options" tab. Here you can export the receipt as an HTML file like shown, and XML file, or a CSV file.

![](http://library.albany.edu/libdru/files/images/exportReceipt.png)

##Receiving Records from the Archives

Typically, the archives will notify you outside of ANTS that records you requested can be received through ANTS. When you are ready to receive records, click the "Receive Files" from either the welcome window or the "Options" tab. This assumes that ANTS is configured to receive records, if not follow the configuration instructions above. If there are records available, you will see a window that displays the available files. Check the records you would like to download, and ANTS will ask you where to save the files.

![](http://library.albany.edu/libdru/files/images/receiveFiles.png)


#Configuring ANTS

ANTS configuration data is stored in a simple config.xml file located in a user's AppData directory. An example path would be: 

+ "C:\Users\USERNAME\AppData\Roaming\ANTS-Transfer_System\config.xml"

The ANTS-Transfer_System directory is created either by the installer or by the first time a user runs ANTS.exe. If config.xml is not found by antsFromBoot.exe when it is launched, an empty configuration file is created.

#####Installing ANTS with Configuration Data

ANTS can be configured remotely if an administrator creates the config.xml file manually. If the setup-ANTS-X.X.exe installer or the ANTS.exe program finds a config.xml file in the same directory, it moves that file into the user's AppData directory that is listed above.

###Example config.xml


    <antsConfig>
      <accessionCount>608</accessionCount>
      <creator>Office of the President</creator>
      <creatorId>ua000</creatorId>
      <donor>Jill Sample</donor>
      <role>Records Manager</role>
      <email>jsample@albany.edu</email>
      <office>AH-312</office>
      <address1>1400 Washington Avenue</address1>
      <address2>Albany, NY 12222</address2>
      <address3/>
      <transferMethod>network</transferMethod>
      <transferLocation>C:\Projects\ants\destination</transferLocation>
      <receiveLocation>C:\Projects\ants\destination\request</receiveLocation>
      <login store="true"/>
      <pw store="False"/>
      <timestampTool>os.stat</timestampTool>
      <timeZone>utc</timeZone>
      <error>minimal</error>
      <compress default="true" lock="false">zip</compress>
      <checksum>md5</checksum>
      <receipt>html</receipt>
      <requestEmail>reference@archives.com</requestEmail>
      <requestSubject>This is a reference request from ANTS</requestSubject>
      <requestBody/>
      <smtpHost>smtp.gmail.com</smtpHost>
      <smtpPort/>
      <notificationEmail>DummyNotificationAccount@gmail.com</notificationEmail>
      <notificationEmailPw>encryptedPW</notificationEmailPw>
      <notificationEmailSubject>Successful ANTS Transfer!</notificationEmailSubject>
      <notifyEmail>archivist@archives.com</notifyEmail>
    </antsConfig>


###Configuration Elements

#####```<antsConfig>```
This element is the root of the config.xml file, all of the following elements are contained within this element at a single level. While the order of these elements is ignored by ANTS, it may be important for future updates if new elements are required.

#####```<accessionCount>```

+ Content Required: any integer as a string, cannot be empty.

This contains an integer as a string which represents a running total of attempted transfers. Each time a transfer is attempted, ANTS adds one to this total. It cannot be edited within the GUI.

This number is used to name the ANTS Submission Information Package (SIP). If there is a filename or directory collision because of this, ANTS inserts a 22-character unique string before the SIP name, but does not alter the ```<accessionCount>``` If no metadata is entered, ANTS adds "accession" at the beginning of the SIP name.

#####```<creator>```

+ any string, may be empty

Creator of the records being transferred. This is part of the accession-level metadata that is added to the SIP. User can edit with the GUI.

#####```<creatorId>```

+ any string, may be empty

Identifier for the creator of the records being transferred. This is part of the accession-level metadata that is added to the SIP. User can edit with the GUI. The Creator ID is used in naming the SIP.

#####```<donor>```

+ any string, may be empty

Name of the person or entity transferring the records. This is part of the accession-level metadata that is added to the SIP. User can edit with the GUI. The donor is used in naming the SIP.

#####```<role>```

+ any string, may be empty

Role of the donor. May be a title or position. This is part of the accession-level metadata that is added to the SIP. User can edit with the GUI.

#####```<email>```

+ any string, may be empty

Email address of the donor. This is part of the accession-level metadata that is added to the SIP. User can edit with the GUI. The donor email attached to the SIP could be used by the receiving archivist to automate a confirmation message.

#####```<office>```

+ any string, may be empty

Office of the donor, part of the general contact information This is part of the accession-level metadata that is added to the SIP. User can edit with the GUI.

#####```<address1>```

+ any string, may be empty

First address line, part of the general contact information This is part of the accession-level metadata that is added to the SIP. User can edit with the GUI.

#####```<address2>```

+ any string, may be empty

Second address line, part of the general contact information This is part of the accession-level metadata that is added to the SIP. User can edit with the GUI.

#####```<address3>```

+ any string, may be empty

Third address line, part of the general contact information This is part of the accession-level metadata that is added to the SIP. User can edit with the GUI.

#####```<transferMethod>```

+ Set number of string options (network, ftp, ftptls)

Method that will be used to transfer records to the archives. "network" refers or any filesystem path, local or UNC. Denotes both the transfer and receive transfer methods. User can edit in the GUI with a radio button.

#####```<transferLocation>```

+ any string, must be valid path or URL

Destination where ANTS will attempt to transfer SIP. For "network" transfers, this can be either a local path or a UNC path of a server. For FTP transfers, this is the complete FTP URL, "ftp://" is optional. User can edit in the GUI. Examples:

+ C:\directory\of\destination
+ \\Archives\triage\collection\destination
+ ftp://www.archives.com/triage/collection/transfer

#####```<receiveLocation>```

+ any string, must be valid path or URL

Location of records requested by records creators. For "network" transfers, this can be either a local path or a UNC path of a server. For FTP transfers, this is the complete FTP URL, "ftp://" is optional. User can edit in the GUI. Examples:

+ C:\directory\of\origin
+ \\Archives\triage\collection\requests
+ ftp://www.archives.com/triage/collection/requests

#####```<login store="true">```

+ any string, required for FTP transfers
+ @store has set number of string options ("true", false")

Login credentials for FTP and FTP/TLS transfers. When @store is set to "true" this can be stored without encryption through the GUI. If field is left empty or @store is set to "false" then user will be prompted for credentials.

#####```<pw store="false">```

+ any string, required for FTP transfers
+ @store has set number of string options ("true", false")

Password credentials for FTP and FTP/TLS transfers. When @store is set to "true" this can be stored with encryption through the GUI. If field is left empty or @store is set to "false" then user will be prompted for credentials.

Although this password is encrypted, that does not mean it is secure. We recommend treating this password as insecure.

#####```<timeZone>```

+ Set number of string options (local, posix, utc)

Option to select timestamp format/timezone. Format will be documented in the SIP. "local" will use the local timezone of the records creator. "posix" will use Unix POSIX time, or the number of seconds since 1970-01-01. "utc" will use Coordinated Universal Time (essentially Greenwich Mean Time). User can edit with the GUI.

#####```<timestampTool>```

+ Set number of string options (os.stat, plaso)

Option to the forensic tool used to gather record-events for users without administrative privileges. "os.stat" is much faster and more useful, while "plaso" is included for future experimentation. User can edit with the GUI.

#####```<error>```

+ Set number of string options (minimal, verbose)

Option to select the type of error messages displayed within the GUI. "minimal" is best for typical use, while "verbose" is best for debugging. Verbose output is always printed to the console and stored in an errorLog.txt file in the user's AppData directory. User can edit with the GUI.

#####```<compress default="true" lock="false">```

+ Set number of string options (zip, tar.gz)
+ @default has set number of string options ("true", false")
+ @lock has set number of string options ("true", false")

Option to select compression format User can edit with the GUI. Both use Python's shutil.make_archive function. User can edit in the GUI with a radio button, and for each transfer, with the checkbox next to the "Submit" button. @default sets whether the checkbox is selected by default. When @lock is set to "true" users will not be given the option to compress and all transfers will be compressed. This feature is designed for additional transfer methods which may alter uncompressed files.

#####```<checksum>```

+ Set number of string options (md5, sha256)

Option to select the checksum algorithm used by Bag-it to hash files. User can edit in the GUI with a radio button.

#####```<receipt>```

+ Set number of string options (html, csv, xml)

Option to select the format ANTS will use to both display and export the receipt of all transferred records. "html" produces a Bootstrap HTML document, "csv" produces a flat listing of all the records transferred without accession metadata, "xml" produces all of ANTS receipt information in its native format.

#####```<requestEmail>```

+ any string, may be empty

Populates Email Request link within HTML receipt. Lets users request copies of previously transferred records. Users cannot edit from the GUI.

#####```<requestSubject>```

+ any string, may be empty

Subject of Email Request link within HTML receipt. Lets users request copies of previously transferred records. Request emails will have this subject. Users cannot edit from the GUI.

#####```<requestBody>```

+ any string, may be empty

Body of Email Request link within HTML receipt. Lets users request copies of previously transferred records. Request emails will begin with this body, and also contain the accession-level metadata that is listed above, like collection Id, donor, etc., as well as SIP name and the ID for the requested record. Users cannot edit from the GUI.

#####```<smtpHost>```

+ any string, may be empty

SMTP Host for sending email notifications after successful transfers. Example could be "smtp.google.com." See [Python's smtpLib documentation](https://docs.python.org/2/library/smtplib.html) for more details. Cannot edit from the GUI.

#####```<smtpPort>```

+ port number as string, may be empty

SMTP port number for sending email notifications after successful transfers. If empty, port will be 587. See [Python's smtpLib documentation](https://docs.python.org/2/library/smtplib.html) for more details. Cannot edit from the GUI.

#####```<notificationEmail>```

+ any string, may be empty

Used for sending email notifications after successful transfers. This would be the email address that sends the notification email from ANTS, not the email address being notified. This should be either the record creator's email or an account used solely for automated notifications. Cannot edit from the GUI.


#####```<notificationEmailPw>```

+ any string, may be empty

Password for sending email notifications after successful transfers. This would be the email address that sends the notification email from ANTS, not the email address being notified. This should be either the record creator's email or an account used solely for automated notifications. This string will be encrypted the first time ANTS is run. Cannot edit from the GUI.

Although this password is encrypted, that does not mean it is secure. We recommend treating this account as insecure.

#####```<notificationEmailSubject>```

+ any string, may be empty

Subject of email notification sent after successful transfers. Cannot edit from the GUI.

#####```<notifyEmail>```

+ any string, may be empty

The email address that will be notified when a successful transfer is made. Typically this is the archivist's email address. Cannot edit from the GUI.


#ANTS Submission Information Package (SIP)

ANTS uses the bag-it standard as the basis for its SIP. Here is an example of an accession:

    ua855-Jill_Sample-11/
    |-- data
    |   \-- rootDirectory
    |   	\-- file.docx
    |   	\-- subDirectory
    |   		\-- example1.png
    |   		\-- example2.txt
    |   	\-- otherfiles.pdf
    |   	\-- otherfiles2.xlsx
    \-- bag-info.txt
    | 	Bag-Software-Agent: bagit.py <http://github.com/libraryofcongress/bagit-python>
    | 	Bagging-Date: 2016-01-13
    | 	Payload-Oxum: 2265357.8
    | 	accession: ua855-Jill_Sample-11
    | 	location: ftp://library.albany.edu/archive/ua/triage/ua855/transfer
    | 	method: ftptls
    | 	submitted: 2016-01-13 16:48:03
    \-- bagit.txt
    | 	BagIt-Version: 0.97
    | 	Tag-File-Character-Encoding: UTF-8
    \-- manifest-md5.txt
    | 	c75db4e69ee891cd5ace46144099f6d0  data/rootDirectory/file.docx
    | 	841a79c62a8cadefd6ca172f8c16adf3  data/rootDirectory/subDirectory/example1.png
    | 	b6264929c4ca64d6413387f960a0e408  data/rootDirectory/subDirectory/example2.txt
    | 	a9f6822be03441fabdddd8503de4c5ad  data/rootDirectory/otherfiles.pdf
    | 	79538a466357a18b8641a7a210f34f7b  data/rootDirectory/otherfiles2.xlsx
    \-- ua855-Jill_Sample-11.xml
    |		<accession number="ua855-Jill_Sample-11" submitted="2016-01-13 16:48:03">
    |		  <profile>
    |			<notes></notes>
    |			<creator>Office of the President</creator>
    |			<creatorId>ua855</creatorId>
    |			<donor>Jill Sample</donor>
    |			<role>Records Manager</role>
    |			<email>jsample@albany.edu</email>
    |			<office>AH-312</office>
    |			<address1>1400 Washington Ave.</address1>
    |			<address2>Albany, NY 12222</address2>
    |			<address3></address3>
    |			<method>ftptls</method>
    |			<location>ftp://library.albany.edu/archive/ua/triage/ua855/transfer</location>
    |		  </profile>
    |		  <folder name="rootDirectory">
    |			<id>054c2c9f-a3ad-4de5-a413-705468d417ab</id>
    |			<path>C:\Users\user\Documents\rootDirectory</path>
    |			<description>user-created description for the accession</description>
    |			<access/>
    |			<curatorialEvents version="0.5 (beta)">
    |			  <event timestamp="2016-01-13 16:48:02">ran MFTRCRD to gather NTFS timestamps</event>
    |			  <event timestamp="2016-01-13 16:48:03">ran Bagit-python to package accession</event>
    |			  <event timestamp="2016-01-13 16:48:03">ftp transfer with TLS</event>
    |			</curatorialEvents>
    |			<recordEvents>
    |			  <timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="STANDARD_INFORMATION" label="File_Create_Time">2015-03-25 14:16:21</timestamp>
    |			  <timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="STANDARD_INFORMATION" label="File_Modified_Time">2015-12-28 15:04:40</timestamp>
    |			  <timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="STANDARD_INFORMATION" label="MFT_Entry_modified_Time">2015-12-28 15:04:40</timestamp>
    |			  <timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="STANDARD_INFORMATION" label="File_Last_Access_Time">2015-12-28 15:04:40</timestamp>
    |			  <timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="FILE_NAME" label="File_Create_Time">2015-03-25 14:16:21</timestamp>
    |			  <timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="FILE_NAME" label="File_Modified_Time">2015-03-25 14:16:21</timestamp>
    |			  <timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="FILE_NAME" label="MFT_Entry_modified_Time">2015-03-25 14:16:21</timestamp>
    |			  <timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="FILE_NAME" label="File_Last_Access_Time">2015-03-25 14:16:21</timestamp>
    |			</recordEvents>
    |			<file name="file.docx">
    |			  <id>d973e82b-ca68-447e-93f1-570830190ff6</id>
    |			  <path>C:\Users\user\Documents\rootDirectory\file.docx</path>
    |			  <description/>
    |			  <access>This file may contain student grades</access>
    |			  <curatorialEvents version="0.5 (beta)">
    |				<event timestamp="2016-01-13 16:48:03">ran MFTRCRD to gather NTFS timestamps</event>
    |				<event timestamp="2016-01-13 16:48:03">ran Bagit-python to package accession</event>
    |				<event timestamp="2016-01-13 16:48:03">ftp transfer with TLS</event>
    |			  </curatorialEvents>
    |			  <recordEvents>
    |				<timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="STANDARD_INFORMATION" label="File_Create_Time">2015-04-09 14:22:17</timestamp>
    |				<timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="STANDARD_INFORMATION" label="File_Modified_Time">2015-02-04 20:22:08</timestamp>
    |				<timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="STANDARD_INFORMATION" label="MFT_Entry_modified_Time">2015-04-09 15:25:30</timestamp>
    |				<timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="STANDARD_INFORMATION" label="File_Last_Access_Time">2015-03-25 14:16:21</timestamp>
    |				<timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="FILE_NAME" label="File_Create_Time">2015-03-25 14:16:21</timestamp>
    |				<timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="FILE_NAME" label="File_Modified_Time">2015-03-25 14:16:21</timestamp>
    |				<timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="FILE_NAME" label="MFT_Entry_modified_Time">2015-03-25 14:16:21</timestamp>
    |				<timestamp source="NTFS" timeType="local+4:00" parser="MFTRCRD" type="FILE_NAME" label="File_Last_Access_Time">2015-03-25 14:16:21</timestamp>
    |			  </recordEvents>
    |			</file>
    |			<folder name="subDirectory">
    |				...
    |			</folder>
    |			...
    |			...
    |		  </folder>
    |		</accession>