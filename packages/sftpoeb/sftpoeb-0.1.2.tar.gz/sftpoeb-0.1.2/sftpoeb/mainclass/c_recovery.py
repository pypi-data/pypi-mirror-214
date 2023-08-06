from ..subclass.path.s_c_setgetlocal import *
from ..subclass.path.s_c_setgetdestination import *
from ..subclass.path.s_c_setgetrecovery import *
from ..subclass.file.s_c_file import *
from ..subclass.process.s_c_process_package_1 import *
from ..subclass import *
from datetime import date, datetime
from ..subclass.input.s_c_input import *
from ..method.mail import *
from ..method.debug import *

class RECOVERY():
    def __init__(self,myPath="None",sftpPath="None",custPath="None",payloadData="None",userSftp="None",groupSftp ="None"):
        self.myPath = myPath
        self.sftpPath = sftpPath
        self.custPath = custPath
        self.userSftp = userSftp
        self.groupSftp = groupSftp
        self.dateNow = datetime.now().strftime("%Y%m%d")
        self.timeNow = datetime.now().strftime("%H%M%S")
        self.process_now = str(self.dateNow + self.timeNow)
        self.payloadData = payloadData
        ### Local
        self.local = setgetlocal(self.myPath,self.sftpPath,self.dateNow,self.timeNow)
        ### Destination
        self.destination = setgetdestination(self.custPath,self.sftpPath,self.dateNow,self.timeNow)
        ### Recovery
        self.recovery = setgetrecovery(self.myPath,self.sftpPath,self.dateNow,self.timeNow)
        ### alert
        self.alert = alert()

    def formation1(self):
        try:

            print(str(self.dateNow + self.timeNow) + '>> API Recovery : Process Recovery done.')
            result = {"status": "OK", "message": "Process Recovery done."}
        except Exception as e:
            print(str(self.dateNow + self.timeNow) + '>> API Recovery error : ' + str(debug_row(e)))
            result = {"status": "ER","errorCode":"PR999", "errorMessage": 'API Recovery error : '+str(debug_row(e))}