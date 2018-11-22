#!/bin/bash
mongod --fork --logpath /tmp/mongo
exec python3 -u truncateOS.py