# Educational project

import pandas as pd
import numpy as np

# налаштування візуалізації
pd.set_option("display.max_columns", 50) 
pd.set_option("display.width", 180) # скільки виводить символів на екран 

# 1. Імпорт та первинне дослідження

# url = "https://s3-eu-west-1.amazonaws.com/shanebucket/downloads/uk-500.csv"
url = "data/uk-500.csv"

df_origin = pd.read_csv(url)

COLUMNS_TO_DROP = [] # константна змінна = якщо слово написано великими літерами; сторили порожній список, перелік стовпчиків, які потрібно видалити

print("\n--- head ---")
print(df_origin.head())


df_origin.head() # Показує перші 5 рядків

print("\n--- info ---")
print(df_origin.info()) # info, show some gups

print("\n--- describe ---")
print(df_origin.describe()) # statistics - numbers

print("\n--- describe for str ---")
print(df_origin.describe(include=[object]).T) # statistics - string, частота - скільки зустрічається у таблиці

print("--- null ---")
# print(df.isna().sum()) # count a sum => пропущених ячейок немає
print(df_origin.isna().sum().sort_values(ascending=False).head(20)) # 20 пропусків ВАЖЛИВО ЗАПАМʼЯТАТИ

print("--- dublicated ---")
print(df_origin.duplicated().sum()) # перевірка дублікатів рядків, у даному прикладі дублікатів нема (відображено 0)

print("--- list columns ---") # повертає лише назви колонок
list_col = df_origin.columns 
print(list(list_col))
for i, col in enumerate(df_origin.columns): # икористуємо enumerateдля подальшої роботи працівників
    print(f"{i:02d}.{col}") # 00 , 01, 03

# 2. Очищення даних
df = df_origin.copy() # робимо копію


# 2.1 Видалити непотрібні колонки (за рішенням аналітика)
if COLUMNS_TO_DROP: # перевіряємо чи у списку щось є
    print("\n--- delete columns in list ---")
    df = df.drop(columns=[col for col in COLUMNS_TO_DROP if col in df.columns], errors='ignore') # звертаємося до копії та видаляємо стовпчики: поверни мені елемент із мого списку; ігноруй помилку, якщо список порожній, то повертати нічого не потрібно
    # columns = []    
    # for col in COLUMNS_TO_DROP:
    #     if col in df_raw.columns:
    #         columns.append(col)
else:
    print("\nCOLUMNS_TO_DROP = empty") # нічого видаляти не потрібно

def standartize_text(s): # стоорили фукнцію, із аргументом s
    if pd.isna(s): # is - чи  na - ячейка, яка буде рядком
        return np.nan # numpy прирівнює всі порожнини до типу nan
    
    if not isinstance(s, str): # додаємо перевірку, якщо моє значення не є рядком , не считується рядоком, то мені його треба зроби рядком
        s = str(s)
    
    s = s.strip() # прибрали пробіли зліва і справа, напочатку і в кінці
    s = " ".join(s.split()) # считує всі символи всередині та зʼєднує всі слова і одним пробілом (" ") 

    return s # зробили старндартизацію 

for col in df.select_dtypes(include=['object']).columns: # проходимося по стовпчиках та приміняємо: бери тільки ті значення, які відповідюьть тільки порожнинам і рядка, порожними ми обходимо, беремо тільки найменування стовпчиків; # apply - бере ячейку і підтавляє ту функцію , яку ми ʼй надали 
    df[col] = df[col].apply(standartize_text)# звертаюся та перезаписую

# print(df_raw) #

# 2.3 Очистити phone та fax від пробілів/символів
# possible_email_cols = [c for c in df.colimns if "email" in c.lower()] # проходжусь по кожному найменнування стовпчику копію, звертась до сповпчика з електронною адресою, кожен має прописаний з таким словом
# possible_web_cols = [c for c in df.colimns if ("web" in c.lower()) or ("website" in c.lower() or "url" in c.lower())] # через or - перевіряю web website url

# possible_phone_cols = [c for c in df.colimns if ("web" in c.lower()) or ("website" in c.lower() or "url" in c.lower())]
# possible_fax_cols = [c for c in df.colimns if ("web" in c.lower()) or ("website" in c.lower() or "url" in c.lower())]

possible_email_cols = [c for c in df.columns if "email" in c.lower()]
possible_web_cols = [c for c in df.columns if ("web" in c.lower() or "website" in c.lower() or "url" in c.lower())]
possible_phone_cols = [c for c in df.columns if ("phone" in c.lower() or "telephone" in c.lower() or "tel" in c.lower())]
possible_fax_cols = [c for c in df.columns if "fax" in c.lower()]

# генерація списку
# [змінна_циклу(з примінненними операціями) for змінна_циклу in де_проходимося]
# [0,1,2,3]
#[n for n in range (4)]

print("\nPossible columns:")
print("Email cols:", possible_email_cols)
print("Web cols:", possible_web_cols)
print("Phone cols:", possible_phone_cols)
print("Fax cols:", possible_fax_cols)

# Приміняємо зміни
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].apply(standatize_text)

