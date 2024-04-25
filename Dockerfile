# 使用官方Python镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录为 /app
WORKDIR /app

# 复制 requirements.txt 文件到容器中
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制脚本文件到容器中
COPY whmcswatchdog.py .

# 提示Docker这些环境变量将由外部配置
ENV TELEGRAM_BOT_TOKEN=
ENV TELEGRAM_CHAT_ID=
ENV SERVERCHAN_KEY=
ENV PRODUCT_URL=

# 容器启动时执行Python脚本
CMD ["python", "./whmcswatchdog.py"]
