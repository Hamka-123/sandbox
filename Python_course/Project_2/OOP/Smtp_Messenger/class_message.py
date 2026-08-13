
import pathlib
import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import utils


class Message:
    
    def __init__(self, config, template_name, attachments = None, cc_emails = None, bcc_emails=None):
        self.SMTP_HOST = config['SMTP_HOST']
        self.SMTP_PORT = config['SMTP_PORT']
        self.SMTP_USER = config['SMTP_USER']
        self.SMTP_PASSWORD = config['SMTP_PASS']
        
        self.template_name = template_name
        self.subject = utils.get_subject_from_template(config, self.template_name)
        # Гарантируем, что attachments всегда будет списком
        self.attachments = attachments if attachments is not None else []
        
        self.to_emails = self.get_emails_list(config)
        self.cc_emails = cc_emails or []
        self.bcc_emails = bcc_emails or []
        self.emails_list = self.to_emails + self.cc_emails + self.bcc_emails
        
        self.msg_html_body = utils.fill_data_to_template(config, self.template_name)
        self.msg_text_body = utils.get_text_message_from_template(self.msg_html_body)
        
        # Добавляем метаданные для отчетов
        self.message_id = f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        self.created_at = datetime.now().isoformat()
        self.status = "created"
        self.sent_at = datetime.now().isoformat()
        self.error = None
    
    def get_analytics_data(self):
        """Возвращает структурированные данные для аналитики и отчетов"""
        # Безопасно получаем данные с проверками
        attachments_count = len(self.attachments) if self.attachments else 0
        
        return {
            "message_id": self.message_id,
            "template_name": self.template_name,
            "subject": self.subject,
            "sender": self.SMTP_USER,
            "recipients": {
                "to": self.to_emails,
                "cc": self.cc_emails,
                "bcc": self.bcc_emails,
                "total_count": len(self.emails_list),
                "unique_count": len(set(self.emails_list))
            },
            "content": {
                "text_length": len(self.msg_text_body) if self.msg_text_body else 0,
                "html_length": len(self.msg_html_body) if self.msg_html_body else 0,
                "has_attachments": attachments_count > 0
            },
            "attachments": {
                "count": attachments_count,
                "files": self.attachments if self.attachments else [],
                "total_size": self._get_attachments_size()
            },
            "timestamps": {
                "created_at": self.created_at,
                "sent_at": self.sent_at
            },
            "delivery": {
                "status": self.status,
                "error": self.error,
                "smtp_server": f"{self.SMTP_HOST}:{self.SMTP_PORT}"
            }
        }
    
    def _get_attachments_size(self):
        """Вычисляет общий размер вложений в байтах"""
        total_size = 0
        if not self.attachments:
            return total_size
            
        for attachment in self.attachments:
            try:
                file_path = pathlib.Path(__file__).parent.joinpath(attachment)
                if file_path.exists():
                    total_size += file_path.stat().st_size
            except (OSError, ValueError):
                continue
        return total_size
        
    def create_message(self):
        message = MIMEMultipart()
        message["Subject"] = self.subject
        message["From"] = self.SMTP_USER
        message["To"] = ", ".join(self.to_emails)
        if self.cc_emails:
            message["Cc"] = ", ".join(self.cc_emails)
       
        #text_part = MIMEText(self.msg_text_body, "plain")
        html_part = MIMEText(self.msg_html_body, "html")
        
        if self.attachments is not None:
            # Add attachment
            for attachment in self.attachments:
                ATTACHMENT_FILE = attachment
                with open(pathlib.Path(__file__).parent.joinpath(ATTACHMENT_FILE), 'rb') as f: 
                    binary_part = MIMEBase("application", "octet-stream")
                    binary_part.set_payload(f.read())
                encoders.encode_base64(binary_part)
                binary_part.add_header(
                    "Content-Disposition",
                    f'attachment; filename= {ATTACHMENT_FILE}'
                )
                message.attach(binary_part) # binary part - attachment

        #message.attach(text_part) # message  part 1 -> text part
        message.attach(html_part) # message part 2 -> HTML part
        
        return message
    
    def get_emails_list(self, config) -> list:
        method = config['EMAIL_SOURCE_NAME']
        match(method):
            case 'API':
                int_config_url = config['INTEGRATION_CONFIG']['URL']
                int_config_method = config['INTEGRATION_CONFIG']['METHOD']
                int_config_timeout = config['INTEGRATION_CONFIG']['TIMEOUT']
                #TODO request and return list of emails
                return ['qababenko@gmail.com']
            case 'CVS':
                file_path = config['INTEGRATION_CONFIG']['URL']
                #TODO read from csv and return list of emails
                return ['qababenko@gmail.com']
            case _:
                print('No such integration')
                
    
    def send(self):
        
        self.message = self.create_message()
        
        with smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT) as server:
            try:
                server.starttls()
                server.login(self.SMTP_USER, self.SMTP_PASSWORD)
                #server.send_message(Message)
                server.sendmail(
                    self.SMTP_USER, 
                    self.emails_list, 
                    self.message.as_string()
                    )
                print("Email sent successfully!")
            except Exception as e:
                print(f"Error sending email: {e}")
                
    def __repr__(self):
        """Представление объекта для разработчика"""
        return (f"Message("
                f"template='{self.template_name}', "
                f"subject='{self.subject}', "
                f"to={len(self.to_emails)} recipients, "
                f"cc={len(self.cc_emails)}, "
                f"bcc={len(self.bcc_emails)}, "
                f"attachments={len(self.attachments) if self.attachments else 0})")
    
    def __str__(self):
        """Строковое представление для пользователя"""
        attachments_info = f", {len(self.attachments)} attachments" if self.attachments else ""
        cc_info = f", CC: {len(self.cc_emails)}" if self.cc_emails else ""
        bcc_info = f", BCC: {len(self.bcc_emails)}" if self.bcc_emails else ""
        
        return (f"📧 Email Message: '{self.subject}'\n"
                f"   • Template: {self.template_name}\n"
                f"   • To: {len(self.to_emails)} recipients\n"
                f"   • Total recipients: {len(self.emails_list)}{cc_info}{bcc_info}\n"
                f"   • Attachments: {len(self.attachments) if self.attachments else 'None'}{attachments_info}")
    
    def display_details(self):
        """Детальная информация о сообщении"""
        print("=" * 50)
        print("📧 EMAIL MESSAGE DETAILS")
        print("=" * 50)
        print(f"Subject: {self.subject}")
        print(f"Template: {self.template_name}")
        print(f"From: {self.SMTP_USER}")
        print(f"To ({len(self.to_emails)}): {', '.join(self.to_emails)}")
        
        if self.cc_emails:
            print(f"Cc ({len(self.cc_emails)}): {', '.join(self.cc_emails)}")
        
        if self.bcc_emails:
            print(f"Bcc ({len(self.bcc_emails)}): {', '.join(self.bcc_emails)}")
        
        if self.attachments:
            print(f"Attachments ({len(self.attachments)}):")
            for i, attachment in enumerate(self.attachments, 1):
                print(f"  {i}. {attachment}")
        else:
            print("Attachments: None")
        
        print(f"Text length: {len(self.msg_text_body)} chars")
        print(f"HTML length: {len(self.msg_html_body)} chars")
        print("=" * 50)
    














