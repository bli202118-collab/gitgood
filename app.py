from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)

import sqlite3

from flask_bcrypt import Bcrypt


# 建立 Flask app
app = Flask(__name__)

# Session 加密金鑰
# 正式上線時不能太簡單
app.secret_key = "course_forum_secret"

# bcrypt 密碼加密工具
bcrypt = Bcrypt(app)


# 首頁
@app.route("/")
def home():

    return render_template("index.html")


# =========================
# 註冊功能
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    # 使用者送出表單
    if request.method == "POST":

        # 取得表單資料
        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]

        # 密碼加密
        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        # 連接資料庫
        conn = sqlite3.connect("database/database.db")

        cursor = conn.cursor()

        # 新增使用者
        cursor.execute("""

        INSERT INTO users (
            username,
            email,
            password
        )

        VALUES (?, ?, ?)

        """, (
            username,
            email,
            hashed_password
        ))

        # 儲存
        conn.commit()

        # 關閉資料庫
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# =========================
# 登入功能
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    # 使用者送出登入表單
    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        # 連接資料庫
        conn = sqlite3.connect("database/database.db")

        cursor = conn.cursor()

        # 找尋使用者
        cursor.execute("""

        SELECT * FROM users
        WHERE email = ?

        """, (email,))

        user = cursor.fetchone()

        conn.close()

        # 檢查使用者存在
        if user:

            # user[3] 是 password 欄位
            # bcrypt 檢查密碼
            if bcrypt.check_password_hash(
                user[3],
                password
            ):

                # Session 紀錄登入狀態
                session["user_id"] = user[0]

                session["username"] = user[1]

                session["role"] = user[4]

                return redirect("/")

    return render_template("login.html")


# =========================
# 登出
# =========================
@app.route("/logout")
def logout():

    # 清空 Session
    session.clear()

    return redirect("/")


if __name__ == "__main__":

    app.run(debug=True)