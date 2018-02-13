# surprise
基于phantomjs+selenium的携程机票爬虫，缺陷是速度很慢，大概十秒才能刷新出来。     
爬取机票信息，通过腾讯云SMS短信通知.    
并且展示当前设置，需要初始化个人信息.
### Demo
[demo](http://lovexiongqingyue.cn:5000/).

#### run `python3 main.py` to see the demo
```
username = ""
password = ""
phonenumber = ""
dstation = "成都"
astation = "上海"
date = "2018-02-27"
expected_price = 100
```
初始化个人信息，可以通过表单更新.

### Requirements
```
pip3 install flask selenium qcloudsms_py beautifulsoup4 lxml
```
    
```python
appid = 
appkey = ""
template_id = 
```
填写自己的腾讯云SMS服务的appid、appkey、template_id.   

