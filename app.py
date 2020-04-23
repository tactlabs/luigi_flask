#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, url_for, request
import math
import requests
import sqlite3
import random
from sqlite3 import Error
import os.path
import luigiLib 
import subprocess
import os
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")
file_path = os.path.join(BASE_DIR, "result.csv")
database = "database"

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/', methods=['POST','GET'])
def index():

    req_json = request.get_json()
    # url = request.values.get('url')
    # if len(url) <= 0:
    #     return error_result({"msg":"Unable to find URL param"})

    return render_template('table_single.html')

@app.route('/trigger', methods=['POST','GET'])
def trigger():
    if request.method == 'POST':
        data = request.form
        uurl = data.get('url')
        # taskId = luigiLib.tasks('https://toronto.craigslist.org/d/computers/search/sya')
        URL = 'https://toronto.craigslist.org/d/computers/search/sya'
        taskId = 'Toronto_https___toronto__760c6829a9'
        status = 'PENDING'
        result_file_path = ''
        task_status = ''
        conn = sqlite3.connect(db_path)
        task_select_sql = ''' SELECT * FROM tasks WHERE task_id  = :taskId '''
        events_select_sql = ''' SELECT * FROM task_events WHERE task_id  = :taskId '''
        task_select_obj = {
                    'taskId' : taskId
                }
        cur = conn.cursor()
        cur.execute(task_select_sql, task_select_obj)
        rows = cur.fetchall()
        print(len(rows))
        for row in rows:
            filterId = row[0]
            events_select_obj = {
                    'taskId' : int(filterId)
                }
            cur.execute(events_select_sql, events_select_obj)
            eventrows = cur.fetchall()
            print(len(eventrows))
            for eventrow in eventrows:
                status = eventrow[2]
                if (status == 'DONE'):
                    task_status = 'SUCCESS'
                    tasks = taskId.split('__')
                    if(os.path.exists(file_path)):
                        result_file_path = os.path.join(BASE_DIR, 'result_{}.csv'.format(tasks[2]))
                        os.rename('result.csv', 'result_{}.csv'.format(tasks[2]))
                    else:
                        print('error')
            
        return render_template('table_single.html', url=URL, status=status, task_status=task_status, file_path=result_file_path)
        # return luigiLib.tasks('https://toronto.craigslist.org/d/computers/search/sya')



def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)  

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    #app.debug = True;
    app.run('127.0.0.1', '4000', True)
