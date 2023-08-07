from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..method.debug import *
import email, smtplib, ssl ,os
def sendmail_attachment(subject_mail, body_mail , receiver_mail,port_mail,host_mail,sender_mail):
    try:
        port_mail = port_mail
        host_mail = host_mail
        subject = subject_mail
        sender_email = sender_mail
        receiver = receiver_mail
        # password = input("Type your password and press enter:")
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = ", ".join(receiver)
        message["Subject"] = subject
        # message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        html_header = """
                        <!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>
                    """
        html_body = body_mail.decode('utf-8')
        html_footer = """
                        </body></html>
                    """
        body = html_header + html_body + html_footer
        message.attach(MIMEText(body, "html","utf-8"))

        text = message.as_string()

        context = ssl.create_default_context()
        s = smtplib.SMTP(host=host_mail,port=port_mail)
        s.sendmail(sender_email, receiver, text)
        s.quit()


        result = {
            "status": "OK",
            "message": "Send Mail Success."
        }
    except Exception as e:
        result = {
            "status": "ER",
            "errorCode": "SM999",  # SM => Send Mail
            "errorMessage": str(debug_row(e))
        }
    return result

def generate_body_template(TotalInvoice,SuccessInvoice,FailedInvoice,recoverInvoice,RecoverResponseInvoices,responseInvoice):
    try:
        body = """
                <div style="margin-left:30px;">
                    <h3>Summary</h3>
                    Total Invoice: """ + str(TotalInvoice) + """<br>
                    Success Invoice : """+str(SuccessInvoice)+""" <br>
                    Failed Invoice : """+str(FailedInvoice)+""" <br>
                    Auto Recover: """+ str(recoverInvoice) +""" 
                </div><br>
                <style>
                    table{
                        border-collapse: collapse;
                    }
                    table, th, td {
                        border: 1px solid black;
                    }
                    td {
                        text-align:center;
                    }
                </style>
                <table style="width:100%;border: 1px solid black;">
                    <h3 style="text-align:center;">Failed Invoice response</h3>
                    <tr style="border: 1px solid black;">
                        <th>Invoice Name</th>
                        <th>Process DTM</th>
                        <th>Error Code</th>
                        <th>Error Message</th>
                    </tr>
                    """
        if responseInvoice != '':
            for i in responseInvoice:
                body += """
                        <tr>
                            <td>"""+str(i["InvoiceName"])+"""</td>
                            <td>"""+str(i["Process DTM"])+"""</td>
                            <td>"""+str(i["errorCode"])+"""</td>
                            <td>"""+str(i["errorMessage"])+"""</td>
                        </tr>
                    """
        else:
            print('No responseInvoices invoice to send mail.')
        if RecoverResponseInvoices != []:
            body += """
                        <style>
                                table{
                                    border-collapse: collapse;
                                }
                                table, th, td {
                                    border: 1px solid black;
                                }
                                td {
                                    text-align:center;
                                }
                            </style>
                            <table style="width:100%;border: 1px solid black;">
                                <h3 style="text-align:center;">รายการที่รอกู้คืนอัตโนมัติ</h3>
                                <tr style="border: 1px solid black;">
                                    <th>Document Name</th>
                                    <th>Error Code</th>
                                    <th>Error Message</th>
                                </tr>
                        """
            for recover_message in RecoverResponseInvoices:
                body += """
                        <tr>
                            <td>""" + str(recover_message["invoiceNo"]) + """</td>
                            <td>""" + str(recover_message["errorCode"]) + """</td>
                            <td>""" + str(recover_message["errorMessage"]) + """</td>
                        </tr>
                    """
        body += """</table><br>"""
        body += """ <hr style="width:100%;border:2px solid black;"/> """
        result = {"status":"OK","result":body.encode('utf-8')}
    except Exception as e:
        result = {"status":"ER","errorMessage":str(debug_row(e)) , "errorCode":"ER999"}
    finally:
        return result

def generate_body_recover(totalInvoice,successInvoice,failedInvoice,successResponseInvoices,failedResponseInvoices):
    try:
        body = """
               <div style="margin-left:30px;">
                   <h3>Summary</h3>
                   Total Invoice : """ + str(totalInvoice) + """ <br>
                   Success Invoice : """ + str(successInvoice) + """<br>
                   Fail Invoice : """ + str(failedInvoice) + """ <br>
               </div><br>
               """
        if successResponseInvoices != []:
            body += """
                        <style>
                                table{
                                    border-collapse: collapse;
                                }
                                table, th, td {
                                    border: 1px solid black;
                                }
                                td {
                                    text-align:center;
                                }
                            </style>
                            <table style="width:100%;border: 1px solid black;">
                                <h3 style="text-align:center;">รายการที่สำเร็จ</h3>
                                <tr style="border: 1px solid black;">
                                    <th>Date of Input</th>
                                    <th>Batch Name</th>
                                    <th>Document Name</th>
                                    <th>Message</th>
                                </tr>
                        """
            for sign_success in successResponseInvoices:
                body += """
                        <tr>
                            <td>""" + str(sign_success["inputDate"]) + """</td>
                            <td>""" + str(sign_success["batchName"]) + """</td>
                            <td>""" + str(sign_success["invoiceNo"]) + """</td>
                            <td>""" + str(sign_success["message"]) + """</td>
                        </tr>
                    """
        if failedResponseInvoices != []:
            body += """
                        <style>
                                table{
                                    border-collapse: collapse;
                                }
                                table, th, td {
                                    border: 1px solid black;
                                }
                                td {
                                    text-align:center;
                                }
                            </style>
                            <table style="width:100%;border: 1px solid black;">
                                <h3 style="text-align:center;">รายการที่ไม่สำเร็จ</h3>
                                <tr style="border: 1px solid black;">
                                    <th>Date of Input</th>
                                    <th>Batch Name</th>
                                    <th>Document Name</th>
                                    <th>Error Code</th>
                                    <th>Error Message</th>
                                </tr>
                        """
            for sign_error in failedResponseInvoices:
                body += """
                        <tr>
                            <td>""" + str(sign_error["inputDate"]) + """</td>
                            <td>""" + str(sign_error["batchName"]) + """</td>
                            <td>""" + str(sign_error["invoiceNo"]) + """</td>
                            <td>""" + str(sign_error["errorCode"]) + """</td>
                            <td>""" + str(sign_error["errorMessage"]) + """</td>
                        </tr>
                    """
        body += """</table><br>"""
        result = {"status": "OK", "result": body.encode('utf-8')}
    except Exception as e:
        result = {"status":"ER","errorMessage":"generate_body_recover : " + str(e) , "errorCode":"ER999"}
    finally:
        return result