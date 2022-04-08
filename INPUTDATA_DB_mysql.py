import psutil
import socket
import mysql.connector
import logging

#Neat logging package
def logFunc():
    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)

db = mysql.connector.connect(
  host="192.168.1.3",
  user="testuser",
  password="test1234",
  database="dashboard"
)
qry="insert into dashboard (hostname,cpu_load,ram_load,disk_usage) values(%s,%s,%s,%s);"

def getSystemInfo():
    global HOSTNAME, CPU_LOAD, RAM_LOAD, DISK_USAGE
    HOSTNAME=socket.gethostname()
    CPU_LOAD=psutil.cpu_percent(4) 
    RAM_LOAD=psutil.virtual_memory()[2]
    DISK_USAGE=psutil.disk_usage('/').percent
    logging.info(f'SysInfo fetched - {HOSTNAME} - {CPU_LOAD} - {RAM_LOAD} - {DISK_USAGE}')

def sendData():
    try:
        cur=db.cursor()
        cur.execute(qry,('BOB-PC',CPU_LOAD,RAM_LOAD,DISK_USAGE))
        db.commit()
        logging.info('Data Inserted Successfully')
    except ValueError:
        logging.info('Someting went wrong committing to database')
        db.rollback()

def main():
    logFunc()
    while True:
        getSystemInfo()
        sendData()

if __name__ == '__main__':
    main()