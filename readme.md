# Backup Tool for Raspberry Pi

## Overview

This tool can be used to backup one windows machine to another using a raspberry pi. It mounts windows shares from both computers and uses rsync to create a backup. 

I am using this tool to backup photos from my workstation in the local network to another pc which is also available locally. 

The tool is straight forward. 

1. It tries to mount both machines. If that fails the script exists. 
2. It then uses rsync to create a backup of the source machines

## Configuration  

Edit [backup.ini](backup.ini) for configuration:

```ini
[From]
MountSrc: //192.168.0.194/Fotos ; what to mount
MountTarget: /media/workstation ; where to mount, please make sure the directory exists!
fstype: cifs ; fstype passed to mount command
options: username=xxx,password=xxx ; options passed to mount command

[To]
MountSrc: //192.168.0.172/PhotoBackup ; what to mount
MountTarget: /media/backupmachine ; where to mount, please make sure the directory exists!
fstype: cifs ; fstype passed to mount command
options: username=xxx,password=xxx ; options passed to mount command
```

## Running

To run the script:
```
$ sudo ./backup.py
```

Run the script automated as a cronjob (use your favourite editor):
```
$ sudo nano /etc/crontab 
```
```
0 * * * * root  cd /wherever/you/cloned/this && ./backup.py
```