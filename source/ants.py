import admin
import os
import subprocess

try:
	admin.runAsAdmin(["c:\\Projects\\ants\\antsFromBoot.exe"])
	
	#subprocess.call(['C:\\Projects\\fsTools\\MftRcrd\\MFTRCRD.exe', 'C:\\Projects\\test2.py', '-d', 'indxdump=off', '1024', '-s'])
	#subprocess.call(['python', 'ants.py'])
	print "admin"

except:
	subprocess.call(["c:\\Projects\\ants\\antsFromBoot.exe"])
	print "not admin"