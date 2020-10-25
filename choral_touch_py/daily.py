#! /usr/bin/python3
#
# Title:choral_touch.py
# Description: anniversary reminder
# Development Environment:OS X 10.10.5/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import calendar
import datetime
import sys
import time

import boto.ses

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class ChoralTouch:

    def html_writer(self, file_name, candidates):
        with open(file_name, "wt") as out_file:
            out_file.write('<html><body>')
            out_file.write('<h1>Choral Touch</h1>')
            out_file.write('<table>')

            for current in candidates:
                out_file.write("<tr><td>%s</td></tr>" % current)

            out_file.write('</table>')
            out_file.write('</body></html>')

    def mail_report(self, file_name):
        message = MIMEMultipart()
        message['Subject'] = 'Choral Touch'
        message['From'] = 'Guy Cole <guycole@gmail.com>'
        message['To'] = 'guycole@gmail.com'

        html = open(file_name, 'r').read()

        attachment = MIMEText(html, 'html')
        message.attach(attachment)

        connection = boto.ses.connect_to_region('us-west-2')
        status = connection.send_raw_email(message.as_string(), source=message['From'], destinations=message['To'])
        print(status)

    def day_of_year(self, date_tuple):
        candidate = datetime.datetime(date_tuple[2], date_tuple[0], date_tuple[1])
        return (candidate - datetime.datetime(date_tuple[2], 1, 1)).days + 1

    def filter(self, julian_dates, raw_line):
        ndx = raw_line.find(' ')
        elements = raw_line[:ndx].split('/')
        date_tuple = (int(elements[0]), int(elements[1]), int(elements[2]))
        doy = self.day_of_year(date_tuple)

        if doy in julian_dates:
            return True

        return False

    def execute(self, data_file_name):
        start_time = time.time()

        date_delta = 10
        julian_dates = []

        today = datetime.datetime.now()
        for ndx in range(date_delta):
            next_day = today + datetime.timedelta(days=1)
            date_tuple = (next_day.month, next_day.day, next_day.year)
            julian_dates.append(self.day_of_year(date_tuple))
            today = next_day

        candidates = []
        with open(data_file_name, 'rt') as in_file:
            for raw_line in in_file:
                if raw_line.startswith('#'):
                    continue

                if self.filter(julian_dates, raw_line) is True:
                    candidates.append(raw_line.strip())

        out_mail = "/tmp/out_mail"
        self.html_writer(out_mail, candidates)
        self.mail_report(out_mail)

        stop_time = time.time()
        duration = stop_time - start_time
        log_message = "stop w/duration %d" % duration
        print(log_message)

print('start choral touch')

#
# argv[1] = configuration filename
#
if __name__ == '__main__':
    if len(sys.argv) > 1:
        yaml_filename = sys.argv[1]
    else:
        yaml_filename = 'config.yaml'

#    with open(yaml_filename, 'r') as stream:
#        try:
#            configuration = yaml.load(stream)
#        except yaml.YAMLError as exc:
#            print(exc)

#    configuration = yaml.load(file(yaml_filename))
#
#    mail_dir = configuration['emailDir']
#
    driver = ChoralTouch()
    driver.execute('/var/choral/touch/choral_touch.dat')
#    driver.execute('/Users/gsc/IdeaProjects/choral-touch-aws/choral_touch.dat')


print('stop choral touch')
