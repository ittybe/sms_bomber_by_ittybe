from service import Service


class Citilink(Service):
    def send_sms(self):
        self.post('https://www.citilink.ru/registration/confirm/phone/+' + self.formatted_phone + '/')
