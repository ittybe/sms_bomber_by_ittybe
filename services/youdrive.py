from service import Service


class YouDrive(Service):
    def send_sms(self):
        self.post('http://youdrive.today/signup/phone',
                          data={'phone': self.phone, 'phone_code': self.phone_code})
