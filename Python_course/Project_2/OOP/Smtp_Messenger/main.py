from class_smtp_messenger import SmtpMessenger

messenger = SmtpMessenger()

print(messenger.config)
#print(messenger.config["SMTP_APP"])
#messenger.test()

print("🚀 SMTP MESSENGER")
messenger.send_message()


messenger.display_report()
#print(messenger.logger.filename)
messenger.send_report()
