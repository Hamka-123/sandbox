
from datetime import datetime

class Reporter:
    
    def __init__(self, config, log_path):
        self.config = config
        self.log_path = log_path
    
    def send(self):
        print(f"Send report to admin email: {self.config["ADMIN_EMAIL"]}")
        pass
    
    def display_to_console(self):
        date = datetime.now()
        print(f"Report for date {date}")
        self.generate_email_report(self.log_path)
    
    def generate_email_report(self, log_file_path):
        """Генерирует отчет из логов"""
        import json
        from collections import Counter
        
        sent_emails = []
        failed_emails = []
        
        with open(log_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    log_entry = json.loads(line.strip())
                    if 'analytics' in log_entry:
                        analytics = log_entry['analytics']
                        if log_entry['level'] == 'INFO' and 'sent successfully' in log_entry['message']:
                            sent_emails.append(analytics)
                        elif log_entry['level'] == 'ERROR':
                            failed_emails.append(analytics)
                except:
                    continue
        
        # Статистика
        total_sent = len(sent_emails)
        total_failed = len(failed_emails)
        total_recipients = sum(email['recipients']['total_count'] for email in sent_emails)
        total_emails = total_sent + total_failed
        
            # Безопасный расчет процентов
        if total_emails > 0:
            success_rate = (total_sent / total_emails) * 100
            success_rate_display = f"{success_rate:.1f}%"
        else:
            success_rate_display = "N/A"
        
        # Популярные шаблоны
        templates = Counter(email['template_name'] for email in sent_emails)
        
        print("📊 EMAIL SENDING REPORT")
        print("=" * 40)
        print(f"Total emails sent: {total_sent}")
        print(f"Total emails failed: {total_failed}")
        print(f"Total recipients: {total_recipients}")
        print(f"Success rate: {success_rate_display}")
        print(f"Popular templates: {dict(templates.most_common(3))}")