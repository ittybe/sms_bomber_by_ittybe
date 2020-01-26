import start_bomb
import click
import config as cfg
country_codes = {'ru': '7', 'ua': '380', 'kz': '7', 'by': '375'}

@click.command()
@click.option('-ph','--phone', default=cfg.phone,
              help='phonenumber')
@click.option('-cnt','--count', default=cfg.count,
              help='number of iterations')
@click.option('-cd','--code', default=cfg.country,
              help='phone code of your country. You can enter ru : 7, ua : 380, kz : 7, by : 375')
@click.option('--sms', default=cfg.smsText,
              help='sms text(not working)')
@click.option('-cl','--send_call', default=cfg.send_calls,
              help='send calls? 0 - no, 1 - yes', type=bool)
@click.option('-pass', '--tor_password', default=cfg.tor_password,
              help=f'tor password, default = {cfg.tor_password}')
@click.option('-dl', '--delay', default=cfg.delay,
              help='delay between every service')
def main(phone, count, code, sms, send_call, tor_password, delay):
    # print(phone, count, code, sms, send_call)
    start_bomb.start(phone=phone, count=count,
                     country_code=code,
                     phone_code=country_codes[code],
                     sms_text=sms,
                     send_calls_bool=send_call,
                     tor_password=tor_password,
                     delay=delay)

if __name__ == "__main__":
    main()
