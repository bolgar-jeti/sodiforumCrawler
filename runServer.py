from flask import Flask, render_template, request
import sqlite3

app=Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    rows=None
    found=None
    datas=None
    if request.method=='POST':
        datas=request.form
        db=sqlite3.connect("sodiforum.db")
        cur=db.cursor()
        sql_cmd="select * from sfcomments where "
        for d in datas.keys():
            if datas[d]!="" and d not in ["date1", "comment", "date2"]:
                sql_cmd+=d+"='"+datas[d]+"' and "
        if datas["comment"]!="":                
            for word in datas["comment"].split(" "):
                sql_cmd+="comment like '%"+word+"%' and "
        if datas["date1"]!="":
            sql_cmd+="date>= '"+datas["date1"]+"' and "
        if datas["date2"]!="":
            sql_cmd+="date<= '"+datas["date2"]+"' and "
        
        sql_cmd=sql_cmd[:sql_cmd.rfind("and ")]
        sql_cmd=sql_cmd.replace("points=","points>=")
        print(sql_cmd)
        if sql_cmd!="select * from sfcomments where":
            rows=cur.execute(sql_cmd).fetchall()
            found=len(rows)
        cur.close()
    return render_template('mainpage.html',found=found, datas=datas, rows=rows) 

if __name__=="__main__":
    app.run(port=3000,debug=True)
