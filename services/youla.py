from service import Service


class Youla(Service):
    def send_sms(self):
        self.post('https://youla.ru/web-api/auth/request_code', data={'phone': self.formatted_phone})
