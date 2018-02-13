from bs4 import BeautifulSoup
from selenium import webdriver
import time


def get_ticket_info(dstation, astation, date, driver):
    url = "http://flights.ctrip.com/booking/%s-%s-day-1.html?DDate1=%s" % (dstation, astation, date)
    t1 = time.time()
    driver.get(url)
    t2 = time.time()
    print("get url:", t2-t1)
    # time.sleep(5)

    initial_pagesource = driver.page_source
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(0.1)
        if initial_pagesource == driver.page_source:
            break
        initial_pagesource = driver.page_source
# with open("xiaohuang.txt", "w") as f:
#     f.write(driver.page_source)
    t1 = time.time()
    # soup = BeautifulSoup(driver.page_source)
    soup = BeautifulSoup(initial_pagesource, "lxml")
    t3 = time.time()
    print("bs4:", t3-t1)
    result = soup.find_all("div", class_=["search_box", "search_box_tag", "search_box_light"])
# print(len(result))
#     print(type(result[0]))
    result_list = []
    for ticket_info in result:
    # print(ticket_info.string)
        try:
            airplane_name = "<" + ticket_info.find_all('div', class_=["clearfix", "J_flight_no"])[0].text + ">"
            d_info_div = ticket_info.find_all('td', class_=["right"])[0].find_all('div')
            airplane_dtime = "<" + d_info_div[0].text + ">"
            airplane_dstation = d_info_div[1].text
            a_info_div = ticket_info.find_all('td', class_=["left"])[0].find_all('div')
            airplane_atime = "<" + a_info_div[0].text + ">"
            airplane_astation = a_info_div[1].text
            airplane_price = int(''.join(list(filter(str.isdigit, ticket_info.find_all('span', class_=["base_price02"])[0].text))))

            result_list.append([airplane_name, airplane_dstation, airplane_astation, airplane_dtime, airplane_atime, airplane_price])
        except:
            pass
    t2 = time.time()
    print("parse the html:", t2-t1)
    return sorted(result_list, key=lambda x: x[-1])

if __name__ == "__main__":
    driver = webdriver.PhantomJS(executable_path="./phantomjs", service_args=['--load-images=no'])
    result_list = get_ticket_info('CTU', 'SHA', '2018-02-27', driver)
    print(result_list)
    # t = SpiderThread('CTU', 'SHA', '2018-02-27')
    # t.start()
    # time.sleep(100)
    # print(t.get_result())