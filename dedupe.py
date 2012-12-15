import os
import pickle
import shutil

# LICENSE: WTFPL http://sam.zoy.org/wtfpl/

# DESCRIPTION
# dedupe.py lets you dedupe files (usually images) that are exactly identical.
# I wrote this script to dedupe my Whatsapp images (since i send the same pictures
# to many people in whatsapp, it duplicates the images). Running this script can
# delete the duplicates!

#### configure the following parameters ####

# path to adb command in the android sdk
adb = "/Users/vigneshv/Downloads/android-sdk-macosx/platform-tools/adb"
# temporary directory to store pulled files
tmpdir = "/tmp/whatsapp_pics"
# path to image files on the phone
imgdir = "/sdcard/Whatsapp/Media/Whatsapp\ Images"
# command  used for checksumming
checksumcmd = "shasum5.12"

#### end of configuration parameters ####

# create temp directory
os.makedirs(tmpdir)

# get files list
files = [a.strip() for a in os.popen("%(adb)s shell ls %(imgdir)s" % locals()).read().strip().split("\n")]

# pull all files and compute checksum
print "Pulling files!"
checksums = {}
for file in files:
    print "Pulling file %(file)s" % locals()
    os.system("%(adb)s pull %(imgdir)s/%(file)s %(tmpdir)s/%(file)s" % locals())
    checksum = os.popen("%(checksumcmd)s %(tmpdir)s/%(file)s" % locals()).read().strip().split(' ')[0]
    if checksums.has_key(checksum):
        checksums[checksum].append(file)
    else:
        checksums[checksum] = [file]

# remove duplicate files having same checksum leaving only one copy
for files in checksums:
    for file in checksums[files][1:]:
        print "removing %(file)s" % locals()
        os.system("%(adb)s shell rm %(imgdir)s/%(file)s" % locals())

# remove temp directory
shutil.rmtree(tmpdir)
print "done!"