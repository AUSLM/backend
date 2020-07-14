#!/bin/bash

# пользователь postgresql
export PGUSER=
# адрес postgresql
export PGHOST=
# порт postgresql
export PGPORT=
# название БД в postgresql
export PGDATABASE=
# пароль пользователя postgresql
export PGPASSWORD=

# адрес приложения
export HOST=
# порт приложения
export PORT=

# Использование Active directory
export AD_USE=

# временно - линк на сервис (http(s)://адрес:порт)
export SITE_ADDR=

# почта супер-админа
export SUPER_ADMIN_MAIL=
# пароль от аккаунта супер-админа
export SUPER_ADMIN_PASSWORD=
# подтверждение регистрации по электронной почте
# 'active' для отключения подтверждения
# 'unconfirmed' для включения
export DEFAULT_USER_STATUS=

# SMTP сервер
export MAIL_SERVER=
# Порт на почтовом сервере
export MAIL_PORT=
# Логин для почтового сервера
export MAIL_USERNAME=
# Пароль от почтового сервера
export MAIL_PASSWORD=
# Адрес, который будет указан в поле From
export MAIL_DEFAULT_SENDER=
