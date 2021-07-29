gunicorn --certfile /etc/letsencrypt/live/www.maniminteractiveserver.com/fullchain.pem --keyfile /etc/letsencrypt/live/www.maniminteractiveserver.com/privkey.pem -b 0.0.0.0:5000 -w 8 app:app
