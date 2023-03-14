import pyad.adquery # імпорт Python AD Tools
import pyad.aduser # ADuser
from ad_settings import ad_username, ad_password, ad_server # імпорт ad_settings
from alphabet import ukr_alphabet   # імпорт кирилиці
from passgen import password    # імпорт генератора випадкових паролів

# параметри підключення до AD
AD_USERNAME: str = ad_username
AD_PASSWORD: str = ad_password
AD_SERVER: str = ad_server
pyad.set_defaults(ldap_server=ad_server, username=ad_username, password=ad_password)
user = pyad.aduser.ADUser.from_cn("")


# функция Transliteration, яка транслітерує заданий аргумент (ім’я) кирилицею з латиницi
def transliterate_ukr(name: str) -> str:
    try:
        name_parts: list[str] = name.split()   
                # приклад: Якщо ім'я "Тарас Шевченко", воно стане ["Тарас", "Шевченко"]
                
        # перевірка того, чи містить вхідний рядок дві частини чи ні
        if len(name_parts) == 2:
            first_name, last_name = name_parts   # #віднесення першої частини до імені та другої частини до прізвища
            
            # перевірка того, чи введений рядок містить лише кириличні символи.
            # якщо у вхідному рядку присутні будь-які некириличні символи, виникає помилка.           
            if not all(ch in ukr_alphabet for ch in first_name+last_name):
                raise ValueError("Input string contains non-Cyrillic characters")

        else:   
            raise ValueError("Input string must contain a first and last name separated by a space") 
        # транслітерація імені за допомогою таблиці кирилиця-латиниця по модулю alphabet.py
        translit_name: str = f"{ukr_alphabet.get(last_name[0], last_name[0])}.{''.join([ukr_alphabet.get(ch, ch) for ch in first_name])}"
        # повернення транслітерованого імені в нижньому регістрі
        return translit_name.lower()
    
    except ValueError as e:  
        print(f"Error: {e}") 
        return ''

# отримання повного імені
name: str = str(input('Paste fullname: '))
# транслітерація українського імені та прізвища в латиницю
username: str = transliterate_ukr(name)


if username:
    pyad.set_defaults(ldap_server=ad_server, username=ad_username, password=ad_password)
    passwd = password()
    
    # extract the transliterated name
    trans_name: str = transliterate_ukr(name)

    user = pyad.aduser.ADUser.from_cn(trans_name, 'Employees/All')
    user.set_password(passwd)
    user.set_password_never_expires(True)
    user.set_password_expired(False)
    user.set_user_account_control_settings(pyad.aduser.user)

    # отримати ім'я та прізвище
    first_name, last_name = name.split()
   
    # завдання імені та прізвища
    user.update_attribute('givenName', f'{first_name}')
    user.update_attribute('sn', f'{last_name}')
    user.update_attribute('displayName', f'{first_name} {last_name}')

    # вiдображення змін
    user.update()    
    passwd: str = password() 
    print(f'Пользователь создан:\n'
          f'{ad_username}@kvadra.in.ua\n'
          f'Логин: {ad_username}\n'
          f'Пароль: {ad_password}'
          ) 
