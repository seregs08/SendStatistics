import os
import time

import paramiko
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from edit_excel import add_value
from mail import send_mail

load_dotenv()

def connect_and_count(
    ip_enm: str,
    username: str,
    password: str,
    ip_mss: list[str],
    port_enm: int, #='порт по умолчанию',
    beeline_chk: bool = None,
    megafon_chk: bool = None,
    tele2_chk: bool = None
) -> int:
    '''
    Подключение к СЭ и получение статистики по нужным операторам
    '''
    result_dict = {}
    if tele2_chk:
        result_dict['tele2'] = {'count': 0, 'plmn': '00'} #'plmn оператора'}
    if megafon_chk:
        result_dict['megafon'] = {'count': 0, 'plmn': '00'} #'plmn оператора'}
    if beeline_chk:
        result_dict['beeline'] = {'count': 0, 'plmn': '00'} #'plmn оператора'}
    if not result_dict:
        print('Не указан ни один оператор для подсчета.')
        return
    
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    cl.connect(hostname=ip_enm, port=port_enm, username=username,
               password=password, look_for_keys=False, allow_agent=False)
    
    with cl.invoke_shell() as ssh:
        for ip in ip_mss:
            ssh.send(f'ssh {username}@{ip}\n')
            time.sleep(1)
            ssh.send(f'{password}\n')
            time.sleep(1)

            for k, v in result_dict.items():
                #Ряд ssh комманд к СЭ для получения статистики, проверка и подсчет в counter
                result_dict[k]['count'] += counter
    return result_dict

if __name__ == '__main__':
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    ip_enm = os.getenv("IP_ENM")
    ip_mss = os.getenv("IP_MSS").split('/')

    filename = r'C:\Путь до excel\Отчет.xlsx'
    
    def start():
        count_dict = connect_and_count(ip_enm=ip_enm, ip_mss=ip_mss,
                                       username=username, password=password,
                                       beeline_chk=True,
                                       megafon_chk=True,
                                       tele2_chk=True
                                       )
        if count_dict:
            beeline = int(count_dict['beeline']['count'])
            megafon = int(count_dict['megafon']['count'])
            tele2 = int(count_dict['tele2']['count'])
            add_value(beeline, megafon, tele2, filename)

    scheduler = BackgroundScheduler()
    scheduler.add_job(start, 'cron', hour='*') #Подсчет и запись статистики
    scheduler.add_job(send_mail, 'cron', day='*', hour=9, kwargs={'mail_from': '_from',
                                                                   'mail_to': '_to',
                                                                    'mail_subject': '_subject'}) #Отправка статистики

    scheduler.start()
    exit = input('Enter, чтобы выйти')