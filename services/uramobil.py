from service import Service


class UraMobil(Service):
    def send_sms(self):
        self.post('https://service.uramobil.ru/profile/smstoken', data={'PhoneNumber': self.formatted_phone})
