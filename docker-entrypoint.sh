#!/bin/bash
mongod --fork --logpath /tmp/mongo
python3 truncateOS.py
mongo pythonParser