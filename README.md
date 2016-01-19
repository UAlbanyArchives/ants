# ANTS: Archives Network Transfer System

for executables to run without dependencies, see [http://library.albany.edu/archive/universityarchives/ants](http://library.albany.edu/archive/universityarchives/ants)

##Features

* Developed for records creators to describe, package, and transfer unstructured files to a university archives.
* GUI desktop application, runs on any Windows XP SP2+ and later without any dependencies.
* Makes use of basic digital forensics tools to gather filesystem metadata and create a robust SIP in records' native environment before transfer.
* Gathers MFT $STANDARDINFORMATION and $FILENAME MAC timestamps of each file.
* Designed to send reference requests and receive files from within the GUI.
* Transfers over network shares with existing LDAP authentication, FTP, or Microsoft OneDrive (still under development).
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

Select the directory that contains your records. Keep in mind that ANTS transfers folders, not individual files, so you will not see any files that may be present in the folder you select. You are encouraged to select the folder where you typically store and use your records, instead of organizing or relabeling them. This will help use preserve the authenticity of the records. If there are files in the directory that you do not want to transfer, don't worry, you will be able to omit them later.

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

![](http://library.albany.edu/libdru/files/images/transferConfig.png)

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
