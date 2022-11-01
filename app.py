from flask import Flask, request, render_template, redirect, session

# 要先把mysql和python連結在一起
import mysql.connector
mysql_connection = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='',
    database='member_data'
)
# 代表mysql:我要開始使用囉!的意思~
cursor = mysql_connection.cursor(buffered=True)


app = Flask(__name__, static_folder="static",
            static_url_path="/")  # __name__ 代表目前執行的模組

#import session的時候要使用的語法
app.secret_key = "any string but secret"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/member")
def member():
    # 如果 id 和 name 都有在session裡面
    if "id" and "name" in session:
        name = session["name"]
        return render_template("member.html", account=name)

    else:  # 沒有的話就會被導到首頁
        return redirect("/")


@app.route("/error")
def error():
    message = request.args.get("message", "")
    # 這是GET寫法，("message"代表網址後面的接的 EX:/error?message=xxxxxxx , 後面的文字為預設文字(也可帶入數字))
    return render_template("error.html", message=message)
    # 後面的message可根據前端的message打了甚麼而做改變


@app.route("/signin", methods=["POST"])
def signin():
    account = request.form["account"]
    password = request.form["password"]

    # 比對前端輸入的account和password，是不是跟mysql裡的一樣，
    # 意思就是!!!  (資料庫的username = 前端帶入後端的account) and (資料庫的password = 前端帶入後端的password)
    check = "SELECT * FROM membership WHERE username = %s and password = %s"
    check_val = (account, password)
    cursor.execute(check, check_val)

    # 用fetchone() 的話，只會搜尋出一組是不是符合的結果 (試著print的話 只會出現None or 對應的資料)
    # 意思就是!!!(前端帳密都輸入apple的話 他只會拉到符合這個資料的資訊，用fetchall() 的話，會拉出全部資料)
    records = cursor.fetchone()
    if records == None:
        return redirect("/error?message=帳號或密碼輸入錯誤")

    else:
        # 因為records是一個陣列 像是[(1),(shino), (67), (67)]，所以records[0]=1，records[1]=shino，再存到session裡面~
        session["id"] = records[0]
        session["name"] = records[1]
        return redirect("/member")


@app.route("/signout")
def signout():
    session.clear()

    return redirect("/")


@app.route("/signup", methods=["POST"])
def signup():
    # 把html的資料放進python內
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]

    check = "SELECT * FROM membership WHERE username = %s"
    check_val = (username,)  # 如果只有單個變數要放 變數後面要逗號(規定就是這樣寫~)
    cursor.execute(check, check_val)

    records = cursor.fetchall()
    # 如果records 不是[]，也有輸入name/username/password(三個只要有一個沒輸入)，就會被導到錯誤頁面
    if records != [] or (name == '') or (username == '') or (password == ''):
        return redirect("/error?message=帳號已經被註冊")

    else:
        # 把前端的變數放入mysql，因為不知道前端輸入的是甚麼，所以用%s代替
        insertCommand = "INSERT INTO membership (name, username, password) VALUES(%s, %s, %s)"
        insert = (name, username, password)  # 這是從前端拿來後端的變數，準備要放進mysql
        # cursor.execute是mysql的語法  (指令, 前端變數)
        cursor.execute(insertCommand, insert)

        # 有資安問題的做法
        # cursor.execute("INSERT INTO membership(name, username, password)VALUES('" + name + "','" + username + "','" + password + "')")

        mysql_connection.commit()
        session["username"] = username
        session["password"] = password
        return redirect("/")


app.run(port=3000)
