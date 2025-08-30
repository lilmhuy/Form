from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your-secret-key"

# Key login cố định
LOGIN_KEY = "AKIRA-02082009"

# Hàm đọc file key system
def load_key_system():
    try:
        with open("key.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "⚠️ Không tìm thấy file key.txt!"

# Giao diện login
login_page = """
<!doctype html>
<html>
<head>
    <title>Login Key System</title>
    <style>
        body {font-family: Arial; background: #f3f3f3; display: flex; justify-content: center; align-items: center; height: 100vh;}
        .box {background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);}
        input {width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px;}
        button {width: 100%; padding: 10px; background: #4CAF50; border: none; color: white; border-radius: 5px; cursor: pointer;}
        button:hover {background: #45a049;}
        .error {color: red;}
    </style>
</head>
<body>
    <div class="box">
        <h2>🔑 Key Login</h2>
        <form method="POST">
            <input type="text" name="key" placeholder="Nhập key đăng nhập..." required>
            <button type="submit">Đăng nhập</button>
        </form>
        {% if error %}<p class="error">{{ error }}</p>{% endif %}
    </div>
</body>
</html>
"""

# Trang chính hiển thị key system từ file
home_page = """
<!doctype html>
<html>
<head>
    <title>Dashboard</title>
</head>
<body>
    <h1>Chào mừng ✅</h1>
    <p><b>Key System (từ file key.txt):</b></p>
    <pre>{{ key_system }}</pre>
    <a href="{{ url_for('logout') }}">Đăng xuất</a>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        key = request.form["key"]
        if key == LOGIN_KEY:
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            error = "❌ Key đăng nhập không hợp lệ!"
    return render_template_string(login_page, error=error)

@app.route("/home")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    key_system = load_key_system()
    return render_template_string(home_page, key_system=key_system)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
