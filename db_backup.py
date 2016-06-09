#!/usr/bin/python

#Written in Python 3.5 by Kurtis Mackey

"""
====================================================================
>>WELCOME TO THE DATABASE BACKUP AND RESTORATION SCRIPT v.0.0.1<<

  NOTE 1: IF NO DIRECTORY IS STATED IN COMMANDS,
          BACKUP WILL BE STORED IN SAME DIRECTORY
        
  NOTE 2: A GIVEN PATHWAY MUST ALREADY EXIST
          THIS PROGRAM WILL NOT CREATE A NEW DIRECTORY

  NOTE 3: A GIVEN PATHWAY MUST NOT HAVE SPACES WHEN EXECUTING
          FROM THE COMMAND LINE
            EX1:  C:\test folder\test.db  - FAIL
            EX2:  C:\test_folder\test.db  - OK

  NOTE 4: THE DATABASE FILE MUST BE .DB EXTENSION
  
  NOTE 5: THE BACKUP FILE MUST BE .SQL EXTENSION

====================================================================
PLEASE MAKE THE SEE THE FOLLOWING FOR VALID COMMANDS:

  TO BACKUP AN EXISTING DATABASE,
  RUN THIS COMMAND FROM THE COMMAND PROMPT:
  > db_backup.py backup database_name.db backup_name.sql

  TO RESTORE A DATABASE FROM AN EXISTING BACKUP,
  RUN THIS COMMAND FROM THE COMMAND PROMPT:
    EX1:  > db_backup.py restore backup_name.sql database_name.db
    EX2:  > db_backup.py restore C:\test_dir\test.sql C:\test_dir2\test.db
    
====================================================================
"""

import sqlite3
import sys
import re
import os.path


ARGUMENT_2 = sys.argv[2]
ARGUMENT_3 = sys.argv[3]

db_check = re.compile(r'^.*.db$')
sql_check = re.compile(r'^.*.sql$')


def backup():
  """ Given Two Command Line Arguments, backup the database.
  sys.argv[2] == Database file name to backup
  sys.argv[3] == Backup DB File Name
  Run Script from CMD as follows:
    db_backup.py backup database_name.db backup_name.sql
  """
  db_file = ARGUMENT_2
  if not os.path.exists(db_file):
    raise Exception('DATABASE FILE DOES NOT EXIST!')
  
  db_test = db_check.search(db_file)
  if not db_test:
    raise AttributeError('THE SECOND ARGUMENT MUST BE A .DB FILE!')

  sql_file = ARGUMENT_3
  sql_test = sql_check.search(sql_file)
  if not sql_test:
    raise AttributeError('THE THIRD ARGUMENT MUST BE A .SQL FILE!')
  
  print('>>Beginning Backup Process<<')
  print('..Connecting to Database')
  start_db = sqlite3.connect(db_file)

  print('..Creating Empty Backup File')
  with open(sql_file, 'w') as backup:
    print('..Database --> Backup    (Please Wait)')
    for line in start_db.iterdump():
      backup.write(line)
  print('..Closing Backup')

  print('..Closing Database')
  start_db.close()
  print('>>Backup Completed!<<')



def restore():
  """ Given Two Command Line Arguments, restore a database from a backup file.
  sys.argv[2] == Backup DB File Name
  sys.argv[3] == Restored DB File
  Run Script from CMD as follows:
    db_backup.py restore backup_name.sql database_name.db
  """
  sql_file = ARGUMENT_2
  sql_test = sql_check.search(sql_file)
  if not sql_test:
    raise AttributeError('THE SECOND ARGUMENT MUST BE A .SQL FILE!')

  db_file = ARGUMENT_3
  db_test = db_check.search(db_file)
  if not db_test:
    raise AttributeError('THE THIRD ARGUMENT MUST BE A .DB FILE!')

  print('>>Beginning Restoration Process<<')
  print('..Creating New Database')
  new_db = sqlite3.connect(db_file)
  new_cur = new_db.cursor()

  print('..Reading Backup File')
  with open(sql_file, 'r') as backup:
    print('..Backup --> New Database    (Please Wait)')
    try:
      new_cur.executescript(backup.read())
    except:
      raise Exception('ERROR:  DATABASE TABLE ALREADY EXISTS!')
  print('..Closing Backup')

  print('..Closing Database')
  new_db.commit()
  new_cur.close()
  new_db.close()
  print('>>Restoration Completed!<<')
  

if __name__ == '__main__':
    print()  # Creates a break on the Command Line for readability.

    # Allows for the first argument to be a function
    globals()[sys.argv[1]]()  

  
  

