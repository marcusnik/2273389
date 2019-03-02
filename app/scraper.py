import os
import time
from bs4 import BeautifulSoup
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import pandas as pd
from app import app


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = StringField("Password")
    submit = SubmitField('Confirm')


def login(driver, username, password):
    time.sleep(2)
    driver.find_element_by_name('id').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_xpath("//input[@value='ok']").click()
    time.sleep(3)


def without_split(driver, df):
    required = {
        "Customer Orders": "http://op.responsive.net/Littlefield/Plot?data=JOBIN&x=all",
        "Queued Orders": "http://op.responsive.net/Littlefield/Plot?data=JOBQ&x=all",
        "Inventory Level": "http://op.responsive.net/Littlefield/Plot?data=INV&x=all",
        "Machine 1 Utilisation Rate": "http://op.responsive.net/Littlefield/Plot?data=S1UTIL&x=all",
        "Machine 2 Utilisation Rate": "http://op.responsive.net/Littlefield/Plot?data=S2UTIL&x=all",
        "Machine 3 Utilisation Rate": "http://op.responsive.net/Littlefield/Plot?data=S3UTIL&x=all",
        "Machine 1 Queue": "http://op.responsive.net/Littlefield/Plot?data=S1Q&x=all",
        "Machine 2 Queue": "http://op.responsive.net/Littlefield/Plot?data=S2Q&x=all",
        "Machine 3 Queue": "http://op.responsive.net/Littlefield/Plot?data=S3Q&x=all"
    }
    for key, value in required.items():
        driver.get(value)
        driver.find_element_by_name('data').click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data_ls = soup.find_all('td')[2:]
        data = list()
        if key == 'Inventory Level':
            current = None
            last = len(data_ls) - 2
            for i in range(len(data_ls)):
                if i % 2 == 0:
                    if i == last:
                        text = "".join(data_ls[i + 1].text.split(","))
                        append_type(data, text)
                    elif current == round(float(data_ls[i].text)):
                        pass
                    elif round(float(data_ls[i].text)) != current:
                        text = "".join(data_ls[i-1].text.split(","))
                        append_type(data, text)
                    current = round(float(data_ls[i].text))
                else:
                    pass

        else:
            for i in range(len(data_ls)):
                if i % 2 == 0:
                    text = "".join(data_ls[i+1].text.split(","))
                    try:
                        data.append(int(text))
                    except:
                        data.append(float(text))
                else:
                    pass
        df[key] = data
    return df


def append_type(list_name, text):
    try:
        list_name.append(int(text))
    except:
        list_name.append(float(text))


def split_category(driver, df):
    required = {
        "Completed Jobs Tier ": "http://op.responsive.net/Littlefield/Plot?data=JOBOUT&x=all",
        "Avg Lead Time Tier ": "http://op.responsive.net/Littlefield/Plot?data=JOBT&x=all",
        "Avg Revenue Tier ": "http://op.responsive.net/Littlefield/Plot?data=JOBREV&x=all"
    }
    for key, value in required.items():
        driver.get(value)
        driver.find_element_by_name('data').click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data_ls = soup.find_all('td')[4:]
        data1, data2, data3 = list(), list(), list()
        for i in range(len(data_ls)):
            if i % 4 == 0:
                [text1, text2, text3] = ["".join(data_ls[i + j].text.split(",")) for j in range(1, 4)]
                append_type(data1, text1)
                append_type(data2, text2)
                append_type(data3, text3)
            else:
                pass
        df[key + str(1)] = data1
        df[key + str(2)] = data2
        df[key + str(3)] = data3
    return df


def scrape(driver, username, password):
    try:
        os.remove(app.config['OUTPUT_PATH'])
    except Exception as e:
        print(e)
        pass
    driver.get("http://op.responsive.net/lt/sharma/entry.html")
    login(driver, username, password)
    df = dict()
    df = without_split(driver, df)
    df = split_category(driver, df)
    ls = list()
    length = len(df['Customer Orders'])
    for i in range(length):
        elem = dict()
        for key, value in df.items():
            elem[key] = value[i]
        elem['Day'] = int(i) + 1
        ls.append(elem)
    # df = pd.DataFrame.from_dict(df)
    # df.to_csv(app.config['OUTPUT_PATH'])
    return df, ls

