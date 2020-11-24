from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText
import time
import tkinter as tk
from threading import Timer



def send_email():
    msg_from = ''  # 发送方邮箱
    passwd = ''  # 填入发送方邮箱的授权码
    msg_to = 'hizyx97@gmail.com,junkrat@qq.com,yzhou168@syr.edu'  # 收件人邮箱

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
        txt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "提醒邮件已发送至："+ msg_to
        print(txt)
        # txt_panel.insert('insert', txt + '\n')
        # txt_panel.see('end')
        # txt_panel.update()
        # print("提醒邮件已发送至：", msg_to)
    finally:
        s.quit()

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
#url="https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-15160618060.68.1ec02172QWpe7D&id=615886665551&rn=55e53f42a861a2e224dd5231be7f05ed&abbucket=12&skuId=4339622732765#"
#url="https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-15160618060.36.a54a2172DH0Y2d&id=615886665551&rn=1fc70735dc7da32f59a93e11fec4a517&abbucket=9"
# url="https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-15160618060.36.a54a2172DH0Y2d&id=615886665551&rn=1fc70735dc7da32f59a93e11fec4a517&abbucket=9&skuId=4339622732763#"

session_expire = 600
refresh_inteval = 30
wait_load = 2
act_sess =int(session_expire/refresh_inteval)
i=0







# window = tk.Tk()
#
# window.title('天猫淘宝检查库存自动下单')
#
# # 第3步，设定窗口的大小(长 * 宽)
# window.geometry('600x400')  # 这里的乘是小x
#
#
# tk.Label(window, text='有库存则下单，没库存则持续刷新', bg='red', font=('Arial', 16)).pack()
# frame = tk.Frame(window)
# frame.pack()
#
# frame_1 = tk.Frame(frame)
# frame_2 = tk.Frame(frame)
# frame_3 = tk.Frame(frame)
# frame_4 = tk.Frame(frame)
# frame_5 = tk.Frame(frame)
# frame_6 = tk.Frame(frame)
# frame_1.pack()
# frame_2.pack()
# frame_3.pack()
# frame_4.pack()
# frame_5.pack()
# frame_6.pack()
#
# tk.Label(frame_1, text='商品立即购买的链接').pack()
# ety_link = tk.Entry(frame_1, width=80)
# ety_link.pack()
#
# tk.Label(frame_2, text='间隔时间(秒), 因为有刷新和页面加载时间，建议不要低于5秒').pack()
# ety_interv = tk.Entry(frame_2, width=10)
# ety_interv.insert('insert', '5')
# ety_interv.pack()
#
# tk.Label(frame_3, text='下单成功则向如下邮箱发送确认邮件，用英文","分隔').pack()
# ety_email= tk.Entry(frame_3, width=80)
# ety_email.pack()

def main():
    timer_interval = 1
    t = Timer(timer_interval, timedTask)
    txt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "任务启动"
    print(txt)
    t.start()

def timedTask():
    # global timer_interval
    # timer_interval = int(ety_interv.get())
    shopping()
    global t
    t = Timer(timer_interval, timedTask)
    t.start()

url = "https://h5.m.taobao.com/cart/order.html?itemId=557183774959&item_num_id=557183774959&_input_charset=utf-8&buyNow=true&v=0&skuId=4529363923901&quantity=1"
def shopping():
    global i
    i+=1
    driver.get(url)
    txt=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"第"+ str(i)+ "次刷新"
    print(txt)
    try :
        driver.find_element_by_xpath('//*[@title="提交订单"]').click()
        # print("进入订单提交页面")
        txt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "进入订单提交页面"
        print(txt)
        txt_panel.insert('insert', txt + '\n')
        txt_panel.see('end')
        txt_panel.update()
        driver.find_element_by_xpath('//*[@title="提交订单"]').click()
        print("订单已提交")
        txt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "订单已提交"
        print(txt)
        txt_panel.insert('insert', txt + '\n')
        txt_panel.see('end')
        txt_panel.update()
        send_email(ety_email.get())
        t.cancel()
    except :
        txt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "暂无库存，等待再次刷新"
        print(txt)
        txt_panel.insert('insert', txt + '\n')
        txt_panel.see('end')
        txt_panel.update()

if __name__ == "__main__":
    main()

