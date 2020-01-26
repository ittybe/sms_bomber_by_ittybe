# -*- coding: utf-8 -*-
import os.path
from datetime import datetime

import requests
from fake_useragent import UserAgent
from urllib3.exceptions import InsecureRequestWarning

from stem import Signal
from stem.control import Controller

class Service:
    user_agent = UserAgent()
    wait_new_ip = None
    is_ip_available = True

    def __init__(self, phone, country_data, sms_text='Произошёл троллинг'):
        self.phone = phone
        self.country_code = country_data[0]
        self.phone_code = country_data[1]
        self.sms_text = sms_text if sms_text != '' else 'Произошёл троллинг'
        self.formatted_phone = self.phone_code + self.phone
        # ip thing
        self.create_tor_session()
        # self.renew_connection()

        # if os.path.isfile('debug'):
        #     self.session_get = self.session.get
        #     self.session_post = self.session.post
        #     self.session.get = self.get
        #     self.session.post = self.post

        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    def log_request_main(self):
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {type(self).__name__}', end='')

    @staticmethod
    def _log_request(name, message, ip):
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {name}')
        return
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {name}: {message} IP:{ip}')

    def create_tor_session(self):
        self.session = requests.session()
        # Tor uses the 9050 port as the default socks port
        # self.session.proxies = {}
        # self.session.proxies['http'] = 'socks5h://localhost:9050'
        # self.session.proxies['https'] = 'socks5h://localhost:9050'
        self.session.headers = {'User-Agent': self.generate_random_user_agent()}
    # signal TOR for a new connection
    @staticmethod
    def renew_connection(password):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=password)
            controller.signal(Signal.NEWNYM)
            # test delete if not working
            # func check new num in some cases doesnt work
            # so we check vars here
            Service.wait_new_ip = controller.get_newnym_wait()
            Service.is_ip_available = controller.is_newnym_available()

    @staticmethod
    def check_newnym():
        """
        change ip values
        to know time wait and
        is available new ip
        """
        # change class attr for getting wait time and ip available
        with Controller.from_port(port=9051) as controller:
            Service.wait_new_ip = controller.get_newnym_wait()
            Service.is_ip_available = controller.is_newnym_available()

    def get(self, *args, **kwargs):
        self.create_tor_session()
        request = self.session.get(*args, **kwargs)
        logging_text = request.text
        if len(logging_text) > 500:
            if '<!doctype html>' in logging_text.lower():
                logging_text = f'Response too long to display ({len(logging_text)} characters) and is HTML'
            else:
                logging_text = f'Response too long to display ({len(logging_text)} characters) and is not HTML'
        # self._log_request(type(self).__name__,
        #                   logging_text.replace('\n', ''),
        #                   self.session.get("http://httpbin.org/ip").text)
        return request

    def post(self, *args, **kwargs):
        self.create_tor_session()
        request = self.session.post(*args, **kwargs)
        logging_text = request.text
        if len(logging_text) > 500:
            if '<!doctype html>' in logging_text.lower():
                logging_text = f'Response too long to display ({len(logging_text)} characters) and is HTML'
            else:
                logging_text = f'Response too long to display ({len(logging_text)} characters) and is not HTML'
        # self._log_request(type(self).__name__,
        #                   logging_text.replace('\n', ''),
        #                   self.session.get("http://httpbin.org/ip").text)
        return request

    @staticmethod
    def generate_random_user_agent():
        return Service.user_agent.random
