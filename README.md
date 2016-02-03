# letsencrypt_cert_check
This is simple python scrypt to check letsencrypt certificate end date and send notification email to you.

## System requirements
- openssl
- python
- letsencrypt

## Usage

1) Edit basic variables at the top of the script:
```
softline = 10
deadline = 2
email_receivers = ['sprokhorov@example.com', 'user1@example.com']
cert_path = '/etc/letsencrypt/live/'
```
2) Add a cron record for a user with read rules on `/etc/letsencrypt/live/` directory:
```
0 10 * * * python /root/letsencrypt_cert_check.py
```
