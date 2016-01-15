# ANTS: Archives Network Transfer System

for executables to run without dependencies, see  [http://library.albany.edu/archive/universityarchives/ants](http://library.albany.edu/archive/universityarchives/ants)

Developed for records creators to describe, package, and transfer unstructured files to a university archives.
  
GUI desktop application, runs on any Windows XP SP2+ and later without any dependencies.
  
Makes use of basic digital forensics tools to gather filesystem metadata and create a robust SIP in records' native environment before transfer.
  
Gathers MFT $STANDARDINFORMATION and $FILENAME MAC timestamps of each file.
  
Designed to send reference requests and receive files from within the GUI.
  
Transfers over network shares with existing LDAP authentication, FTP, or Microsoft OneDrive (still under development).
  
Can be configured remotely prior to user installation.
  
Maintains local receipt for all transferred materials with identification for easy future requests.
  
Developed for Windows and NTFS filesystems.
  
Can gather local, UTC, or POSIX timestamps.

Any feedback or suggested features are welcome, gwiedeman[at]albany.edu

Uses Joakim Schicht's MftRcrd tool and Plaso engine developed by Kristinn Gudjonsson and Joachim Metz.

Documentation to come
