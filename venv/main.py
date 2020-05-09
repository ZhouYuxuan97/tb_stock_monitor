from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText
import time
import datetime
import tkinter as tk
from threading import Timer

# cd C:\Program Files (x86)\Google\Chrome\Application
# chrome.exe --remote-debugging-port=9222

def send_email(msg_to):
    msg_from = '491118392@qq.com'  # 发送方邮箱
    passwd = 'dfhjbbahymsibjid'  # 填入发送方邮箱的授权码
    # msg_to = 'hizyx97@gmail.com,junkrat@qq.com'  # 收件人邮箱

    subject = "[淘宝订单已生成，请尽快付款]"  # 主题
    content = "**********淘宝订单已生成，请尽快付款!**********"
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "提醒邮件已发送至："+ msg_to
        print(txt)
        txt_panel.insert('insert', txt + '\n')
        txt_panel.see('end')
        txt_panel.update()
        # print("提醒邮件已发送至：", msg_to)
    finally:
        s.quit()

chrome_options = Options()
prefs = {"profile.managed_default_content_settings.images": 2,'permissions.default.stylesheet':2}
chrome_options.add_argument("'chrome.prefs': {'profile.managed_default_content_settings.images': 2}")
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.add_argument("--disable-extensions")
chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
#url="https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-15160618060.68.1ec02172QWpe7D&id=615886665551&rn=55e53f42a861a2e224dd5231be7f05ed&abbucket=12&skuId=4339622732765#"
#url="https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-15160618060.36.a54a2172DH0Y2d&id=615886665551&rn=1fc70735dc7da32f59a93e11fec4a517&abbucket=9"
# url="https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-15160618060.36.a54a2172DH0Y2d&id=615886665551&rn=1fc70735dc7da32f59a93e11fec4a517&abbucket=9&skuId=4339622732763#"

session_expire = 600
refresh_inteval = 30
wait_load = 1
act_sess =int(session_expire/refresh_inteval)
i=0


window = tk.Tk()

window.title('天猫淘宝检查库存自动下单')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('600x400')  # 这里的乘是小x


tk.Label(window, text='先登录,有库存则下单,没库存则持续刷新', bg='grey', font=('Arial', 16)).pack()
frame = tk.Frame(window)
frame.pack()

frame_1 = tk.Frame(frame)
frame_2 = tk.Frame(frame)
frame_3 = tk.Frame(frame)
frame_4 = tk.Frame(frame)
frame_5 = tk.Frame(frame)
frame_6 = tk.Frame(frame)
frame_1.pack()
frame_2.pack()
frame_3.pack()
frame_4.pack()
frame_5.pack()
frame_6.pack()

tk.Label(frame_1, text='商品立即购买的链接').pack()
ety_link = tk.Entry(frame_1, width=80)
ety_link.pack()

tk.Label(frame_2, text='间隔时间(秒), 因为有刷新和页面加载时间，建议不要低于5秒').pack()
ety_interv = tk.Entry(frame_2, width=10)
ety_interv.insert('insert', '5')
ety_interv.pack()

tk.Label(frame_3, text='下单成功则向如下邮箱发送确认邮件，用英文","分隔').pack()
ety_email= tk.Entry(frame_3, width=80)
txt = "hizyx97@gmail.com,yzhou168@syr.edu,junkrat@11.com"
ety_email.insert('insert', "hizyx97@gmail.com,yzhou168@syr.edu,junkrat@qq.com")
ety_email.pack()



def task():
    global i
    i+=1
    txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "第" + str(i) + "次刷新"
    print(txt)
    txt_panel.insert('insert', txt + '\n')
    txt_panel.see('end')
    txt_panel.update()

url = ""
def shopping():
    global i
    i+=1
    driver.get(url)
    txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]+"第"+ str(i)+ "次刷新"
    print(txt)
    txt_panel.insert('insert', txt + '\n')
    txt_panel.see('end')
    txt_panel.update()
    time.sleep(wait_load)
    # if(i % act_sess == 0) :
    #     driver.find_element_by_id("J_SeaHdShopSearch").click()
    #     time.sleep(wait_load)
    #     driver.back()
    #     txt=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"保持session状态"
    #     print(txt)
    #     txt_panel.insert('insert', txt + '\n')
    #     txt_panel.see('end')
    #     txt_panel.update()
    try:
        driver.find_element_by_id("J_LinkBuy").click()
        time.sleep(wait_load)
        txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "已点击立即购买"
        print(txt)
        txt_panel.insert('insert', txt + '\n')
        txt_panel.see('end')
        txt_panel.update()
        try :
            driver.find_element_by_xpath('//*[@title="提交订单"]').click()
            txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "订单已提交"
            print(txt)
            txt_panel.insert('insert', txt + '\n')
            txt_panel.see('end')
            txt_panel.update()
            send_email(ety_email.get())
            cancel()
        except :
            txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "暂无库存，等待再次刷新"
            print(txt)
            txt_panel.insert('insert', txt + '\n')
            txt_panel.see('end')
            txt_panel.update()
    except:
        txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "暂无库存，等待再次刷新"
        print(txt)
        txt_panel.insert('insert', txt + '\n')
        txt_panel.see('end')
        txt_panel.update()

def seckill():
    while 1:
        global i
        i+=1
        driver.get(url)
        txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] +"第"+ str(i)+ "次刷新"
        print(txt)
        txt_panel.insert('insert', txt + '\n')
        txt_panel.see('end')
        txt_panel.update()
        time.sleep(0.3)
        driver.find_element_by_id("J_LinkBuy").click()
        time.sleep(wait_load)
        txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "已点击立即购买"
        print(txt)
        txt_panel.insert('insert', txt + '\n')
        txt_panel.see('end')
        txt_panel.update()
        try:
            # driver.find_element_by_xpath('//*[@title="提交订单"]').click()
            if driver.find_element_by_xpath('//*[@title="提交订单"]') :
                txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "订单已提交"
                print(txt)
                txt_panel.insert('insert', txt + '\n')
                txt_panel.see('end')
                txt_panel.update()
                # send_email(ety_email.get())
                txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "任务完成"
                print(txt)
                txt_panel.insert('insert', txt + '\n')
                txt_panel.see('end')
                txt_panel.update()
                break
        except :
            txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "暂无库存，等待再次刷新"
            print(txt)
            txt_panel.insert('insert', txt + '\n')
            txt_panel.see('end')
            txt_panel.update()


def timedTask_shopping():
    shopping()
    global t
    t = Timer(timer_interval, timedTask_shopping())
    t.start()

def timedTask_seckill():
    seckill()
    # global t
    # t = Timer(timer_interval, timedTask_seckill)
    # t.start()

timer_interval = 1
t=Timer(timer_interval,timedTask_shopping)

def start_shopping():
    global timer_interval
    timer_interval = int(ety_interv.get())
    global url
    url = ety_link.get()
    txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "任务启动"
    print(txt)
    txt_panel.insert('insert', txt + '\n')
    txt_panel.see('end')
    txt_panel.update()
    t = Timer(timer_interval, timedTask_shopping)
    t.start()

def start_seckill():
    # global timer_interval
    # timer_interval = int(ety_interv.get())
    # print(timer_interval)
    global url
    url = ety_link.get()
    txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "任务启动"
    print(txt)
    txt_panel.insert('insert', txt + '\n')
    txt_panel.see('end')
    txt_panel.update()
    # global t
    # t = Timer(timer_interval, timedTask_seckill)
    # t.start()
    timedTask_seckill()

def cancel():
    t.cancel()
    # send_email(ety_email.get())
def close() :
    t.cancel()
    window.destroy()


btn_start_shopping = tk.Button(frame_4, text='开始库存监控', width=10, command=start_shopping)
btn_start_shopping.pack(side='left')
btn_start_seckill = tk.Button(frame_4, text='开始秒杀', width=10, command=start_seckill)
btn_start_seckill.pack(side='left')
btn_cancel = tk.Button(frame_4, text='取消', width=10, command=cancel)
btn_cancel.pack(side='left')
btn_close = tk.Button(frame_4, text='关闭', width=10, command= close)
btn_close.pack(side='left')


txt_panel = tk.Text(frame_5, width=60, height=15)
scrollbar = tk.Scrollbar(frame_5)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
txt_panel.pack( side=tk.LEFT, fill=tk.Y)
scrollbar.config(command=txt_panel.yview)
txt_panel.config(yscrollcommand=scrollbar.set)

tk.Label(frame_6, text='Yuxuan Zhou@2020.5').pack(side='right')


txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2] + "窗体生成"
print(txt)
txt_panel.insert('insert', txt + '\n')
txt_panel.see('end')
txt_panel.update()
# 第5步，主窗口循环显示
window.mainloop()


# def shopping():
#     global i
#     i+=1
#     driver.get(url)
#     txt=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"第"+ i+ "次刷新"
#     print(txt)
#     txt_panel.insert('insert', txt + '\n')
#     txt_panel.see('end')
#     txt_panel.update()
#     if(i % act_sess == 0) :
#         driver.find_element_by_id('//*[@title="天猫Tmall.com"]').click()
#         time.sleep(wait_load)
#         driver.back()
#         txt=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"保持session状态"
#         print(txt)
#         txt_panel.insert('insert', txt + '\n')
#         txt_panel.see('end')
#         txt_panel.update()
#     driver.find_element_by_id("J_LinkBuy").click()
#     time.sleep(wait_load)
#     try :
#         driver.find_element_by_xpath('//*[@title="提交订单"]').click()
#         # print("进入订单提交页面")
#         txt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "进入订单提交页面"
#         print(txt)
#         txt_panel.insert('insert', txt + '\n')
#         # txt_panel.see('end')
#         # txt_panel.update()
#         # driver.find_element_by_xpath('//*[@title="提交订单"]').click()
#         # print("订单已提交")
#         txt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "订单已提交"
#         print(txt)
#         txt_panel.insert('insert', txt + '\n')
#         txt_panel.see('end')
#         txt_panel.update()
#         send_email(ety_email.get())
#         t.cancel()
#
#     except :
#         txt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "暂无库存，等待再次刷新"
#         print(txt)
#         txt_panel.insert('insert', txt + '\n')
#         txt_panel.see('end')
#         txt_panel.update()
#         # print("暂无库存，等待再次刷新")
