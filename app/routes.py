import os
from app import app
from flask import render_template, redirect, Response, url_for, request
from flask_csv import send_csv
from app.scraper import LoginForm, scrape
from selenium import webdriver
from contextlib import contextmanager
CHROME_PATH = app.config['CHROME_PATH']
CHROME_BIN = app.config['CHROME_BIN']



def driver_init(CHROME_PATH, CHROME_BIN=None):
    options = webdriver.ChromeOptions()
    if CHROME_BIN:
        options.binary_location = CHROME_BIN
    options.add_argument('--window-size=1200,800')
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--incognito')
    driver = webdriver.Chrome(executable_path=CHROME_PATH,
                              options=options)
    return driver


@contextmanager
def driver_context(type='chrome'):
    if type == 'chrome':
        driver = driver_init(CHROME_PATH, CHROME_BIN)
        yield driver
    else:
        driver = webdriver.PhantomJS(executable_path=app.config['PHANTOM_PATH'], service_args=['--load-images=no'])
        driver.set_window_size(1120, 550)
        yield driver
    driver.quit()


@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            os.remove(app.config['OUTPUT_PATH'])
        except:
            pass
        with driver_context() as driver:
            df, ls = scrape(driver, form.username.data, form.password.data)
        return send_csv(ls,
                        "latest-littlefield.csv",
                        ["Day",
                         "Customer Orders",
                         "Queued Orders",
                         "Inventory Level",
                         "Machine 1 Utilisation Rate",
                         "Machine 2 Utilisation Rate",
                         "Machine 3 Utilisation Rate",
                         "Machine 1 Queue",
                         "Machine 2 Queue",
                         "Machine 3 Queue",
                         "Completed Jobs Tier 1",
                         "Completed Jobs Tier 2",
                         "Completed Jobs Tier 3",
                         "Avg Lead Time Tier 1",
                         "Avg Lead Time Tier 2",
                         "Avg Lead Time Tier 3",
                         "Avg Revenue Tier 1",
                         "Avg Revenue Tier 2",
                         "Avg Revenue Tier 3"])
    return render_template('index.html', form=form)


# @app.route('/data')
# def data_load():
#     return render_template('data_ready.html')
#
#
# @app.route('/download')
# def plot_csv():
#     file_path = os.path.join(os.path.dirname(__name__), os.path.pardir, 'output', 'latest-littlefield.csv')
#     with open(file_path) as file:
#         csv_file = file.read
#     resp = Response(csv_file,
#                     mimetype='text/csv',
#                     headers={"Content-disposition":
#                              "attachment; filename=latest-littlefield.csv"})
#     return resp