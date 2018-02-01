#! /usr/bin/python
#
# Title:converter.py
# Description: convert flat file to sql
# Development Environment:OS X 10.10.5/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
# month/day (year) event
# 1/1 (2001) Happy New Year
#
import calendar
import datetime
import sys
import time
import uuid
import yaml


class Converter:

    def execute(self, file_name):
        infile = open(file_name, 'r')
        buffer = infile.readlines()
        infile.close()

        for current in buffer:
            temp = current.strip()

            ndx1 = temp.index(' ')
            ndx2 = temp.index(' ', ndx1+1)

            raw_date = temp[:ndx1].split('/')
            month = int(raw_date[0])
            day = int(raw_date[1])

            raw_year = temp[ndx1:ndx2]
            temp1 = raw_year.replace('(', ' ')
            temp2 = temp1.replace(')', ' ')
            year = int(temp2.strip())

            message = temp[ndx2+1:]

            date = "%d-%d-%d" % (year, month, day)

            output = "insert into event(month, day, year, date, note) values(%d, %d, %d, '%s', '%s');" % (month, day, year, date, message)
            print output

print 'start converter'

if __name__ == '__main__':
    file_name = 'datefairy.dat'

    driver = Converter()
    driver.execute(file_name)

print 'stop converter'
