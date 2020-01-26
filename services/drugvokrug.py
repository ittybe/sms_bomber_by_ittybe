from service import Service


class DrugVokrug(Service):
    def send_sms(self):
        self.post('https://drugvokrug.ru/siteActions/processSms.htm', data={'cell': self.formatted_phone})
