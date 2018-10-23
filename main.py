#coding=utf-8
import requests
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
import copy
import time
import re
import os
import json
import io
import urllib2
import json
import string
import datetime

class Spider:
    class Lesson:

        def __init__(self, name, code, teacher_name, Time, number):
            self.name = name
            self.code = code
            self.teacher_name = teacher_name
            self.time = Time
            self.number = number

        def show(self):
            print('  name:' + self.name + '  code:' + self.code + '  teacher_name:' + self.teacher_name + '  time:' + self.time)

    def __init__(self, url):
        self.__uid = ''
        self.__real_base_url = ''
        self.__attendetail_url = 'http://kaoqin.weigaogroup.com:8010/StaffSelf/AttenDetail.aspx'
        self.__absencesheet_url = 'http://kaoqin.weigaogroup.com:8010/StaffSelf/AbsenceSheet.aspx'
        self.__base_url = url
        self.__name = ''
        self.__base_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            'ddl_kcxz': '',
            'ddl_ywyl': '',
            'ddl_kcgs': '',
            'ddl_xqbs': '',
            'ddl_sksj': '',
            'TextBox1': '',
            'dpkcmcGrid:txtChoosePage': '1',
            'dpkcmcGrid:txtPageSize': '200',
        }
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
             'Content-Type':'application/x-www-form-urlencoded',
             'Accept-Charset': 'gb2312,gbk;q=0.7,utf-8;q=0.7,*;q=0.7',

        }
        self.session = requests.Session()
        self.__now_lessons_number = 0
        self.VIEWSTATE ='' 
        self.VIEWSTATEGENERATOR = ''
        self.EVENTVALIDATION = ''
        #self.bs = webdriver.Firefox()

    def __set_real_url(self):
        '''
        得到真实的登录地址（无Cookie）
        获取Cookie（有Cookie)
        :return: 该请求
        '''
        request = self.session.get(self.__base_url, headers=self.__headers)
        real_url = request.url
        if real_url != 'http://kaoqin.weigaogroup.com:8010/login.aspx' and real_url != 'http://kaoqin.weigaogroup.com:8010/login.aspx':   # 湖南工业大学
            self.__real_base_url = real_url[:len(real_url) - len('default2.aspx')]
        else:
            if real_url.find('index') > 0:
                self.__real_base_url = real_url[:len(real_url) - len('index.aspx')]
            else:
                self.__real_base_url = real_url

        return request
    def __set_atten_url(self):
        '''
        得到真实的登录地址（无Cookie）
        获取Cookie（有Cookie)
        :return: 该请求
        '''
        request = self.session.get(self.__attendetail_url, headers=self.__headers)
        print("attened "+ request.url)
        return request

    def __set_absence_url(self):
        '''
        得到真实的登录地址（无Cookie）
        获取Cookie（有Cookie)
        :return: 该请求
        '''
        print("__set_absence_url called ")
        request = self.session.get(self.__absencesheet_url, headers=self.__headers)
        #print request
        print("absence")
        #print self.__absencesheet
        return request

    def __get_code(self):
        '''
        获取验证码
        :return: 验证码
        '''
        if self.__real_base_url != 'http://218.75.197.123:83/':
            request = self.session.get(self.__real_base_url + 'CheckCode.aspx', headers=self.__headers)
        else:
            request = self.session.get(self.__real_base_url + 'CheckCode.aspx?', headers=self.__headers)
        with open('code.jpg', 'wb')as f:
            f.write(request.content)
        im = Image.open('code.jpg')
        im.show()
        print('Please input the code:')
        code = input()
        return code

    def __get_login_data(self, uid, password):
        '''
        得到登录包
        :param uid: 学号
        :param password: 密码
        :return: 含登录包的data字典
        '''
        self.__uid = uid
        request = self.__set_real_url()
        print(request.text)
        soup=BeautifulSoup(request.text)
        __VIEWSTATE=soup.find(id="__VIEWSTATE")['value'] 
        __VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value'] 
        __EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value'] 
        #print("viewstate = " + __VIEWSTATE)
        #print("viewstate = " + __VIEWSTATEGENERATOR)
        #print("viewstate = " + __EVENTVALIDATION)        
        data = {
            '__VIEWSTATE': __VIEWSTATE,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': __EVENTVALIDATION,
            'txtName': self.__uid,
            'txtPass': password,
            'btnLogin':'',
        }
        return data
    
    def __get_attendetail_data(self):
        '''
        得到登录包
        :param uid: 学号
        :param password: 密码
        :return: 含登录包的data字典
        '''
        self.__uid = uid
        request = self.__set_atten_url()
        #print(request.text)
        soup=BeautifulSoup(request.text)
        __VIEWSTATE=soup.find(id="__VIEWSTATE")['value'] 
        __VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value'] 
        __EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value'] 
        #agvTableCallbackState = soup.find(id="agvTable$CallbackState")['value'] 
        #print("__VIEWSTATE = " + __VIEWSTATE)
        #print("__VIEWSTATEGENERATOR = " + __VIEWSTATEGENERATOR)
        #print("__EVENTVALIDATION = " + __EVENTVALIDATION)        
        data = {
            '__VIEWSTATE': __VIEWSTATE,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': __EVENTVALIDATION,
            #'ASPxRoundPanel1$deStartTime': '2018-10-01',
            #"ASPxRoundPanel1$deEndTime": "2018-10-08",
            #'ASPxRoundPanel1_cbType1_I': '全部', 
            #'ASPxRoundPanel1_cbType1_VI': '全部', 
            #'ASPxRoundPanel1_deEndTime_Raw': '1540944000000',
            #'ASPxRoundPanel1_deStartTime_Raw': '1538352000000',
            "ASPxRoundPanel1$btnSerch":"",
            
             'hdfSqlWhere':'1=2'
        }

        #           
        return data

    def __get_absence_shift_data(self):
        self.__uid = uid
        request = self.__set_absence_url()
        print(request.text)
        soup=BeautifulSoup(request.text)
        __VIEWSTATE=soup.find(id="__VIEWSTATE")['value'] 
        __VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value'] 
        __EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value'] 
        print("__VIEWSTATE = " + __VIEWSTATE)
        print("__VIEWSTATEGENERATOR = " + __VIEWSTATEGENERATOR)
        print("__EVENTVALIDATION = " + __EVENTVALIDATION)        
        data = {
            '__VIEWSTATE':__VIEWSTATE,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': __EVENTVALIDATION,

            #'ASPxRoundPanel1$deEndTime':'2018-10-31',
            #'ASPxRoundPanel1$deEndTime$DDD$C':'10/31/2018:10/31/2018',
            'ASPxRoundPanel1$deStartTime':'2018-10-01',
            'ASPxRoundPanel1$btnAddShift':'',
            'hdfSqlWhere':'1=2'
        }
        return data

    def __get_absence_data(self):

        submiteDate = "2018-10-01"
        
        self.__uid = uid
        #request = self.__set_absence_url()
        #print(request.text)
        #soup=BeautifulSoup(request.text)
        __VIEWSTATE= self.VIEWSTATE
        __VIEWSTATEGENERATOR = self.VIEWSTATEGENERATOR
        __EVENTVALIDATION = self.EVENTVALIDATION
        print("__VIEWSTATE = " + __VIEWSTATE)
        print("__VIEWSTATEGENERATOR = " + __VIEWSTATEGENERATOR)
        print("__EVENTVALIDATION = " + __EVENTVALIDATION)        
        data = {
            '__VIEWSTATE':__VIEWSTATE,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': __EVENTVALIDATION,
            'ASPxRoundPanel1$deStartTime': '2018-10-01',
            'ASPxRoundPanel1$deEndTime': '2018-10-30',
            
            #"ppcSheet$TPCC0$TC$deDate":	"2018-10-01",
            #'ppcSheet$TPCC0$TC$deDate$DDD$C':'10/23/2018:10/01/2018',
            #"ppcSheet$TPCC0$TC$teDate":	"17:00",
            #'ppcSheet$TPCC0$TC$rblInOrOut:':'0',
            #'ppcSheet$TPCC0$TC$meReason':'',
            #"ppcSheet$TPCC0$TC$btnAddOK":"",
            'hdfSqlWhere':'1=2',
            #'ppcSheetWS':'1:1:12000:432:-17:0:-10000:-10000:1'
            'agvTable$DXKVInput':'[]',
            'agvTable$DXSelInput':'',	
            'ASPxRoundPanel1_deEndTime_DDD_C_FNPWS':'0:0:-1:-10000:-10000:0:0px:-10000:1',
            'ASPxRoundPanel1_deEndTime_DDDWS':'0:0:-1:-10000:-10000:0:-10000:-10000:1',
            'ASPxRoundPanel1_deEndTime_Raw':'1540944000000',
            'ASPxRoundPanel1_deStartTime_DDD_C_FNPWS':'0:0:-1:-10000:-10000:0:0px:-10000:1',
            'ASPxRoundPanel1_deStartTime_DDDWS':'0:0:-1:-10000:-10000:0:-10000:-10000:1',
            'ASPxRoundPanel1_deStartTime_Raw':'1538352000000',
            'ASPxRoundPanel1$deEndTime':'2018-10-31',
            'ASPxRoundPanel1$deEndTime$DDD$C':'10/31/2018:10/31/2018',
            'ASPxRoundPanel1$deStartTime':'2018-10-01',
            'ASPxRoundPanel1$deStartTime$DDD$C':'10/01/2018:10/01/2018',
            'DXScript	':'1_44,1_76,2_34,2_41,2_33,1_48,1_69,1_67,2_28,2_27,1_54,3_7,2_37,2_39,2_36',
            'ppcSheet_TPCC0_deDate_0_DDD_C_FNPWS':'0:0:-1:-10000:-10000:0:0px:-10000:1',
            'ppcSheet_TPCC0_deDate_0_DDDWS':'0:0:12000:531:147:0:-10000:-10000:1',
            'ppcSheet_TPCC0_deDate_0_Raw':'1538389796012',
            'ppcSheet_TPCC0_teDate_0_Raw':'-59011398000000',
            'ppcSheet$TPCC0$TC$btnAddOK	':'',
            'ppcSheet$TPCC0$TC$deDate	':'2018-10-01',
            'ppcSheet$TPCC0$TC$deDate$DDD$C':'10/23/2018:10/01/2018',
            'ppcSheet$TPCC0$TC$meReason	':'',
            'ppcSheet$TPCC0$TC$rblInOrOut':'0',
            'ppcSheet$TPCC0$TC$rblInOrOut$RB0':'C',
            'ppcSheet$TPCC0$TC$rblInOrOut$RB1':'U',
            'ppcSheet$TPCC0$TC$teDate':'17:00',
            'ppcSheetWS	':'1:1:12000:432:-17:0:-10000:-10000:1',

            "ASPxRoundPanel1$btnAddShift":""
            
        }
        return data





    
    def __get_cookie_from_network(self):
        '''
        首次进入选课界面
        :return: none
        '''
        url_login = 'http://kaoqin.weigaogroup.com:8010/login.aspx' 
        driver = webdriver.PhantomJS()
        driver.get(url_login)
        driver.find_element_by_xpath('//input[@type="text"]').send_keys(self.__uid) # 改成你的微博账号
        driver.find_element_by_xpath('//input[@type="password"]').send_keys(password) # 改成你的微博密码
        
        driver.find_element_by_xpath('//input[@type="submit"]').click() # 点击登录
        
        # 获得 cookie信息
        cookie_list = driver.get_cookies()
        print cookie_list
        
        cookie_dict = {}
        for cookie in cookie_list:
        
            f = open(cookie['name']+'.weibo','w')
            pickle.dump(cookie, f)
            f.close()
        
        if cookie.has_key('name') and cookie.has_key('value'):
            cookie_dict[cookie['name']] = cookie['value']
        
        return cookie_dict
        
    def login(self, uid, password):
        '''
        外露的登录接口
        :param uid: 学号
        :param password: 密码
        :return: 抛出异常或返回是否登录成功的布尔值
        '''
        #self.__get_cookie_from_network()
        while True:
            data = self.__get_login_data(uid, password)
            if self.__real_base_url != 'http://kaoqin.weigaogroup.com:8010':
                self.__real_base_url = 'http://kaoqin.weigaogroup.com:8010/'
                request = self.session.post(self.__real_base_url + 'Login.aspx', headers=self.__headers, data=data)
            else:
                self.__real_base_url = 'http://kaoqin.weigaogroup.com:8010/'
                print("url2" + self.__real_base_url)            
                request = self.session.post(self.__real_base_url + 'Login.aspx', headers=self.__headers, data=data)
            #print(request.text)
            dict_cookies=self.session.cookies.get_dict()#获取cookies  
           
    
            print dict_cookies
            soup = BeautifulSoup(request.text)
            
            if request.status_code != requests.codes.ok:
                print('4XX or 5XX Error,try to login again')
                time.sleep(0.5)
                continue
            if request.text.find('ChangeLanguage') > -1:
                print('登录成功！')
            try:
                self.__enter_lessons_first()
                return True
            except:
                print('Unknown Error,try to login again.')
                time.sleep(1000)
                #continue
        
    def __submit_absence_day_time(self):
        print("ABSENCE ABSENCE ABSENCE ABSENCE ABSENCE ABSENCE")
        #def __submit_absence_day_time(self,date ='',time = ''):
        
        data = self.__get_absence_shift_data()
        request = self.session.post(self.__absencesheet_url, data=data, headers=self.__headers)
        print "Shift Start"
        print request.status_code
        print "Shift End"
        soup=BeautifulSoup(request.text)
        __VIEWSTATE=soup.find(id="__VIEWSTATE")['value'] 
        __VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value'] 
        __EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value'] 
        print("__VIEWSTATEtttttt = " + __VIEWSTATE)
        print("__VIEWSTATEGENERATORttttt = " + __VIEWSTATEGENERATOR)
        print("__EVENTVALIDATION = " + __EVENTVALIDATION)   
        self.VIEWSTATE =__VIEWSTATE 
        self.VIEWSTATEGENERATOR = __VIEWSTATEGENERATOR
        self.EVENTVALIDATION = __EVENTVALIDATION
        data = self.__get_absence_data()
        self.__headers['Referer'] = self.__absencesheet_url
        request = self.session.post(self.__absencesheet_url, data=data, headers=self.__headers)
        print("ABSENCE ABSENCE ABSENCE ABSENCE ABSENCE ABSENCE")
        self.__headers['Referer'] = request.url
        soup = BeautifulSoup(request.text, features="html.parser")
        #print soup.prettify()
        #print request.status_code
        
    def __enter_lessons_first(self):
        '''
        首次进入选课界面
        :return: none
        '''
        data = self.__get_attendetail_data()
        self.__headers['Referer'] = self.__attendetail_url
        request = self.session.post(self.__attendetail_url, data=data, headers=self.__headers)
        print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
        #soup.prettify(request.text)
        self.__headers['Referer'] = request.url
        soup = BeautifulSoup(request.text, features="html.parser")
        #print soup.prettify()
        print request.status_code

        souptr = soup.find_all('tr', class_='dxgvDataRow_Office2010Blue')

        total_day = len(souptr)/2

        print total_day
        
        date_css = 'td#agvTable_tccell{}_0'
        shift_css = 'td#agvTable_tccell{}_1'
        card_css = 'tr#agvTable_DXDataRow{} td.dxgv'
        att_css = 'td#agvTable_tccell{}_5'

        date_list = []
        shift_list = []
        card_list = []
        att_list = []
        inline_list = []

        for i in range(total_day):
            
            inline_list = []
            inline_list.append(soup.select(date_css.format(i))[0].string.strip())
            inline_list.append(soup.select(shift_css.format(i))[-1].string.strip())
            if soup.select(card_css.format(i))[3].string.strip() == "":
               inline_list.append("CAR_NA") #append NA to indicate not the full day
            else:
               inline_list.append(soup.select(card_css.format(i))[3].string.strip())
                                  
            if soup.select(att_css.format(i))[-1].string.strip() == "":
               inline_list.append("NOTFULL") #append NA to indicate not the full day
            else:
               inline_list.append(soup.select(att_css.format(i))[-1].string.strip())
            #print inline_list
            inline_list_data=json.dumps(inline_list,ensure_ascii=False,encoding="gb2312")
            print inline_list_data
            p = re.compile('.+?"(.+?)"',re.S)
            shift_time = p.findall(inline_list_data)[1]
            card_time = p.findall(inline_list_data)[2]
            full_day = p.findall(inline_list_data)[3]
            if full_day == "NOTFULL":
               print "Not full day"
            if(card_time == "CAR_NA"):
               print "No card info"
            card_time_split  = card_time.split(',')
            card_time_split_cunt = len(card_time_split)
            #card_time_split_json =  json.dumps(p.findall(,ensure_ascii=False,encoding="gb2312")
            #打开的时间 不需要显示
            #for i in range(len(card_time_split)):
            #    print card_time_split[i]
            #7:50-11:30,12:30-16:15
            morning_time =  '07:52'#shift_time[10:14]
            noon_break_time = '11:30'
            noon_on_time = '12:30'#shift_time[21:26]
            off_time = '16:15'#shift_time[27:len(shift_time)-1]
          
            morning_time  = datetime.datetime.strptime(morning_time,'%H:%M')
            noon_break_time  = datetime.datetime.strptime(noon_break_time,'%H:%M')
            noon_on_time  = datetime.datetime.strptime(noon_on_time,'%H:%M')
            off_time  = datetime.datetime.strptime(off_time,'%H:%M')
            
            morning_flag = 0
            noon_flag = 0
            off_flag = 0
            for i in range(len(card_time_split)):
                car_time = datetime.datetime.strptime(card_time_split[i],'%H:%M')
                if(car_time < morning_time):
                   morning_flag += 1

            if morning_flag == 0:
               print "Submit morning time!"
           
            
            if morning_flag > 1:
               print "Found duplicate morning card info!" 

            for i in range(card_time_split_cunt):
                if(datetime.datetime.strptime(card_time_split[i],'%H:%M') > noon_break_time and datetime.datetime.strptime(card_time_split[i],'%H:%M') < noon_on_time):
                   noon_flag += 1

            if noon_flag == 0:
               print "Submit noon time!"
            if noon_flag > 1:
               print "Found duplicate noon card info!"               

            for i in range(card_time_split_cunt):
                
                if (datetime.datetime.strptime(card_time_split[i],'%H:%M') > off_time):
                    off_flag += 1

            if off_flag == 0:
               print "Submit off time!"
            if off_flag > 1:
               print "Found duplicate off card info!" 
            #print morning_time
            #print noon_break_time
            #print noon_on_time
            #print off_time
        self.__submit_absence_day_time()
        
        #for td in souptd1st:
        #    print td[0].string
        #print souptr.find_all(id='agvTable_tccell0_10')
        #date = souptd1st.next_elements

        #res_td = r'<td>(.*?)</td>'
        #m_td = re.findall(res_td,souptd1st,re.S|re.M)
        #for mm in m_td:
            #print unicode(mm,'utf-8'),  #unicode防止乱
        print ("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        #for tr in souptr
        #    print tr['title']
        self.__set__VIEWSTATE(soup)
        selected_lessons_pre_tag = soup.find('legend', text='已选课程')
        selected_lessons_tag = selected_lessons_pre_tag.next_sibling
        tr_list = selected_lessons_tag.find_all('tr')[1:]
        self.__now_lessons_number = len(tr_list)
        try:
            xq_tag = soup.find('select', id='ddl_xqbs')
            self.__base_data['ddl_xqbs'] = xq_tag.find('option')['value']
        except:
            pass
            
    def __set__VIEWSTATE(self, soup):
        __VIEWSTATE_tag = soup.find('input', attrs={'name': '__VIEWSTATE'})
        self.__base_data['__VIEWSTATE'] = __VIEWSTATE_tag['value']

    
    def __get_lessons(self, soup):
        '''
        提取传进来的soup的课程信息
        :param soup:
        :return: 课程信息列表
        '''
        lesson_list = []
        lessons_tag = soup.find('table', id='kcmcGrid')
        lesson_tag_list = lessons_tag.find_all('tr')[1:]
        for lesson_tag in lesson_tag_list:
            td_list = lesson_tag.find_all('td')
            code = td_list[0].input['name']
            name = td_list[1].string
            teacher_name = td_list[3].string
            Time = td_list[4]['title']
            number = td_list[10].string
            lesson = self.Lesson(name, code, teacher_name, Time, number)
            lesson_list.append(lesson)
        return lesson_list

    def __search_lessons(self, lesson_name=''):
        '''
        搜索课程
        :param lesson_name: 课程名字
        :return: 课程列表
        '''
        self.__base_data['TextBox1'] = lesson_name.encode('gb2312')
        data = self.__base_data.copy()
        data['Button2'] = '确定'.encode('gb2312')
        request = self.session.post(self.__headers['Referer'], data=data, headers=self.__headers)
        soup = BeautifulSoup(request.text, 'lxml')
        self.__set__VIEWSTATE(soup)
        return self.__get_lessons(soup)

    def __select_lesson(self, lesson_list):
        '''
        开始选课
        :param lesson_list: 选的课程列表
        :return: none
        '''
        data = copy.deepcopy(self.__base_data)
        data['Button1'] = '  提交  '.encode('gb2312')
        for lesson in lesson_list:
            code = lesson.code
            data[code] = 'on'
        request = self.session.post(self.__headers['Referer'], data=data, headers=self.__headers)
        soup = BeautifulSoup(request.text, 'lxml')
        self.__set__VIEWSTATE(soup)
        error_tag = soup.html.head.script
        if not error_tag is None:
            error_tag_text = error_tag.string
            r = "alert\('(.+?)'\);"
            for s in re.findall(r, error_tag_text):
                print(s)
        print('已选课程:')
        selected_lessons_pre_tag = soup.find('legend', text='已选课程')
        selected_lessons_tag = selected_lessons_pre_tag.next_sibling
        tr_list = selected_lessons_tag.find_all('tr')[1:]
        self.__now_lessons_number = len(tr_list)
        for tr in tr_list:
            td = tr.find('td')
            print(td.string)
            



    def run(self):
        '''
        开始运行
        :return: none
        '''
        print('请输入搜索课程名字')
        lesson_name = input()
        lesson_list = self.__search_lessons(lesson_name)
        print('请输入想选的课的id，id为每门课程开头的数字,如果没有课程显示，代表公选课暂无')
        for i in range(len(lesson_list)):
            print(i, end=='')
            lesson_list[i].show()
        select_id = int(input())
        lesson_list = lesson_list[select_id:select_id + 1]
        while True:
            try:
                number = self.__now_lessons_number
                self.__select_lesson(lesson_list)
                if self.__now_lessons_number > number:
                    break
            except:
                print("抢课失败，休息0.5秒后继续")
                time.sleep(0.5)


if __name__ == '__main__':
    print('尝试登录...')
    with io.open('config.json',encoding='utf-8')as f:
        config = json.load(f)
    url = config['url']
    uid = config['student_number']
    password = config['password']
    print(uid+""+password)
    spider = Spider(url)
    if (spider.login(uid, password)):
        spider.run()
    os.system("pause")
