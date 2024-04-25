import requests
import datetime
import time
import os
import loguru

# 配置参数
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
SERVERCHAN_KEY = os.getenv('SERVERCHAN_KEY')
PRODUCT_URL = os.getenv('PRODUCT_URL')

def check_stock(url):
    """检查商品库存状态"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return '缺貨中' not in response.text

def send_telegram_message(message):
    """通过Telegram机器人发送消息"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, json=payload)
    logger.info('Telegram response:', response.text)

def send_serverchan_message(title, message):
    """通过Server酱发送消息"""
    url = f"https://sc.ftqq.com/{SERVERCHAN_KEY}.send"
    data = {
        'text': title,
        'desp': message
    }
    response = requests.post(url, data=data)
    logger.info('Server酱 response:', response.text)

def main():

    logger.info("Start Monitoring！:-)")
    
    previous_available = False

    while True:
        stock_available = check_stock(PRODUCT_URL)

        if stock_available and not previous_available:
            message = "产品现已有货！快来购买： " + PRODUCT_URL
            send_telegram_message(message)
            send_serverchan_message("商品有货通知", message)
            previous_available = True
            logger.info('有货通知已发送')

        elif not stock_available and not previous_available:
            message = "产品已售罄。"
            #send_telegram_message(message)
            #send_serverchan_message("商品售罄通知", message)
            #previous_available = False
            #logger.info('售罄通知已发送')
            logger.info(message)

        elif not stock_available and previous_available:
            message = "已抢完,售罄通知已发送"
            send_telegram_message(message)
            #send_serverchan_message("商品售罄通知", message)
            previous_available = False
            logger.info(message)

        time.sleep(300)  # 每10分钟检查一次

if __name__ == "__main__":
    main()
