from flask import *
import mysql.connector

app = Flask(
    __name__,
    static_folder="static/",
    static_url_path="/"
)

#設定session 密鑰
app.secret_key= "fjehiwqdmkdn313"
# connect sql
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='website')
@app.route("/",methods=["GET", "POST"])
def index():
    return render_template("index2.html")


@app.route('/signup', methods=["POST"])
def signup():
    name = request.form['name']
    account = request.form['account']
    password = request.form['password']
    # 使用cursor方法建立指標對象
    mycursor = mydb.cursor()
    # 使用execute執行SQL檢查是否有相同名字
    mycursor.execute('SELECT * FROM member WHERE username = %s', [account])
    # 取到一筆相同的資料放進變數user
    user = mycursor.fetchone()
    if user != None:
        return redirect("/error?message=帳號已經被註冊")
    elif name == "" or account == "" or password == "":
        return redirect("/error?message=請輸入完整資訊")
    # 把資料放進資料庫
    sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
    mycursor.execute(sql, [name, account, password])
    mydb.commit()
    return redirect('/')

# 驗證系統路由 使用POST
@app.route("/signin", methods=["POST"])
def signin():
    if 'account' in request.form and 'password' in request.form:
        account = request.form['account']
        password = request.form['password']
    mycursor = mydb.cursor()
    # 使用execute執行SQL檢查是否有相同名字
    mycursor.execute('SELECT * FROM member WHERE username = %s AND password = %s', (account, password))
    user = mycursor.fetchone()
    if user:
        session['loggedin'] = True
        session['id'] = user[0]
        session['name'] = user[1]
        session['act'] = user[2]
        session['pwd'] = user[3]
        return redirect('/member')
    elif account == "" or password == "":
        return redirect("/error?message=請輸入帳號、密碼")
    else:
        return redirect("/error?message=帳號、或密碼輸入錯誤")

#成功登入頁
@app.route("/member")
def member():
    if 'act' in session and 'pwd' in session:
        return render_template("success.html", username=session['name'])
    else:
        return redirect("/")

#失敗登入頁
@app.route("/error")
def error():
    data = request.args.get('message', '發生錯誤')
    return render_template("error.html", data=data)

#成功登出頁
@app.route("/signout")
def signout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run(port=3000, debug=True)
