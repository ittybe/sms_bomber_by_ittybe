from service import Service


class McDonalds(Service):
    def send_sms(self):
        self.post('https://mcdonalds.ru/api/auth/code', json={'phone': '+' + self.formatted_phone})
