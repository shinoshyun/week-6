from re import template
import re
from unicodedata import name
from flask import Flask, request, render_template, redirect, session
from flask import url_for

import mysql.connector
mysql_connection = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='dumplings67',
    database='member_data'
)
cursor = mysql_connection.cursor(buffered=True)


app = Flask(__name__, static_folder="static",
            static_url_path="/")  # __name__ 代表目前執行的模組

app.secret_key = "any string but secret"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/member")
def member():
    if "account" and "password" in session:  # 如果account、password有在session裡
        account = session.get("account")
        password = session.get("password")
        return render_template("member.html", account=account)
        # return username + "，歡迎登入系統"

    else:  # 沒有的話就會被導到首頁
        return redirect("/")


@app.route("/error")
def error():
    message = request.args.get("message", "")
    # 這是GET寫法，("message"代表網址後面的接的 EX:/error?message= , 後面的文字為預設文字(也可帶入數字))
    return render_template("error.html", message=message)
    # 後面的message可根據前端的message打了甚麼而做改變


@app.route("/signin", methods=["POST"])
def signin():
    account = request.form["account"]
    password = request.form["password"]

    check = "SELECT * FROM membership WHERE username = %s and password = %s"
    check_val = (account, password)
    cursor.execute(check, check_val)

    records = cursor.fetchall()
    # return records
    if records == []:
        return redirect("/error?message=帳號或密碼輸入錯誤")

    else:
        check = "SELECT id, name FROM membership"

        records = cursor.fetchall()
        for r in records:
            print(r)
    # for i in records:
    #     print(i)
    # session["name"] = name
    # session["username"] = username

    # return redirect("/member")


@app.route("/signout")
def signout():
    session.clear()
    # del session["account"]  # 登出以後就會完全的刪除資料，利用del把存在session裡的資料刪除
    # del session["password"]
    return redirect("/")


@app.route("/signup", methods=["POST"])
def signup():
    # 把html的資料放進python內
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]

    check = "SELECT * FROM membership WHERE username = %s"
    check_val = (username,)
    cursor.execute(check, check_val)

    records = cursor.fetchall()
    if records == []:
        insertCommand = "INSERT INTO membership (name, username, password) VALUES(%s, %s, %s)"

        insert = (name, username, password)

        cursor.execute(insertCommand, insert)

        # 有資安問題的做法
        # cursor.execute("INSERT INTO membership(name, username, password)VALUES('" +
        #                name + "','" + username + "','" + password + "')")

        mysql_connection.commit()

        return redirect("/")

    else:
        return redirect("/error?message=帳號已經被註冊")


app.run(port=3000)


# result = cursor.fetchone()
# if not result == None:
#     return redirect("/error")
