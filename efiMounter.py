#revision 1.1
#Added an option to copy efi folder from USB to HDD
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
    print(pl['AllDisksAndPartitions'][0]['Partitions'][0])
    foundPartition = pl['AllDisksAndPartitions'][0]['Partitions']
    for i in range(len(foundPartition)):
        if 'VolumeName' in foundPartition[i]:
            if(foundPartition[i]['VolumeName']) == 'EFI':
                identifiedDevice = foundPartition[i]['DeviceIdentifier']
                return identifiedDevice
    # return(pl)

def identifyAllDisk():
    createPlist()
    os.system('plutil -convert binary1 diskdetails.plist')
    pl = biplist.readPlist('diskdetails.plist')
    return pl

def getExternalDevices():
    externalDevices = []
    for i in range(len(identifyAllDisk()['AllDisksAndPartitions'])):
        allPartitions = identifyAllDisk()['AllDisksAndPartitions'][i]['Partitions']
        if len(allPartitions) != 0:
            volName = allPartitions[0]['VolumeName']
            if volName != 'EFI':
                # os.system('ls /Volumes/{0}'.format(volName))
                externalDevices.append(volName)
    return externalDevices

    # print(allPartitions)

def copyEfiFiles():
    externalDevices = getExternalDevices()
    if len(externalDevices) <= 0:
        print('No USB / External device found')
    else:
        for i in range(len(externalDevices)):
            print('{0}->{1}'.format(i,externalDevices[i]))

        usbNumber = input('Choose the usb drive: ')
        selectedUsb = externalDevices[int(usbNumber)]
        # os.system('ls /Volumes/{0}'.format(selectedUsb))
        output = subprocess.getoutput('ls /Volumes/{0}'.format(selectedUsb))
        if 'EFI' in output:
            os.system('sudo diskutil mount /dev/{0}'.format(identifyEfiDisk()))
            os.system('cp -R /Volumes/{0}/EFI /Volumes/EFI/'.format(selectedUsb))
            os.system('sudo diskutil unmount /dev/{0}'.format(identifyEfiDisk()))
            print('EFI folder copied to hdd\nNow you can remove the USB and boot from HDD')
        else:
            print('EFI folder does not exists')


def activity():
    running = True
    while running:
        yourInput = input('1->copy efi from usb to hdd\n2->mount efi\n3->unmount efi\ne->exit\n')
        if yourInput == '1':
            # print(getExternalDevices())
            copyEfiFiles()
        elif yourInput == '2':
            os.system('sudo diskutil mount /dev/{0}'.format(identifyEfiDisk()))
        elif yourInput == '3':
            os.system('sudo diskutil unmount /dev/{0}'.format(identifyEfiDisk()))
        elif yourInput == 'e':
            running = False

activity()

    
    
