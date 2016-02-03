import os
import subprocess
import time
import smtplib

softline = 10
deadline = 2
email_receivers = ['sprokhorov@example.com']
cert_path = '/etc/letsencrypt/live/'


def mail_send(subject, message, level):
    subject = level + ': ' + subject
    msg_from = 'Letsencrypt'
    msg_to = 'Administrator'
    msg_body = 'From: {0}\n' \
        'To: {1}\n' \
        'Subject: {2}\n\n' \
        '{3}\n'.format(msg_from, msg_to, subject, message)
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(msg_from, email_receivers, msg_body)
        # print "Successfully sent email"
    except SMTPException:
        # print "Error: unable to send email"


def cert_check(cert, domain):
    if os.path.isfile(cert):
        try:
            #end_date = 'May  3 08:28:00 2015 GMT'
            end_date = subprocess.check_output(
                'openssl x509 -enddate -noout -in ' + cert, shell=True).replace('\n', '').split('=')[1]
            end_date_unix_time = subprocess.check_output(
                'date -d "' + end_date + '" +%s', shell=True).replace('\n', '')
        except subprocess.CalledProcessError:
            print 'Cant run shell'
        days_left = (int(end_date_unix_time) - int(time.time())) / 86400
        if days_left <= softline and days_left > deadline:
            level = 'WARNING'
            subject = 'letsencrypt domain:{0} days left:{1}'.format(
                domain, days_left)
            message = 'Hello your letsencrypt certificate for {0} will die after {1} days.'.format(
                domain, days_left)
            mail_send(subject, message, level)
        elif days_left <= deadline and days_left > 0:
            level = 'IMPORTANT'
            subject = 'letsencrypt domain:{0} days left:{1}'.format(
                domain, days_left)
            message = 'Hello your letsencrypt certificate for {0} will die after {1} days. It\'s time to worry'.format(
                domain, days_left)
            mail_send(subject, message, level)
        elif days_left <= 0:
            level = 'CRITICAL'
            subject = 'letsencrypt domain:{0} days left:{1}'.format(
                domain, days_left)
            message = 'Hello your letsencrypt certificate for {0} is dead. Hurry up to renew it'.format(
                domain, days_left)
            mail_send(subject, message, level)
    else:
        print 'error no file ' + cert


def main():
    domains_list = os.listdir(cert_path)
    for domain in domains_list:
        cert = cert_path + domain + '/fullchain.pem'
        cert_check(cert, domain)

if __name__ == '__main__':
    main()
