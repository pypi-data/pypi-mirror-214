import sftpoeb.mainclass.c_sftp as c_sftp
myPath = 'D:/Work/sFTP-AUTO/class_sftp/home/natthawut.th/bubblelytest/bubblelytest/'
custPath = 'D:/Work/sFTP-AUTO/class_sftp/home/sftp/bubblelytest/bubblelytest'
payloadData = {
    "SellerTaxid":"0105562115475",
    "SellerBranchId":"00000",
    "UserCode":"bubblelytest",
    "AccessKey":"P@ssw0rd",
    "APIKey":"AK2-3UY8R84Q6LIZ5A18IDZH6JI3O63IZLJLJH01CS1OUHRTWR5VG4AED7UCTA5HKE92JJLN1R1DZT74WCDN9PI4L4JM7B62ULRNQTHJ4EO85IYUELWWVG5R7EX8AHQNQY8YNW21Y8Q5EE46P0GQUEOFY700LLOCIBOLRXG0ZVY3J9IUWQOTYBB9TJ85DKSIU8E93MIF8NQ89HRYGGNI4U7K69DZQ9H0EGG0YC2Z09O90J77COR0HCQK9W9SALBWE3E6I",
    "Authorization":"Mjc6R29DY1JvRlA5RGc5QUhlNWh6aU15MUxvRHFwM1RJNXpTVTVrVUVTRTpleUowWVhocFpDSTZJakF4TURVMU5qRXdOekkwTWpBaUxDSndZWE56ZDI5eVpDSTZJbTR4TWpNME5UWTNPQ0o5SVFNV2djQ08zZDdaTnkyUnE0WXpYcHlxa3U0ckdxOFk=",
    "ServiceCode":"S06",
    "receiver_mail":["natthawut.th@inet.co.th"]
}
sftpPath = ''
usersftp = "bubblelytest"
groupsftp = "sftp"

### เรียกคลาส SFTP
sftp = c_sftp.SFTP(myPath,sftpPath,custPath,payloadData,usersftp,groupsftp)
sftp.alert.setReceiverMail(payloadData["receiver_mail"])
sftp.alert.setSubjetcMail("alert sftp <uat>")
sftp.package2(quantityThread=1)