#! /usr/bin/python
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
import uuid
import yaml

from sql_table import Event

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import boto.ses

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class ChoralTouch:

    def htmlWriter(self, file_name, results):
        outfile = open(file_name, 'w')
        outfile.write('<html><body>')
        outfile.write('<h1>Choral Touch</h1>')
        outfile.write('<table>')

        for result in results:
            buffer = "<tr><td>%d/%d</td><td>%d</td><td>%s</td></tr>" % (result['month'], result['day'], result['year'], result['note'])

            outfile.write(buffer)

        outfile.write('</table>')
        outfile.write('</body></html>')
        outfile.close()

    def mailReport(self, file_name):
        message = MIMEMultipart()
        message['Subject'] = 'Choral Touch'
        message['From'] = 'Guy Cole <guycole@gmail.com>'
        message['To'] = 'guycole@gmail.com'

        html = open(file_name, 'r').read()

        attachment = MIMEText(html, 'html')
        message.attach(attachment)

        connection = boto.ses.connect_to_region('us-west-2')
        status = connection.send_raw_email(message.as_string(), source=message['From'], destinations=message['To'])

    def day_of_year(self, day, month):
        today = datetime.datetime.now()
        candidate = datetime.datetime(today.year, month, day)
        return (candidate - datetime.datetime(today.year, 1, 1)).days + 1

    def filter(self, day, month, jd_start, date_delta):
        today = datetime.datetime.now()
        if calendar.isleap(today.year):
            jd_limit = 366
        else:
            jd_limit = 365

        jd_stop = jd_start + date_delta

        jd = self.day_of_year(day, month)
        if jd_stop > jd_limit and jd < date_delta:
            # year end wrap
            jd += jd_limit

        if jd >= jd_start and jd < jd_stop:
            return jd

        return -1

    def discovery(self, jd_start, date_delta, session):
        results = []

        selected_set = session.query(Event).all()
        for selected in selected_set:
            id = selected.id
            month = selected.month
            day = selected.day
            year = selected.year
            note = selected.note

            jd = self.filter(day, month, jd_start, date_delta)
            if jd < 0:
                print "failure:%d:%s" % (id, note)
            else:
                print "success:%d:%s" % (id, note)

                flag = False
                fresh = {'jd':jd, 'id':id, 'month':month, 'day':day, 'year':year, 'note':note}
                for temp in results:
                    if jd > temp['jd']:
                        flag = True
                        results.insert(results.index(temp), fresh) 
                        break;

                if flag is False:
                    results.append(fresh)

        print len(results)
        for temp in results:
            print temp

        return results

    def execute(self, task_id):
        start_time = time.time()

        date_delta = 10

        today = datetime.datetime.now()
        jd_start = (today - datetime.datetime(today.year, 1, 1)).days + 1

        mysql_url = "mysql://%s:%s@%s:3306/%s" % (mysql_username, mysql_password, mysql_hostname, mysql_database)
        engine = create_engine(mysql_url, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        results = self.discovery(jd_start, date_delta, session)
        outfile = "%s/outmail" % (mail_dir)
        self.htmlWriter(outfile, results)
        self.mailReport(outfile)

        stop_time = time.time()
        duration = stop_time - start_time
        log_message = "stop w/duration %d" % (duration)
        print log_message

print 'start choral touch'

#
# argv[1] = configuration filename
#
if __name__ == '__main__':
    if len(sys.argv) > 1:
        yaml_filename = sys.argv[1]
    else:
        yaml_filename = 'config.yaml'

    configuration = yaml.load(file(yaml_filename))

    mail_dir = configuration['emailDir']

    mysql_username = configuration['mySqlUserName']
    mysql_password = configuration['mySqlPassWord']
    mysql_hostname = configuration['mySqlHostName']
    mysql_database = configuration['mySqlDataBase']

    driver = ChoralTouch()
    driver.execute(uuid.uuid4())

print 'stop choral touch'
