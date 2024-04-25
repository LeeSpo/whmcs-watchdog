# 使用官方Python镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录为 /app
WORKDIR /app

# 复制 requirements.txt 文件到容器中
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制脚本文件到容器中
COPY script.py .

# 设置环境变量（实际使用时应通过Docker命令行或compose文件设置环境变量，以保护敏感信息）
ENV TELEGRAM_BOT_TOKEN=telegram_bot_token
ENV TELEGRAM_CHAT_ID=telegram_chat_id
ENV SERVERCHAN_KEY=serverchan_key
ENV PRODUCT_URL =product_url_withid


# 容器启动时执行Python脚本
CMD ["python", "./whmcswatchdog.py"]
