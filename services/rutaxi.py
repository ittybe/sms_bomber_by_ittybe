from service import Service


class RuTaxi(Service):
    def send_sms(self):
        self.post('https://moscow.rutaxi.ru/ajax_keycode.html',
                          data={'1': self.formatted_phone})
