from ...method.mail import * 
from ...method.debug import *
from datetime import datetime
class alert():
    def __init__(self,mail_subject="None",mail_host="onerelay.one.th",mail_port="25"):
        self.mail_subject = mail_subject
        self.mail_receiver = []
        self.mail_sender ="Support-etax@inet.co.th"
        self.mail_host = mail_host
        self.mail_port = mail_port
    
    def setSubjetcMail(self,subject):
        self.mail_subject = subject
        return self.mail_subject
    
    def setReceiverMail(self,receiver):
        self.mail_receiver = receiver
        return self.mail_receiver

    def afterjobfinsh(self,TotalInvoice,SuccessInvoice,FailedInvoice,RecoverInvoice,RecoverResponseInvoices,ResponseInvoice):
        if self.mail_subject == "None":
            self.mail_subject = "< TH-ROBOTICS (UAT)> E-tax Process Notify. Date : " + str(datetime.now().strftime("%Y%m%d")) + " Time : " + str(datetime.now().strftime("%H%M%S"))
        
        ResponseSendMail = ""
        if FailedInvoice > 0 :
            mail_body = generate_body_template(TotalInvoice,SuccessInvoice,FailedInvoice,RecoverInvoice,RecoverResponseInvoices,ResponseInvoice)
            ResponseSendMail = sendmail_attachment(self.mail_subject,mail_body["result"],self.mail_receiver,self.mail_port,self.mail_host,self.mail_sender)
        else:
            ResponseSendMail = {"status":"OK","message":"Pass. Not found invoice fail"}

        print("MailAlert : " , ResponseSendMail)