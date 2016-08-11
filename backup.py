#!/usr/bin/python

import os
import subprocess
import ConfigParser


Config = ConfigParser.ConfigParser()
Config.read("backup.ini")

runningIndicator = ".backuprunning"

def is_mounted(special, directory):
    search_prefix = '{} on {}'.format(special, directory.rstrip('/'))
    if os.path.ismount(directory):
        mounts = subprocess.check_output(['mount']).split('\n')
        for line in mounts:
            if line[:len(search_prefix)] == search_prefix:
                return True;
    return False

def umount(target):
    os.system("umount " + target + " -l")

def mount(src, target, fstype, options):
    os.system("mount -t " + fstype + " -o " + options + " " + src + " " + target)

def make_sure_mounted(section):
    umount(section["target"])
    if not is_mounted(section["src"], section["target"]):
        mount(section["src"], section["target"], section["fstype"], section["options"])
        if not is_mounted(section["src"], section["target"]):
            raise RuntimeError("From is not mounted")

def parse_section(name):
    sec = {}
    
    sec["src"] = Config.get(name, "MountSrc")
    sec["target"] = Config.get(name, "MountTarget")
    sec["options"] = Config.get(name, "Options")
    sec["fstype"] = Config.get(name, "fstype")

    return sec

def backup(From, To):
    os.system("rsync -a -v --delete " + From["target"] + " " + To["target"])

def check_running():
    return os.path.isfile(runningIndicator)

def mark_running(mark):
    if mark:
        print("mark running: true")
        f = open(runningIndicator,"w+")
        f.close()
    else:
        print("mark running: false")
        os.remove(runningIndicator)

def main():

    if check_running():
        print("process already running. exiting. ")
        return

    mark_running(True)
    try:
        From = parse_section("From")
        To = parse_section("To")

        make_sure_mounted(From)
        make_sure_mounted(To)

        backup(From, To)
    except:
        mark_running(False)
        raise

    mark_running(False)

main()
