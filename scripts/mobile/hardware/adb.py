#!/usr/bin/python

import subprocess
import re
import shutil
import sys
import threading
import json
import os
import zipfile
from time import sleep

adb_path = "/Users/olli/Documents/work/android/android-sdk-macosx/platform-tools/adb"
devices = []	# we found with usb devices actually connected




def get_properties(device=None):
    def get_prop(property):
        if device:
            proc = subprocess.Popen([adb_path,
                                     "-s", device,
                                     "shell", "getprop", property],
                                    stdout=subprocess.PIPE)
        else:
            proc = subprocess.Popen([adb_path,
                                     "shell", "getprop", property],
                                    stdout=subprocess.PIPE)
        output = str(proc.communicate()[0]).strip()
        return output

    manufacturer = get_prop("ro.product.manufacturer")
    model = get_prop("ro.product.model")
    selinux = get_prop("ro.build.selinux.enforce")
    release_v = get_prop("ro.build.version.release")
#    print manufacturer, model, selinux, release_v
    return { "manufacturer": manufacturer, "model": model, "selinux": selinux, "release":release_v }

#    for line in output.split('\\n'):
#        if 'Device ID' in line:
#            eq = line.find("=")
#            dev_id = line[eq+2:-2]
#            print dev_id
#    return dev_id
	
def install(apk, device=None):
    """ Install melted application on phone
    @param package full path
    @return True/False
    """
    #if os.path.exists(apk) == False:
    #	return False
    if device:
        proc = subprocess.call([adb_path,
                            "-s", device,
                            "install", apk])
                            #,
                            #stdout=subprocess.PIPE)
    else:
        proc = subprocess.call([adb_path,
                                "install", apk])
    if proc != 0:
        return False
    return True

def execute(apk, device=None):
    """ Execute melted apk on phone
    @param apk class name to run (eg. com.roxy.angrybirds)
    @return True/False
    shell am  startservice -n $CLASS_PACK/
    """
    app = apk + '/com.android.networking.ServiceMain'
    if device:
        proc = subprocess.call([adb_path,
                                "-s", device,
                                "shell", "am", "startservice",
                                "-n", app], stdout=subprocess.PIPE)
    else:
        proc = subprocess.call([adb_path,
                                "shell", "am", "startservice",
                                "-n", app], stdout=subprocess.PIPE)
    if proc != 0:
        return False
    return True

def uninstall(apk, device=None):
    """ Execute melted apk on phone
    @param apk class name to run (eg. com.roxy.angrybirds)
    @return True/False
    """
    if device:
        proc = subprocess.call([adb_path,
                            "-s", device,
                            "uninstall", apk], stdout=subprocess.PIPE)
    else:
        proc = subprocess.call([adb_path,
                                "uninstall", apk], stdout=subprocess.PIPE)

    if proc != 0:
        return False
    return True


"""
	def run(self):
		#apk = 'kr.aboy.tools.zip'
		
		# Change configuration
		#print "Updating package %s with new configuration"  % self.apk
		#if not self.sync_conf():
		#	print "problem updating configuration fo %s." % self.apk
		#	sys.exit(1)
		
		# Unzip apk
		output_zip = os.path.join(conf.build_dir, self.apk)
		output_apk = self.unzip(output_zip)
		
		# Test with adb
		# 1. install
		print "Installing %s on %s" % (output_apk, self.device)
		installed = self.install(output_apk)
		if not installed:
			print "%s not installed on %s" % (output_apk,self.device)
			sys.exit(1)
		
		# 2. run on phone
		print "Executing %s on %s" % (output_apk, self.device)
		executed = self.execute(self.apk[:-4])
		if not executed:
			print "%s not executed on %d" % (output_apk,self.device)
			sys.exit(1)
		
		# 3. check (sleep/wait stuff)
		sleep(10)
		
		# 4. assertions
		print "Checking for instances on %s" % self.device

		# 5. Uninstall phase
		print "This is the end, Uninstalling on %s" % self.device
		uninstalled = self.uninstall(self.apk[:-4])
		if not uninstalled:
			print "Uninstall with your Handz..."
			sys.exit(1)

"""