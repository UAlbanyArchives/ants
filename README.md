# ANTS: Archives Network Transfer System

Developed for records creators to described files, package them, and transfer them to an archives.

Will make use of basic digital forensics tools to gather filesystem metadata and create a robust SIP in records' native environment before transfer.

Executable should run by itself with no dependencies

Developed for Windows and NTFS filesystems

Currently only a working demo with GUI that transfers files over local or network path.

Any feedback or suggested features are welcome, gwiedeman[at]albany.edu

Uses Joakim Schicht's MftRcrd tool and Plaso engine developed by Kristinn Gudjonsson and Joachim Metz - will credit further later

# to do:
_______

* Write FTP module
* make timestamps consistant and allow for local timezones
* comment code
* make unpacker to PREMIS