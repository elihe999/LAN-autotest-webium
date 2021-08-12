# -*- coding: utf-8 -*-
import json
import sys
import socket
import requests
import tftpServer

from collections import deque
import time
from scapy.all import *
from threading import Thread


# core dump check 
# point out where to save it.
# python check and download file 
# python send http / https request
def search_lan_mac(ip):
    conf.route.resync()
    conf.route.route('0.0.0.0')[0]
    # show_interfaces()
    get_working_if()
    addr = ip.split('.')
    lan = addr[0] + "." + addr[1] + "." + addr[2] + ".1/24"
    ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=lan), timeout=3, verbose=False)
    for snd, rcv in ans:
        cur_mac = rcv.sprintf("%Ether.src%")
        cur_ip  = rcv.sprintf("%ARP.psrc%")
        if cur_ip == ip:
            return cur_mac
    return False

def search_ip(ip,mac):
    conf.route.resync()
    conf.route.route('0.0.0.0')[0]
    # show_interfaces()
    get_working_if()
    addr = ip.split('.')
    lan = addr[0] + "." + addr[1] + "." + addr[2] + ".1/24"
    ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=lan), timeout=3, verbose=False)
    for snd, rcv in ans:
        cur_mac = rcv.sprintf("%Ether.src%")
        cur_ip  = rcv.sprintf("%ARP.psrc%")
        if cur_mac == mac:
            if  ip.strip() != cur_ip.strip():
                ip = cur_ip.strip()
                return cur_ip
    return ip

def sendHttpReuqest(url,http):
    try:
        pos = url.find("passcode=")
        print(url[:pos] + "passcode=*****")
    except:
        print(url)
    
    if http:
        res = requests.get("http://" + url, verify = False)
        print(res)
        return res
    else:
        res = requests.get("https://" + url, verify = False)
        print(res)
        return res

class apiTester():
    def __init__(self):
        self.ip = ""
        self.userName = ""
        self.password = ""
        self.interval = 100
        self.loop = 1
        self.testType = "reboot"
        self.version1 = ""
        self.version1 = ""
        self.version1 = ""

        self.dir1 = ""
        self.dir2 = ""
        self.dir3 = ""
        
        self.serverType = 1 # 1 means http

        self.mac = ""
        self.messageList = deque()

        self.errorCount = 0
        self.http = True
        self.foundCoreStop = False
        self.coreDumpPath = ".\\"
        self.testStatus = [False,0,0,"ip","mac"]

        self.enableAI = False
    
    def setEnableAI(self, enable):
        self.enableAI = enable

    def setCNN(self,cnnP):
        self.cnn = cnnP
    
    def setServerType(self,serverType):
        if serverType == "tftp":
            self.serverType = 0
        elif serverType == "http":
            self.serverType = 1
        elif serverType == "https":
            self.serverType = 2
        elif serverType == "ftp":
            self.serverType = 3
        elif serverType == "ftps":
            self.serverType = 4
    
    def setVersion(self,v1,v2,v3,d1,d2,d3):
        self.version1 = v1
        self.version2 = v2
        self.version3 = v3
        self.dir1 = d1
        self.dir2 = d2
        self.dir3 = d3

    def setTestStatus(self,status,messageList,path):
        self.testStatus = status
        self.messageList = messageList
        self.coreDumpPath = path

    def setFoundCoreStop(self,stop):
        self.foundCoreStop = stop

    def setValue(self,ip,user,password,interval,loop,testType):
        self.ip = ip
        self.userName = user
        self.password = password
        self.interval = interval
        self.loop = loop
        self.testType = testType

        #
        t = Thread(target=tftpServer.lauchServer,args=())
        t.start()

    def initPhone(self):
        url = self.ip
        url += "/cgi-bin/api-request_init_phone_status?passcode="
        url += self.password

        try:
            res = sendHttpReuqest(url,self.http)
        except:
            if self.loop == 0:
                self.http = not self.http
            try:
                self.checkAndWait(5)
                res = sendHttpReuqest(url,self.http)
            except:
                self.outputMessage("destination unreachable !")
                self.errorCount += 1
                if self.loop == 0:
                    self.testStatus[0] = False
                return False

        if res.status_code == 200:
            self.outputMessage("init phone success")
            return True
        elif res.status_code == 401:
            self.outputMessage("话机 未鉴权，请检查IP地址和密码",1)
            self.testStatus[0] = False
            return False
        elif res.status_code == 500:
            self.outputMessage("device return code：500",1)
            return False
        else:
            return False
    
    def rebootPhone(self):
        url = self.ip
        url += "/cgi-bin/api-sys_operation?passcode="
        url += self.password + "&request=REBOOT"
        try:
            sendHttpReuqest(url,self.http)
            self.outputMessage("send Reboot API ")
        except:
            self.errorCount += 1
            self.outputMessage("reboot Api connect failed",1)
            self.checkAndWait(10)
    
    def resetPhone(self):
        url = self.ip
        url += "/cgi-bin/api-sys_operation?passcode="
        url += self.password + "&request=RESET"
        try:
            sendHttpReuqest(url,self.http)
        except:
            self.errorCount += 1
            self.outputMessage("reset Api connect failed",1)
            self.checkAndWait(10)
    
    def provisionPhone(self):
        url = self.ip
        url += "/cgi-bin/api-sys_operation?request=PROV&passcode="
        url += self.password
        try:
            sendHttpReuqest(url,self.http)
        except:
            # it may already in provision status, after config setting change
            # self.outputMessage("provision Api connect failed",1)
            self.checkAndWait(4)

    def coreDumpCheckAndDownload(self):
        url = self.ip
        url += "/cgi-bin/api-download_coredump?passcode=" + self.password
        try:
            res = sendHttpReuqest(url,self.http) # set stream = True
        except:
            self.outputMessage("core dump check Api connect failed",1)
            self.checkAndWait(10)
            return False
        if res.status_code == 404:
            return False
        
        name = str(res.headers)
        pos = name.find("filename")
        pos = name.find('"',pos)
        end = name.find('"',pos+1)
        name = name[pos+1:end]

        #download file 
        with open(self.coreDumpPath + "\\" + name, 'wb') as f:
            for data in res.iter_content(1024):
                f.write(data)
        f.close()

        self.outputMessage("found core dump",1)
        self.outputMessage(name)

        return True


    def getPvalue(self,pvalue):
        url = self.ip
        url += "/cgi-bin/api.values.get?request=" + pvalue
        url += "&passcode=" + self.password
        res  = ""
        try:
            res = sendHttpReuqest(url,self.http)
        except:
            self.checkAndWait(5)
            try:
                res = sendHttpReuqest(url,self.http)
            except:
                self.outputMessage("get pvalue failed",1)
                return "ERROR"

        if res.status_code != 200:
            self.outputMessage("Response: " + str(res.status_code) , 1)
            return "ERROR"
        
        try:
            # value = json.load(res.text).get("body").get(pvalue)
            pos =  res.text.index("\"" + pvalue + "\"" )
            pos = res.text.index(":",pos+1)
            pos = res.text.index("\"",pos+1)
            end = res.text.index("\"",pos+1)
            value = res.text[pos+1:end]
            return value
        except:
            self.outputMessage("get pvalue response format error",1)
            self.outputMessage(res.text,0)
            return "ERROR"
        

    def outputMessage(self,msg,status = 0):
        if status == 1:
            msg = "<span style=\"color:red\">" + msg + "</span>"
        elif status == 2:
            msg = "<span style=\"color:blue\">" + msg + "</span>"
        else:
            msg = "<span style=\"color:black\">" + msg + "</span>"
        
        timeStr = "<span style=\"color:black\">" + time.strftime("[%m-%d %H:%M:%S] ",time.localtime())

        msg = timeStr + "</span>" + msg
        self.messageList.append(msg)
        # print (msg)

    def prepareCfgFile(self,serverType,objectDir):
        cfgFile = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
        cfgFile += "<gs_provision version=\"1\">\n"
        cfgFile += "<config version=\"1\">\n"
        cfgFile += "<P238>0</P238>\n"
        cfgFile += "<P6767>" + str(serverType) + "</P6767>\n"
        cfgFile += "<P8375>0</P8375>\n"
        cfgFile += "<P232></P232>\n"
        cfgFile += "<P233></P233>\n"
        cfgFile += "<P6768></P6768>\n"
        cfgFile += "<P6769></P6769>\n"
        cfgFile += "<P192>" + objectDir + "</P192>\n"
        cfgFile += "</config>\n"
        cfgFile += "</gs_provision>\n"
        return cfgFile


    def checkAndWait(self,count):
        self.outputMessage("wait:" + str(count))
        for i in range(count):
            time.sleep(1)
            if count > 4:
                self.testStatus[2] = count - i
            if self.testStatus[0] == False:
                self.testStatus[2] = 0
                break
        self.testStatus[2] = 0

    def activelyWait(self,count,wishLabel):
        self.outputMessage("max wait:" + str(count))

        ensureCount = 0
        for i in range(count):
            time.sleep(1)
            self.testStatus[2] = count - i

            res, label, acc  =  self.cnn.predict()
            if self.testStatus[2] > 5:
                if res == False or acc <0.6:
                    continue
                if label == wishLabel and acc >0.6:
                    ensureCount += 1
                    if ensureCount >= 2:
                        self.outputMessage("status change: " + label, 2)
                        self.checkAndWait(4)
                        self.testStatus[2] = 0
                        return True
                else:
                    ensureCount = 0

            if self.testStatus[0] == False:
                self.testStatus[2] = 0
                break

        self.testStatus[2] = 0
        return False

    def updateConfig(self):
        host = ""
        try:
            # host = socket.gethostbyname(socket.getfqdn(socket.gethostname()[0]))
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            host = s.getsockname()[0]
            s.close()
        except:
            self.outputMessage("Get local host ip failed")
            self.errorCount += 1
            return False

        url = self.ip
        url +=  "/cgi-bin/api-provision?server=tftp://" 
        url +=   host + ":6699"
        url +=  "&passcode=" + self.password
        
        try:
            sendHttpReuqest(url,self.http)
            return True
        except:
            self.checkAndWait(5)
            try:
                sendHttpReuqest(url,self.http)
                return True
            except:
                self.outputMessage("Set config Api connect failed")
                self.errorCount += 1
                return False
    

    def executeTestFlow(self):
        var = search_lan_mac(self.ip)
        if var != False:
            self.mac = var
        
        self.testStatus[0] = True
        self.testStatus[4] = self.mac

        self.errorCount = 0
        successCount = 0
        
        for i in range(self.loop):

            ip = search_ip(self.ip,self.mac)
            if ip != self.ip:
                self.outputMessage("update new ip: " + ip,0)
                self.ip = ip

            if self.testStatus[0] == False:
                break

            self.testStatus[1] = i
            self.testStatus[3] = self.ip


            if self.errorCount>5:
                self.testStatus[0] = False
                self.outputMessage("连续失败5-6次，终止测试",2)
                break

            self.outputMessage("-------loop: " + str(i) +" success:" + str(successCount) + "---------",2)

            initResult = self.initPhone()
            if initResult != True:
                if self.errorCount>5 or self.testStatus[0] == False:
                    break
                else:
                    continue

            contain = self.coreDumpCheckAndDownload()
            if contain and self.foundCoreStop: # and foundToStops
                self.outputMessage("found core dump stop Test, if you want to continue, please change advance option")
                break
            
            self.outputMessage("check core Dump finished")
            
            if self.testStatus[0] == False:
                break

            if self.testType == "Reboot":
                self.rebootPhone()

                # use camera help to check devic status--
                if self.enableAI:
                    res =  self.activelyWait(20,"boot")
                    if res == False:
                        self.outputMessage("send reboot api, but device no response (20s)",1)
                        self.errorCount += 1
                        self.outputMessage("start next loop after wait 25s",0)
                        self.checkAndWait(25) 
                        continue

                    if self.testStatus[0] == False:
                        break

                    res = self.activelyWait(self.interval,"idle")
                    if res == False:
                        self.outputMessage("device reboot timeout, not back to idle status",1)
                        self.errorCount += 1
                        continue
                    else:
                        self.outputMessage("reboot susccess")
                        #after reboot finished, need wait api setup
                        self.outputMessage("wait for api setup",0)
                        self.checkAndWait(25)
                else:
                    self.checkAndWait(self.interval)
                    self.outputMessage("reboot susccess")
                successCount += 1
                self.errorCount = 0
                
            elif self.testType == "Reset": # after reset, api remote control set to disable ?
                self.resetPhone()
                self.password = "admin"
                self.checkAndWait(self.interval)
            elif self.testType == "Provision":
                self.outputMessage(" get device version")
                currentVersion = self.getPvalue("68")
                if currentVersion == "ERROR":
                    self.errorCount += 1
                    continue
                
                self.outputMessage("current version:" + currentVersion)

                objVersion = self.version1
                objDir = self.dir1

                if self.version3 != "":
                    if self.version1 == currentVersion:
                        objVersion = self.version2
                        objDir = self.dir2
                    elif self.version2 == currentVersion:
                        objVersion = self.version3
                        objDir = self.dir3
                    elif self.version3 == currentVersion:
                        objVersion = self.version1
                        objDir = self.dir1
                else:
                    if objVersion == currentVersion:
                        objVersion = self.version2
                        objDir = self.dir2
                self.outputMessage("start provision...",0)
                self.outputMessage(currentVersion + " -> " + objVersion,0)
                
                cfgFile = self.prepareCfgFile(self.serverType,objDir)

                prefix = self.getPvalue("P234")
                postfix = self.getPvalue("P235")

                if prefix == "ERROR" or postfix == "ERROR":
                    self.errorCount += 1
                    continue

                # need test it 
                macStr = self.mac.replace(":","")
                macStr = macStr.lower()
                fileName = "configXml\\" +  prefix + "cfg" + macStr + ".xml" + postfix
                f = open(fileName, "w")
                f.write(cfgFile)
                f.close()

                self.outputMessage("upload config file")
                uploadResult = self.updateConfig()
                if uploadResult == False:
                    self.checkAndWait(10)
                    continue
                
                # need check angain ? see value change is success. if config failed
                # could reduce waiting time

                # if pvalue set right, this  api not neccesy
                self.provisionPhone()
                
                if self.enableAI:
                    res =  self.activelyWait(20,"boot")
                    if res == False:
                        self.outputMessage("send provision api, but device no response",1)
                        self.outputMessage("retry after wait 25s")
                        self.checkAndWait(25)
                        self.errorCount += 1
                        continue
                    
                    res = self.activelyWait(self.interval,"idle")
                    if res == False:
                        self.outputMessage("device provision timeout, device not back to idle",1)
                        self.errorCount += 1
                        continue
                    self.outputMessage("device back to idle, wait for api setup")
                    self.checkAndWait(25)
                else:
                    self.checkAndWait(self.interval)
                

                if self.testStatus[0] == False:
                    break

                #update Ip than check version is right!
                ip = search_ip(self.ip,self.mac)
                if ip != self.ip:
                    self.outputMessage("update new ip :" + ip,0)
                    self.ip = ip
                
                self.testStatus[3] = self.ip
                self.initPhone()
                
                newVersion = self.getPvalue("68")
                if newVersion != objVersion:
                    self.outputMessage("provision failed, version is not: [" + objVersion + "]",1)
                    self.outputMessage("current version : [" + newVersion + "]",2)
                    self.outputMessage("previous version: [" + currentVersion + "]",0)
                    # target error one time
                    self.errorCount += 1
                    self.outputMessage("check failed reason...")
                    if newVersion == "ERROR":
                        self.outputMessage("interval time maybe too short, or connect device failed")
                    else:
                        checkDir = self.getPvalue("P192")
                        if checkDir != objDir and checkDir != "ERROR":
                            self.outputMessage("config file uploaded failed",1)
                else:
                    self.outputMessage("provsion success")
                    self.errorCount = 0
                    successCount += 1
                
                #also need update other info.
        self.outputMessage("Test finished",2)
        self.outputMessage("Success Time:" +  str(successCount))
        self.testStatus[0] = False
            


if __name__ == "__main__":

    cnnP = CNN()
    cnnP.loadModel()
    t = Thread(target=cnnP.openCamera,args=())
    t.start()

    api = apiTester()
    api.setCNN(cnnP)

    ip = "192.168.92.11"
    passwd = "123"
    username = "admin"
    ptime = 400
    loop = 5

    v1 = "0.2.13.45"
    v2 = "1.0.11.6"
    v3 = ""
    d1 = "192.168.92.45:8080/0.2.13.45_fw/"
    d2 = "192.168.92.45:8080/1_0_11_6_fw/"
    d3 = ""
    api.setVersion(v1,v2,v3,d1,d2,d3)
    path = ""

    testStatus = [False,0,0,"ip","mac"]
    messageList = deque()
    api.setValue(ip,username,passwd,ptime,loop,"Reboot")
    api.setTestStatus(testStatus,messageList,path)
    api.setFoundCoreStop(False)
    api.setEnableAI(True)
    api.executeTestFlow()
