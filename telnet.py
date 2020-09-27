import getpass
import telnetlib
import re
import csv
import paho.mqtt.publish as publish
import psutil
import time
import uuid
hotsname = "172.16.20.12"
port = 1883
ap = "1"


def telnet():
    HOST = "192.168.1.40"
    user = "root"
    password = "admin"

    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"login: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    tn.write(b"ls\n")
    tn.write(b"wiviz\n")
    tn.write(b"exit\n")
    setdata = tn.read_all().decode('ascii')
    f = open("wiviz.txt", "w")
    f.write(setdata)
    f.close()

    print(setdata)


def cuttext():
    f = open("wiviz.txt", "r")
    string_with_empty_lines = f.read()

    lines = string_with_empty_lines.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    string_without_empty_lines = ""
    for line in non_empty_lines:
        string_without_empty_lines += line + "\n"

    print(string_without_empty_lines)

    f = open("wiviz.txt", "w")
    f.write(string_without_empty_lines)
    f.close()

def survey(m1):
    file = open('wiviz.txt', 'r')
    names = []
    mac = []
    rssi = []
    types = []
    for i,line in enumerate(file):
        names.append(line.strip())
        #----mac----
        result_mac = 'h.mac' in names[i]
        cut_mac1 = names[i].replace(';', '')
        cut_mac2 = cut_mac1.replace('h.mac = ', '')
        if result_mac == True:
            test = m1 in cut_mac2
            if test == True:
                print(cut_mac2)
                publish.single(topic="fx80a",payload=str(cut_mac2)+","+str(ap),qos=1,hostname=hotsname,port=port)
            mac.append(cut_mac2)
        #----rssi----
        result_rssi = 'h.rssi' in names[i]
        cut_rssi1 = names[i].replace(';', '')
        cut_rssi2 = cut_rssi1.replace('h.rssi = ', '')
        if result_rssi == True and test == True:
            print(cut_rssi2)
            rssi.append(int(cut_rssi2))
        #----type----
        result_types = 'h.type' in names[i]
        cut_types1 = names[i].replace(';', '')
        cut_types2 = cut_types1.replace('h.type = ', '')
        if result_types == True:
            types.append(cut_types2)
    #print(names)



telnet()
cuttext()
survey('E0:DD:C0:F8:2B:C7')
