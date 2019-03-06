import netifaces
import smtplib
import time

class ipnotify:
    def __init__(self, address, password, subject, recipients):
        # IP
        self.ip = self.getIP()
        self.lastCheck = time.time()
        # Email
        self.address = address
        self.password = password
        self.subject = subject
        self.recipients = recipients
        # Send Initial IP
        self.send(self.subject, self.ip)
    def getIP(self):
        try:
            ipinfo = netifaces.ifaddresses("wlan0")[netifaces.AF_INET]
            return ipinfo[0]["addr"]
        except:
            return "ERROR"
    def send(self, subject, message):
        try:
            server = smtplib.SMTP("smtp.gmail.com:587")
            server.starttls()
            server.login(self.address, self.password)
            message = "Subject: {}\n\n{}".format(subject, message)
            server.sendmail(self.address, self.recipients, message)
            server.quit()
        except:
            pass
    def update(self):
        now = time.time()
        if self.lastCheck < now-5:
            ip = self.getIP()
            if self.ip != ip:
                self.ip = ip
                self.send(self.subject, self.ip)
            self.lastCheck = now

