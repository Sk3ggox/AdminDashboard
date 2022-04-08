import logging
from tkinter import Tk, Label
import mysql.connector

#Neat logging package
def logFunc():
    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)

#Create tkinter main window
root = Tk()

#Create header labels and title
def createWindow():
    root.title('DataDisplay')
    Label(root,text='Entry ID',width=20).grid(row=0,column=0)
    Label(root,text='Host',width=20).grid(row=0,column=1)
    Label(root,text='CPU',width=20).grid(row=0,column=2)
    Label(root,text='RAM',width=20).grid(row=0,column=3)
    Label(root,text='Disk',width=20).grid(row=0,column=4)

#Declare self-repeating function
def clock():
    #Initiate database connection
    db = mysql.connector.connect(
    host="192.168.1.3",
    user="testuser",
    password="test1234",
    database="dashboard"
    )
    cur = db.cursor()
    #Execute SQL query to fetch last entry of each device (corrected because syntax mistake...)
    cur.execute('''SELECT entry_id,hostname,cpu_load,ram_load,disk_usage FROM `dashboard` WHERE entry_id IN ( SELECT MAX(entry_id) FROM dashboard GROUP BY hostname); ''')
    t_set = cur.fetchall()
    logging.debug(f"Fetched Data from db - {t_set}")
    #Make adding devices dynamic (e.g. when a new device gets stored in db, show on new row)
    i=1
    for row in t_set:
        for j in range(len(row)):
            e = Label(root, width=20, text=row[j])
            #Add new row. Adapt col to current item
            e.grid(row=i, column=j)
            #Check if float, add % for clarity and change bg to warn admin of problems
            if isinstance(row[j], float):
                e["text"] = str(row[j]) + '%'
                if row[j] > 95:
                    e["background"] = "red"
                elif row[j] < 95 and row[j] > 85:
                    e["background"] = "orange"
                elif row[j] < 85 and row[j] > 75:
                    e["background"] = "yellow" 
        i=i+1
    cur.close()
    db.close()
    #Repeat function every 1 sec
    root.after(1000, clock)

#Main loop containing all functions
def main():
    logFunc()
    createWindow()
    clock()
    root.mainloop()

#Check if this is a script or lib
if __name__ == '__main__':
    main()