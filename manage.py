#!/usr/bin/env python3
###########################################################
#
# This python script is used for mysql database backup
# using mysqldump and tar utility.
#
# Tested with : Python 2.7.15 & Python 3.5
# Script Revision: 1.4
#
##########################################################
 
# Import required python libraries
 
import os
import time
import pipes
from subprocess import call

def getIndex(
    _arryLi: list,
    item: str
):
    return _arryLi.index(item)
    
try:
    # MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
    # To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.

    # Read database config in EMR-API-API
    database_yml_file = open("/var/www/BHT-EMR-API/config/database.yml", "r")
    database_yml_file = database_yml_file.read().split()

    username = ''
    password = ''
    database = ''

    for item in database_yml_file:
        if (item == "username:"):
           username = (
               database_yml_file[getIndex(database_yml_file, item) + 1]
           ) 
           print("username: "+username)
        
        if (item == "password:"):
            password = (
                database_yml_file[getIndex(database_yml_file, item) + 1]
            )
            print("password: "+password)
        
        if (item == "database:"):
            database = (
                database_yml_file[getIndex(database_yml_file, item) + 1]
            )
            print("database: "+database)
        
    DB_HOST = 'localhost'
    DB_USER = username
    DB_USER_PASSWORD = password
    DB_NAME = database
    BACKUP_PATH = '/var/www/EMR-DB-BACKUP/'
    
    # Getting current DateTime to create the separate backup folder like "20180817-123433".
    DATETIME = time.strftime('%Y%m%d-%H%M%S')
    TODAYBACKUPPATH = BACKUP_PATH
    
    # Checking if backup folder already exists or not. If not exists will create it.
    try:
        os.stat(TODAYBACKUPPATH)
    except:
        os.mkdir(TODAYBACKUPPATH)
    
    # Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
    print ("checking for databases names file.")
    if os.path.exists(DB_NAME):
        file1 = open(DB_NAME)
        multi = 1
        print ("Databases file found...")
        print ("Starting backup of all dbs listed in file " + DB_NAME)
    else:
        print ("Databases file not found...")
        print ("Starting backup of database " + DB_NAME)
        multi = 0
    
    # Starting actual database backup process.
    if multi:
        in_file = open(DB_NAME,"r")
        flength = len(in_file.readlines())
        in_file.close()
        p = 1
        dbfile = open(DB_NAME,"r")
    
        while p <= flength:
            db = dbfile.readline()   # reading database name from file
            db = db[:-1]         # deletes extra line
            dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
            os.system(dumpcmd)
            gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
            os.system(gzipcmd)
            p = p + 1
        dbfile.close()
    else:
        db = DB_NAME
        dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
        os.system(dumpcmd)
        gzipcmd = "gzip -f " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
        os.system(gzipcmd)
    
    print ("")
    print ("Backup script completed")
    print ("Your backups have been created in '" + TODAYBACKUPPATH + "' directory")

    try:
        call("./Services/sync_db.sh")
    except Exception as e:
        print("error: ",e)
except Exception as e:
    print("error: ",e)