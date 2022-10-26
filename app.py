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

cursor = mysql_connection.cursor()

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
    account = request.form["account"]  # 這是POST寫法，要把使用者在前端的資料抓進來後端，然後放進變數
    password = request.form["password"]

    if (account == "test") and (password == "test"):  # 如果說帳密都是test就回傳到(路由/member)
        # 在這一步才能把資料存到session，如果在if前面就存的話，就會連錯誤的地方都一起影響
        session["account"] = account
        session["password"] = password
        return redirect("/member")

    elif (account == "") or (password == ""):
        # 任一欄為空 就導去(路由/error)先預設message後面的文字
        return redirect("/error?message=請輸入帳號、密碼")

    else:
        # 任一欄輸入錯的話就導去(路由/error)先預設message後面的文字
        return redirect("/error?message=帳號、或密碼輸入錯誤")


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

    # 再把資料放進mysql資料庫裡

    mysql_connection.commit()

    cursor.execute(
        "SELECT username FROM membership WHERE (username='" + username + "')")
    records = cursor.fetchall()
    if records == []:
        cursor.execute("INSERT INTO membership (name, username, password) VALUES('" +
                       name + "', '" + username + "', '" + password + "')")
        return "可以註冊"
    else:
        return "不能註冊"


app.run(port=3000)


# result = cursor.fetchone()
# if not result == None:
#     return redirect("/error")
