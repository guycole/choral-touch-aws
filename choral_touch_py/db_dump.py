#! /usr/bin/python
#
# Title:db_dump.py
# Description:dump choral touch and write to AWS S3
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import datetime
import os
import sys
import time
import uuid
import yaml

import boto3
import botocore

#from boto.s3.connection import S3Connection
#from boto.exception import S3ResponseError
#from boto.s3.key import Key


class DumpDriver:

    def execute(self, task_id):
        start_time = time.time()

        dump_name = "touch-%d-%2.2d-%2.2d.sql.gz" % (datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
        dump_path = "%s/%s" % (snapshot_dir, dump_name)
        command = "%s -u %s -p%s %s | %s > %s" % (dump_command, mysql_username, mysql_password, mysql_database, gzip_command, dump_path)
        print command
        os.system(command)

        s3bucket_name = 'dbdump.braingang.net'
        s3file_name = "%s/%s" % (s3bucket_name, dump_name)

        s3 = boto3.resource('s3')
        s3.Object(s3bucket_name, dump_name).put(Body=open(dump_path, 'rb'))

        os.unlink(dump_path)

        stop_time = time.time()
        duration = stop_time - start_time

        return duration

print 'start'

#
# argv[1] = configuration filename
#
if __name__ == '__main__':
    if len(sys.argv) > 1:
        yamlFileName = sys.argv[1]
    else:
        yamlFileName = 'config.yaml'

    configuration = yaml.load(file(yamlFileName))

    dump_command = configuration['dumpCommand']
    gzip_command = configuration['gzipCommand']
    rm_command = configuration['rmCommand']

    snapshot_dir = configuration['snapShotPath']

    mysql_username = configuration['mySqlDumpUserName']
    mysql_password = configuration['mySqlDumpPassWord']
    mysql_hostname = configuration['mySqlDumpHostName']
    mysql_database = configuration['mySqlDumpDataBase']

    driver = DumpDriver()
    duration = driver.execute(uuid.uuid4)

    log_message = "DumpDriver end w/duration:%d" % duration
    print log_message

print 'stop'
