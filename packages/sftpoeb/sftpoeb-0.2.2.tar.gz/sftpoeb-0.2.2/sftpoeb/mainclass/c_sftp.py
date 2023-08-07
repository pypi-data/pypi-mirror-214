from ..subclass.path.s_c_setgetlocal import *
from ..subclass.path.s_c_setgetdestination import *
from ..subclass.path.s_c_setgetrecovery import *
from ..subclass.file.s_c_file import *
from ..subclass.process.s_c_process_package_1 import *
from ..subclass.process.s_c_process_package_2 import *
from ..subclass.alert.s_c_alert import *
from datetime import date, datetime
from ..subclass.input.s_c_input import *
from ..method.mail import *
class SFTP():
    def __init__(self,myPath="None",sftpPath="None",custPath="None",payloadData="None",userSftp="None",groupSftp ="None"):
        self.myPath = myPath
        self.sftpPath = sftpPath
        self.custPath = custPath
        self.userSftp = userSftp
        self.groupSftp = groupSftp
        self.dateNow = datetime.now().strftime("%Y%m%d")
        self.timeNow = datetime.now().strftime("%H%M%S")
        self.payloadData = payloadData
        ### Local
        self.local = setgetlocal(self.myPath,self.sftpPath,self.dateNow,self.timeNow)
        ### Destination
        self.destination = setgetdestination(self.custPath,self.sftpPath,self.dateNow,self.timeNow)
        ### Recovery
        self.recovery = setgetrecovery(self.myPath,self.sftpPath,self.dateNow,self.timeNow)
        ### inputFile
        self.input = inputFile(self.local,self.destination,self.dateNow,self.timeNow)
        ### alert
        subject_mail = "< TH-ROBOTICS (UAT)> E-tax Process Notify. Date : " + str(self.dateNow) + " Time : " + str(self.timeNow)
        self.alert = alert(subject_mail)

    def package1(self,quantityThread): 

        ### เปิดคลาสกระบวนการดำเนินการไฟล์
        ### ทำการสร้างโฟลเดอร์ Local เตรียมไว้ pathเดิมให้ใช้ set ... ก่อน ค่อย get
        self.local.getLocalPath()
        self.local.getLocalHistory()
        self.local.getLocalOutputPdfPath()
        self.local.getLocalOutputXmlPath()
        self.local.getLocalLogPath()
        self.local.getLocalPathNow()

        ### ทำการสร้างโฟลเดอร์ Destination เตรียมไว้ ถ้าต้องการแก้ไข pathเดิมให้ใช้ set ... ก่อน ค่อย get
        self.destination.getDestinationPath()
        self.destination.getDestinationInbound()
        self.destination.getDestinationHistory()
        self.destination.getDestinationOutputPdfPath()
        self.destination.getDestinationOutputXmlPath()
        self.destination.getDestinationLogPath()

        ### ทำการสร้างโฟลเดอร์ Recovery เตรียมไว้ pathเดิมให้ใช้ set ... ก่อน ค่อย get
        self.recovery.getRecoveryPath()
        self.recovery.getRecoverySavePath()
        self.recovery.getRecoverySignPath()
        self.recovery.getRecoveryCheckPath()

        ### ทำการเริ่มกระบวนการทำงาน เขียน log และ Chown Folder
        c_process = packageprocess1(self.local,self.destination,self.recovery,self.payloadData,self.dateNow,self.timeNow,self.userSftp,self.groupSftp)
        c_process.runThreadProcess(quantityThread)
        c_process.writelog()
        c_process.finalProcess()
        
        ### Alert Mail
        self.alert.afterjobfinsh(c_process.countInvoice , c_process.success , c_process.fail , c_process.recover_count , c_process.recover , c_process.losemessage)

    def package2(self,quantityThread): 

        ### เปิดคลาสกระบวนการดำเนินการไฟล์
        ### ทำการสร้างโฟลเดอร์ Local เตรียมไว้ pathเดิมให้ใช้ set ... ก่อน ค่อย get
        self.local.getLocalPath()
        self.local.getLocalHistory()
        self.local.getLocalOutputPdfPath()
        self.local.getLocalOutputXmlPath()
        self.local.getLocalCsvArchivePath()
        self.local.getLocalPdfArchivePath()
        self.local.getLocalLogPath()
        self.local.getLocalPathNow()

        ### ทำการสร้างโฟลเดอร์ Destination เตรียมไว้ ถ้าต้องการแก้ไข pathเดิมให้ใช้ set ... ก่อน ค่อย get
        self.destination.getDestinationPath()
        self.destination.getDestinationInbound()
        self.destination.getDestinationPathCSV()
        self.destination.getDestinationPathPDF()
        self.destination.getDestinationHistory()
        self.destination.getDestinationCsvArchivePath()
        self.destination.getDestinationPdfArchivePath()
        self.destination.getDestinationOutputPdfPath()
        self.destination.getDestinationOutputXmlPath()
        self.destination.getDestinationLogPath()

        ### ทำการสร้างโฟลเดอร์ Recovery เตรียมไว้ pathเดิมให้ใช้ set ... ก่อน ค่อย get
        self.recovery.getRecoveryPath()
        self.recovery.getRecoverySavePath()
        self.recovery.getRecoverySignPath()
        self.recovery.getRecoveryCheckPath()

        ### ทำการเริ่มกระบวนการทำงาน เขียน log และ Chown Folder
        c_process = packageprocess2(self.local,self.destination,self.recovery,self.payloadData,self.dateNow,self.timeNow,self.userSftp,self.groupSftp)
        c_process.runThreadProcess(quantityThread)
        c_process.writelog()
        c_process.finalProcess()
        
        ### Alert Mail
        self.alert.afterjobfinsh(c_process.countInvoice , c_process.success , c_process.fail , c_process.recover_count , c_process.recover , c_process.losemessage)
