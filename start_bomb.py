# -*- coding: utf-8 -*-
import time
import inspect
import os
import sys
import threading

# import config as cfg


services = os.listdir('services')
service_classes = {}
sys.path.insert(0, 'services')

for service in services:
    if service.endswith('.py') and service != 'service.py':
        module = __import__(service[:-3])
        for member in inspect.getmembers(module, inspect.isclass):
            if member[1].__module__ == module.__name__:
                service_classes[module] = member[0]

def run_service(service_class, module_, phone, country_code, phone_code, sms_text, type_):
    try:
        instance = getattr(module_, service_class)(phone, [country_code, phone_code], sms_text)
        if type_ == 'call':
            instance.send_call()
        else:
            instance.send_sms()
    except Exception:
        instance.log_request_main()
        print("\t\tfailed!")
    else:
        instance.log_request_main()
        print("\t\tsuccessed!")
    # sys.exit()

def start(phone, count, country_code, phone_code, sms_text, send_calls_bool, tor_password, delay):
    # phone = request.form['phone']
    # count = request.form['count']
    # country_code = request.form['country']
    # phone_code = country_codes[country_code]
    # send_calls = request.form['call']
    # sms_text = request.form['smsText']
    # send_calls_bool = True if send_calls == 'true' else False

    # module and name of class
    instance_service = getattr(list(service_classes.items())[0][0],
                               list(service_classes.items())[0][1])
    for _ in range(int(count)):
        if instance_service.is_ip_available:
            for module_, service_class in service_classes.items():
                try:
                    _ = getattr(module_, service_class).send_call
                    if send_calls_bool:
                        # run_service(service_class, module_, phone, country_code, phone_code, sms_text, 'call')
                        threading.Thread(target=run_service,
                                         args=(service_class, module_, phone, country_code, phone_code, sms_text,
                                               'call')).start()
                except AttributeError:
                    # run_service(service_class, module_, phone, country_code, phone_code, sms_text, 'sms')

                    threading.Thread(target=run_service,
                                     args=(service_class, module_, phone, country_code, phone_code, sms_text,
                                           'sms')).start()
                except Exception as X:
                    print(X)
                time.sleep(delay)
            # one func do all work and check and reconnect
            instance_service.renew_connection(tor_password)
        else:
            # sleeping after one iteration
            wait = instance_service.wait_new_ip
            print(f"newnym is {instance_service.is_ip_available}")
            print(f"wait {wait} to get new ip")
            time.sleep(wait)
            # check but not reconnect 'cause
            # main "if ip" will not allowed
            # reconnect also change vars
            instance_service.check_newnym()
            # after sleeping we renew connection and get new ip
            # instance_service.renew_connection(cfg.tor_password)

    return '(ﾉ◕ヮ◕)ﾉ*:・ﾟ✧'
