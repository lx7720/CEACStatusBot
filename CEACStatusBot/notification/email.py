from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from .handle import NotificationHandle

class EmailNotificationHandle(NotificationHandle):
    def __init__(self,fromEmail:str,toEmail:str,emailPassword:str,hostAddress:str='') -> None:
        super().__init__()
        self.__fromEmail = fromEmail
        self.__toEmail = toEmail.split("|")
        self.__emailPassword = emailPassword
        self.__hostAddress = hostAddress or "smtp."+fromEmail.split("@")[1]
        if ':' in self.__hostAddress:
            [addr, port] = self.__hostAddress.split(':')
            self.__hostAddress = addr
            self.__hostPort = int(port)
        else:
            self.__hostPort = 0

    def send(self,result):
        
        mail_title = '[CEACStatusBot] {} : {}'.format(result["application_num_origin"],result['status'])
        
        # Create a more readable HTML layout
        mail_content_html = f"""
        <html>
        <head>
        <style>
            body {{ font-family: sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
        </style>
        </head>
        <body>
        <h2>CEAC Visa Status Notification</h2>
        <table>
            <tr>
                <th>Application Number</th>
                <td>{result.get('application_num_origin', 'N/A')}</td>
            </tr>
            <tr>
                <th>Status</th>
                <td><strong>{result.get('status', 'N/A')}</strong></td>
            </tr>
            <tr>
                <th>Visa Type</th>
                <td>{result.get('visa_type', 'N/A')}</td>
            </tr>
            <tr>
                <th>Case Created</th>
                <td>{result.get('case_created', 'N/A')}</td>
            </tr>
            <tr>
                <th>Case Last Updated</th>
                <td>{result.get('case_last_updated', 'N/A')}</td>
            </tr>
            <tr>
                <th>Description</th>
                <td>{result.get('description', 'N/A')}</td>
            </tr>
        </table>
        </body>
        </html>
        """

        msg = MIMEMultipart()
        msg["Subject"] = Header(mail_title,'utf-8')
        msg["From"] = self.__fromEmail
        msg['To'] = ";".join(self.__toEmail)
        msg.attach(MIMEText(mail_content_html,'html','utf-8'))

        smtp = SMTP_SSL(self.__hostAddress, self.__hostPort) # ssl登录
        print(smtp.login(self.__fromEmail,self.__emailPassword))
        print(smtp.sendmail(self.__fromEmail,self.__toEmail,msg.as_string()))
        smtp.quit()
