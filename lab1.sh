#!/bin/bash
apt install -y mariadb-client
mysql -u root -proot -h 10.5.0.3 < lab1.sql
../bin/python3 lab1.py
cat result.out