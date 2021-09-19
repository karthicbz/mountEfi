#revision 1.0 
#This version only mounts and unmounts efi partition on mac os

import subprocess
import os
import biplist

def createPlist():
    output = subprocess.getoutput('diskutil list -plist')
    details = []
    buildWord = ''
    for out in output:
        if out != '\n':
            buildWord += out
        else:
            if buildWord == '<plist version="1.0">':
                buildWord = ''
                pass
            else:
                details.append(buildWord)
                buildWord = ''

    f = open('diskdetails.plist', 'w')
    for text in details:
        f.write(text)
        
def identifyEfiDisk():
    createPlist()
    os.system('plutil -convert binary1 diskdetails.plist')
    pl = biplist.readPlist('diskdetails.plist')
    #print(pl['AllDisksAndPartitions'][0]['Partitions'][0])
    foundPartition = pl['AllDisksAndPartitions'][0]['Partitions']
    for i in range(len(foundPartition)):
        if 'VolumeName' in foundPartition[i]:
            if(foundPartition[i]['VolumeName']) == 'EFI':
                identifiedDevice = foundPartition[i]['DeviceIdentifier']
                return identifiedDevice

def activity():
    running = True
    while running:
        yourInput = input('1->mount efi\n2->unmount efi\ne->exit\n')
        if yourInput == '1':
            os.system('sudo diskutil mount /dev/{0}'.format(identifyEfiDisk()))
        elif yourInput == '2':
            os.system('sudo diskutil unmount /dev/{0}'.format(identifyEfiDisk()))
        elif yourInput == 'e':
            running = False

activity()


    
    
