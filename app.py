
from flask import Flask, request, jsonify, send_from_directory
import sqlite3, os
from datetime import datetime

app = Flask(__name__, static_folder="static")
DB="booking.db"

RESOURCES=["超净台1","超净台2","倒置显微镜","荧光显微镜","离心机"]

def conn():
    c=sqlite3.connect(DB)
    c.row_factory=sqlite3.Row
    return c

def init():
    c=conn()
    c.execute("""CREATE TABLE IF NOT EXISTS resources(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE)""")
    c.execute("""CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource TEXT,
        user TEXT,
        cell TEXT,
        purpose TEXT,
        start TEXT,
        end TEXT)""")
    for r in RESOURCES:
        c.execute("INSERT OR IGNORE INTO resources(name) VALUES(?)",(r,))
    c.commit()
    c.close()

@app.route("/")
def index():
    return send_from_directory("static","index.html")

@app.route("/api/resources")
def resources():
    c=conn()
    data=[dict(x) for x in c.execute("select * from resources")]
    c.close()
    return jsonify(data)

@app.route("/api/bookings")
def bookings():
    c=conn()
    data=[dict(x) for x in c.execute(
        "select * from bookings order by start")]
    c.close()
    return jsonify(data)

@app.route("/api/book",methods=["POST"])
def book():
    d=request.json
    c=conn()
    conflict=c.execute("""
    select * from bookings 
    where resource=? and start < ? and end > ?
    """,(d["resource"],d["end"],d["start"])).fetchone()
    if conflict:
        c.close()
        return jsonify({"ok":False,"msg":"该设备该时间段已预约"}),409

    c.execute("""
    insert into bookings(resource,user,cell,purpose,start,end)
    values(?,?,?,?,?,?)
    """,(d["resource"],d["user"],d["cell"],d["purpose"],d["start"],d["end"]))
    c.commit()
    c.close()
    return jsonify({"ok":True})

@app.route("/api/delete/<int:i>",methods=["DELETE"])
def delete(i):
    c=conn()
    c.execute("delete from bookings where id=?",(i,))
    c.commit()
    c.close()
    return jsonify({"ok":True})

if __name__=="__main__":
    init()
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
