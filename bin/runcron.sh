#!/bin/bash
#
# Title:runcron.sh
#
# Description: cron job
#
# Development Environment: OS X 10.13.6
#
# Author: G.S. Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
docker run -d --rm -v /var/choral/touch:/var/choral/touch choral-touch
#