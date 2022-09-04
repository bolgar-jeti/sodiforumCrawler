from bs4 import BeautifulSoup
import requests
import datetime
import sqlite3
import sys

def makeTable():
    global cur
    global con
    ifexist=(cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='sfcomments';").fetchone())
    #print(ifexist[0])
    if(ifexist[0]==0):
        sql_cmd="create table sfcomments (id int primary key, page int, name text, verified int, comment text, points int, date text);"
        cur.execute(sql_cmd)
    con.commit()

def getLastVoteablePage():
    global cur
    maxpage=cur.execute("select max(page) from sfcomments").fetchone()[0]
    if (maxpage==None):
        return 1
    if(maxpage<=100):
        return int(maxpage/50)
    # calculate date
    sql_cmd="SELECT max(date) FROM sfcomments"
    lastCommentDate= datetime.datetime.isoformat(datetime.datetime.fromisoformat(cur.execute(sql_cmd).fetchone()[0])-datetime.timedelta(days=3))
    sql_cmd="SELECT max(page) from sfcomments where date<='"+lastCommentDate+"'"
    print(cur.execute(sql_cmd).fetchone()[0])
    return cur.execute(sql_cmd).fetchone()[0]

def getCommentAsStr(commenttag):
    string=""
    for element in commenttag.contents:
        string += str(element)
    return string

def getLastCommentDeltatimePerPage(comments):
    date = comments[-1].find(class_="date").text.replace(",","")
    date = datetime.datetime.strptime(date,"%b %d %Y %H:%M:%S")
    delta = (datetime.datetime.now()-date).days
    return delta

def getPageForSure(url):
    sfpage = requests.get(url)
    while (sfpage.status_code!=200):
        sfpage = requests.get(url)
    if (sfpage.status_code==200):
        sfpage = sfpage.text
        sfpage = BeautifulSoup(sfpage, "html.parser")
    return sfpage

def getAcomment(bftag, page=0):
    cid = int(bftag["rel"])
    name = bftag.find("span").find("strong").text
    verified = (len(bftag.find("span").find_all(class_="verified"))) # 1 or 0
    date = bftag.find(class_="date").text.replace(",","")
    date = datetime.datetime.strptime(date,"%b %d %Y %H:%M:%S")
    comment = bftag.find(class_="innerDiv")
    comment = getCommentAsStr(comment)
    points = int(bftag.find(class_="buttons").find("b").text)
    '''
        Table scheme: id, page, name, verified, comment, points, date
    '''
    global con
    global cur
    sql="INSERT INTO sfcomments VALUES (?,?,?,?,?,?,?) ON CONFLICT (id) DO UPDATE set points="+str(points)+", page="+str(page)+""
    values=(cid, page, name, verified, comment, points, date.isoformat())
    cur.execute(sql,values)

def getAllComments():
    global con
    global cur
    maxPageNo = int(getPageForSure("https://forum.sodika.org/").find(class_="active").get_text())
    minPageNo=1
    lastPage=getLastVoteablePage()
    if (lastPage!=None):
        minPageNo = lastPage
    
    for i in range(minPageNo, maxPageNo+1):
        sfpage = getPageForSure("https://forum.sodika.org/?pageNo="+str(i))
        comments = sfpage.find_all(class_="comment")
        for comment in comments:
            getAcomment(comment, i)
        if(i % 50 == 0):
            con.commit()
            print("COMMIT WAS MADE")
        print("Page done: "+str(i))
        if (i==maxPageNo):
            print("This was last page: "+str(i))
            con.commit()
            print("COMMIT WAS MADE")
            
    print("END")
    input("press enter to exit")

con=sqlite3.connect("sodiforum.db")
cur=con.cursor()

makeTable()
getAllComments()

con.close()

