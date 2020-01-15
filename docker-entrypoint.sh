#!/bin/sh
export SECRET_KEY=${SECRET_KEY:-$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c50)}

export SMTP_PORT=${SMTP_PORT:-587}
export SMTP_HOST=${SMTP_HOST:-smtp.mydomain.tld}
export SMTP_LOGIN=${SMTP_LOGIN:-mymaillogin}
export SMTP_PWD=${SMTP_PWD:-mymailpassword}
export SMTP_STARTTLS=${SMTP_STARTTLS:-True}

if [ ! -f /data/config.py ]; then
    echo "generate new config file"
    cp /app/config.py.sample /data/config.py
    sed -i "s/secretKey/${SECRET_KEY}/g" /data/config.py
    sed -i "s/smtpHost/${SMTP_HOST}/g" /data/config.py
    sed -i "s/smtpPort/${SMTP_PORT}/g" /data/config.py
    sed -i "s/smtpLogin/${SMTP_LOGIN}/g" /data/config.py
    sed -i "s/smtpPwd/${SMTP_PWD}/g" /data/config.py
    sed -i "s/smtpStartTls/${SMTP_STARTTLS}/g" /data/config.py
else
    echo "config file already exists"
fi

if [ -f /app/config.py ]; then
    rm -f /app/config.py
    ln -s /data/config.py /app/config.py
fi

export FLASK_APP=app
cat /app/config.py

flask db init
flask db migrate
flask db upgrade

if [ ! -f /data/db.sqlite ]; then
    mv /app/db.sqlite /data/db.sqlite
fi

rm -f /app/db.sqlite
ln -s /data/db.sqlite /app/db.sqlite

if [ ! -d /data/migrations ]; then
    mv /app/migrations /data/migrations
fi
rm -f /app/migrations
ln -s /data/migrations /app/migrations


python -m server



