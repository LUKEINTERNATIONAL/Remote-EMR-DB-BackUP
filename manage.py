#!/usr/bin/env python3
from subprocess import call

try: 
    call("./Services/sync_db.sh")
except Exception as e:
    print("error: ",e)