from service import Service


class FindClone(Service):
    def send_call(self):
        self.get('https://findclone.ru/register', params={'phone': '+' + self.formatted_phone})
