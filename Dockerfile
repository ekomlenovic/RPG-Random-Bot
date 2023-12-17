FROM python:3.10

WORKDIR /app

COPY requirements.txt .
COPY main.py .
COPY bot/ /app/bot/
COPY lang/ /app/lang/

RUN pip install --no-cache-dir -r requirements.txt

ENV BOT_TOKEN=Your_Bot_Token_Or_Ask_Me_For_It \
    BOT_PREFIX=! \
    BOT_MIN=1 \
    BOT_ROLE=The_Role_Optionnal_if_you_have_admin_permission

CMD ["python", "main.py"]
