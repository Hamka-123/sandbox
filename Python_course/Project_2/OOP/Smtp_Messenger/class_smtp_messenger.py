import pathlib
import env_config
import utils
from class_reporter import Reporter
from class_logger_service import LoggerService
from class_message import Message

class SmtpMessenger:
    
    def __init__(self):
        self.config:dict = env_config.config
        self.log_path = pathlib.Path(__file__).parent.joinpath("email_manager.log")
        self.logger: LoggerService = LoggerService(self.log_path)
        self.reporter: Reporter = Reporter(self.config, self.log_path)   
        
    '''
    def send_message(self, action = 'One message', mode = ['cc','bcc', 'attachments'], template = 'first_template'):
        """Отправляет одно или несколько сообщений с выбором шаблона
        -
        action: One message, Many messages
        mode: list[cc, bc, attachments]
        template = str name
        """
        action = utils.get_action_from_user()
        mode = utils.get_mode_from_user()
        # ===== modes =====
        cc_emails = None
        bcc_emails = None
        attachments = None
        
        for m in mode:
            match m:
                case 'cc':
                    print("== Getting emails for CC ==") 
                    cc_emails = utils.get_email_list_from_user()
                case 'bcc':
                    print("== Getting emails for BCC ==") 
                    bcc_emails = utils.get_email_list_from_user()
                case 'attachments':
                    print("== Getting attachments url ==") 
                    attachments = utils.get_attachments_urls_from_user()
            
        # ===== actions =======
        match action:
            case 'One message': #send one message to one or more receivers
                template = utils.get_template_from_user(self.config)
                message = Message(self.config, template, attachments, cc_emails, bcc_emails)
                message.send()
                print(message)
            case 'Many messages': #send many messages to one or more receivers
                count_of_emails = int(input("How much emails you want send?: ")) #how much emails need?
                i = 1
                while i <= count_of_emails:
                    template = utils.get_template_from_user(self.config)
                    message = Message(self.config, template, attachments, cc_emails, bcc_emails)
                    message.send()
                    print(message.display_details())
                    i += 1
    '''
    def send_message(self):
        """Отправляет одно или несколько сообщений с индивидуальными настройками для каждого"""
        action = utils.get_action_from_user()
        
        match action:
            case 'One message': 
                # Отправка одного письма с индивидуальными настройками
                self._send_single_message()
                
                
            case 'Many messages': 
                # Отправка нескольких писем с индивидуальными настройками для каждого
                self._send_multiple_messages()
    
    def _send_single_message(self):
        """Отправляет одно письмо с индивидуальными настройками"""
        print("\n" + "="*50)
        print("📧 НАСТРОЙКИ ОДНОГО ПИСЬМА")
        print("="*50)
        
        # Запрашиваем настройки для этого письма
        mode = utils.get_mode_from_user()
        template = utils.get_template_from_user(self.config)
        email_options = self._get_email_options_for_message(mode)
        
        # Создаем и отправляем письмо
        message = Message(self.config, template, **email_options)
        error_occurred = None
    
        try:
            message.send()
            print(message)
            print("✅ Письмо отправлено!")
            
            # Логируем успешную отправку с аналитическими данными
            self.logger.info("Email sent successfully", message.get_analytics_data())
            
        except Exception as e:
            error_occurred = e
            # Логируем ошибку с аналитическими данными
            self.logger.error(f"Failed to send email: {str(e)}", message.get_analytics_data())
        
        # Выводим сообщение об ошибке после блока except
        if error_occurred:
            print(f"❌ Ошибка отправки: {error_occurred}")
        
    def _send_multiple_messages(self):
        """Отправляет несколько писем с индивидуальными настройками для каждого"""
        count_of_emails = int(input("\nСколько писем хотите отправить?: "))
        
        for i in range(count_of_emails):
            print(f"\n" + "="*50)
            print(f"📧 ПИСЬМО {i+1} ИЗ {count_of_emails}")
            print("="*50)
            
            # Для каждого письма запрашиваем индивидуальные настройки
            mode = utils.get_mode_from_user()
            template = utils.get_template_from_user(self.config)
            email_options = self._get_email_options_for_message(mode)
            
            # Создаем и отправляем письмо
            message = Message(self.config, template, **email_options)
            message.send()
            print(message)
            print(f"✅ Письмо {i+1} отправлено!")
            
            # Спросить, хотим ли продолжить (опционально)
            if i < count_of_emails - 1:
                continue_sending = input("\nПродолжить отправку? (y/n): ").strip().lower()
                if continue_sending not in ['y', 'yes', 'д', 'да']:
                    print("⏹️ Отправка прервана пользователем")
                    break
    
    def _get_email_options_for_message(self, mode):
        """Получает настройки email для конкретного письма"""
        cc_emails = None
        bcc_emails = None
        attachments = None
        
        for m in mode:
            match m:
                case 'cc':
                    print("\n== Получатели CC для этого письма ==") 
                    cc_emails = utils.get_email_list_from_user()
                case 'bcc':
                    print("\n== Получатели BCC для этого письма ==") 
                    bcc_emails = utils.get_email_list_from_user()
                case 'attachments':
                    print("\n== Вложения для этого письма ==") 
                    attachments = utils.get_attachments_urls_from_user()
        
        return {
            'attachments': attachments,
            'cc_emails': cc_emails,
            'bcc_emails': bcc_emails
        }
    def send_report(self):
        self.reporter.send()
        
    def display_report(self):
        self.reporter.display_to_console()
        
    def test(self):
        s = utils.get_subject_from_template(self.config, 'Deployment_notification')
        print(s)
