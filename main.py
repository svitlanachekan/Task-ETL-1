# Educational project
# GMT20251118-122823

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


# 2.1 Видалити непотрібні стовпчики (за рішенням аналітика)
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

# Застосовуємо зміни
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].apply(standartize_text)

# email    
for col in possible_email_cols:
    df[col] = df[col].str.lower()
    
# web    
for col in possible_web_cols:
    df[col] = df[col].str.lower()
    
# clean phone/fax
def clean_phone(x):
    if pd.isna(x):
        return np.nan
    s = str(x)
    s = s.strip()

    # plus = "" # не був досліджений та считувувся як число, додоємо "
    # if s.startswith("+"):
    #     plus = "+"

# 2 варіант
    plus = "+" if s.startswith("+") else "" # !!! ЗАПАЬʼЯТАТИ КОРОТКИЙ ВАРІАНТ

    # digits = "" # беремо рядок, розбиваємо, та перевіряємо, чи це число
    # for ch in s:
    #     if ch.isdigit():
    #         digits += ch
        
    digits = "".join(ch for ch in s if ch.isdigit())

    if digits == "":
        return np.nan
    
    # 'ljflsjg- 5467' -> digits='1234567' видаляє, якщо не підоходить до функцції digit
    # 'qwe--ty' -> digits=''

    return plus + digits # прибрали літери

for col in possible_phone_cols + possible_fax_cols:
    #якщо прибрати всі рисочки, то залишаю номер, якщо відозмінити телеіфони, то треба розуміти , яка країна 
    df[col] = df[col].apply(clean_phone)

# 2.4. Стандартизувати формат текстових полів
def title_if_str(s):
    if pd.isna(s):
        return np.nan
    return str(s).title()

city_cols = [c for c in df.columns if c.lower() in ("city", "city_name", "town")]

address_cols = [c for c in df.columns if c.lower() in ("address")]

name_cols = [c for c in df.columns if c.lower() in ("name", "first_name", "second_name", "last name")]

name_title = city_cols + address_cols + name_cols 
if city_cols + address_cols + name_cols: 
    for col in name_title:
        df[col] = df[col].apply(title_if_str) 
    print( '\n--- name of title ---')
else:
    print("\n--- haven't name ---")

# 3. Створення нових колонок (Feature Engineering)

df["full_name"] = df.first_name + " " + df.last_name

df["city_length"] = df["city"].apply(len)

# df["city2"] = df["city"].str.len()

# df["is_gmail"] = 
# print([bool(s) for s in df["email"] if "@gmail.com" in str(s).lower()])

df["is_gmail"] = [True if "@gmail.com" in str(s).lower() else False for s in df["email"]]

# possible_email_cols = [c for c in df.columns if "email" in c.lower()]


# 4. Фільтрація даних

print("\n--- підвибірки ---")

# користувачі з доменом gmail.com
gmail_users = df.loc[df['is_gmail'] == True].copy()
# print(gmail_users)

print("Gmail users:", len(gmail_users))

# працівники компаній з “LLC” або “Ltd”

# df["company_name"]

df["company_name"] = df["company_name"].fillna("")
# print(df["company_name"].fillna(""))

mask_LLC_Ltd = df.company_name.str.contains(r"\b(LLC|Ltd|llc|LTD|ltd)\b", regex=True, na=False)
# print(mask_LLC_Ltd)

company_llc_ltd = df.loc[mask_LLC_Ltd].copy()
# print(company_llc_ltd)

print("Company LLC and Ltd:", len(company_llc_ltd))


# 5. Позиційна вибірка (iloc)

# iloc[row, col]

try:
    first_10_cols_2_5 = df.iloc[:10, 2:6]
    print("\nПерші 10 рядків + колонки 2–5")
    print(first_10_cols_2_5)
except Exception as e:
    print("Can`t (Перші 10 рядків + колонки 2–5):", e)


every_10th = df.iloc[::10, :].copy()
print("\nevery_10th")
print(every_10th)


random_5 = df.sample(5, random_state=42)
print("\nrandom 5 row")
print(random_5)


# 6. Групування та статистика



# print(df.head())









        