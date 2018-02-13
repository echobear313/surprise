from flask import Flask
from flask import render_template, request
import spider
import time
from selenium import webdriver
import json
import threading
from qcloudsms_py import SmsSingleSender
import os
app = Flask(__name__)

username = "小何"
password = "helloxiaohe"
phonenumber = "18800201072"
dstation = "成都"
astation = "上海"
date = "2018-02-27"
expected_price = 100

@app.route('/', methods=['POST', 'GET'])
def index():
    global username
    global password
    global phonenumber
    global dstation
    global astation
    global date
    global expected_price
    if request.method == 'POST':
        post_password = request.form['password']
        print(post_password)
        post_dstation = request.form['dstation']
        post_astation = request.form['astation']
        post_date = request.form['date']
        post_expected_price = request.form['expected_price']
        if post_password == password:
            dstation = post_dstation
            astation = post_astation
            date = post_date
            expected_price = post_expected_price
            print(username, password, phonenumber, dstation, astation, date)
            return render_template("index.html", username=username, dstation=dstation, astation=astation, date=date, expected_price=expected_price)
        else:
            return "<h1>用户名或密码错误</h1>"
    else:
        return render_template("index.html", username=username, dstation=dstation, astation=astation, date=date, expected_price=expected_price)

@app.route('/get_result', methods=['GET' ])
def get_result():
    global all_city
    global dstation
    global astation
    global date
    t1 = time.time()
    driver = webdriver.PhantomJS(executable_path=os.path.join("phantomjs", "phantomjs"), service_args=['--load-images=no'])
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
    t2 = time.time()
    print("load webdriver:", t2-t1)
    result_list = spider.get_ticket_info(all_city[dstation], all_city[astation], date, driver)
    try:
        lowest_ = result_list[0]
    except IndexError as e:
        return "请稍后再试"
    lowest_ = [str(x).strip() for x in lowest_]
    print(lowest_)
    return " ".join(lowest_[:-2])+"<h4>当前最低价 %s</h4>" % lowest_[-1]


def background_thread():
    global all_city
    global dstation
    global astation
    global date
    global expected_price
    global phonenumber
    index = 1
    appid = 1400068164
    appkey = "ae90627c37cacb8b1c8f4ba110e9dbbc"
    template_id = 86380
    ssender = SmsSingleSender(appid, appkey)
    while True:
        t1 = time.time()
        driver = webdriver.PhantomJS(executable_path=os.path.join("phantomjs", "phantomjs"), service_args=['--load-images=no'])
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        t2 = time.time()
        print("load webdriver:", t2-t1)
        print("background thread runs %s times!" % index)
        result_list = spider.get_ticket_info(all_city[dstation], all_city[astation], date, driver)
        try:
            lowest_ = result_list[0]
        except IndexError as e:
            time.sleep(10)
            continue
        lowest_ = [str(x).strip() for x in lowest_]
        lowest_[1] = "<" + dstation + " " + lowest_[1] + ">"
        lowest_[2] = "<" + astation + " " + lowest_[2] + ">"
        if int(lowest_[-1]) <= expected_price:
            result = ssender.send_with_param(86, phonenumber,
					template_id, lowest_)['result']
            print("sending a sms! result code", result)
        print("background_thread: ", lowest_)
        time.sleep(3600)
        index += 1


if __name__ == '__main__':
    with open("city_info.json", "r") as f:
        all_city = json.loads(f.read())
    threading.Thread(target=background_thread).start()
    app.run(host='0.0.0.0')