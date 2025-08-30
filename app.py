from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = "supersecret"  # cần cho session

# Key hợp lệ để login
VALID_KEY = "AKIRA-02082009"

# Đọc key từ file key.txt (mỗi dòng 1 key)
def load_keys():
    try:
        with open("key.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

# ================= HTML + CSS ================= #
login_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Login Key System</title>
  <style>
    body {font-family: Arial, sans-serif; margin: 0; background: #f3f4f6;}
    .login-box {background: white; padding: 25px; border-radius: 12px;
                box-shadow: 0px 8px 20px rgba(0,0,0,0.2); text-align: center;
                width: 320px; margin: 100px auto;}
    .login-box h2 {margin-bottom: 20px;}
    input[type="text"] {width: 100%; padding: 10px; margin: 10px 0;
                        border-radius: 8px; border: 1px solid #ccc; font-size: 14px;}
    button {width: 100%; padding: 10px; border: none; border-radius: 8px;
            background: #667eea; color: white; font-size: 16px; cursor: pointer; transition: 0.3s;}
    button:hover {background: #764ba2;}
    .error {color: red; font-weight: bold;}
  </style>
</head>
<body>
  <div class="login-box">
    <h2>🔑 Key System Login</h2>
    {% if error %}
      <p class="error">{{ error }}</p>
    {% endif %}
    <form method="POST">
      <input type="text" name="key" placeholder="Nhập key...">
      <button type="submit">Login</button>
    </form>
  </div>
</body>
</html>
"""

dashboard_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Dashboard</title>
  <style>
    body {font-family: Arial, sans-serif; margin: 0; background: #f3f4f6;}
    .navbar {background: #667eea; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center;}
    .navbar a {color: white; text-decoration: none; font-weight: bold;}
    .container {display: flex;}
    .sidebar {width: 200px; background: #2d3748; color: white; height: calc(100vh - 60px); padding-top: 20px;}
    .sidebar ul {list-style: none; padding: 0;}
    .sidebar ul li {margin: 15px 0;}
    .sidebar ul li a {color: white; text-decoration: none; padding: 10px; display: block; transition: 0.3s;}
    .sidebar ul li a:hover {background: #4a5568; border-radius: 8px;}
    .content {flex: 1; padding: 20px;}
    .keys-box {background: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);}
    .keys-box ul {list-style: none; padding: 0;}
    .keys-box ul li {padding: 5px 0; border-bottom: 1px solid #ddd;}
  </style>
</head>
<body>
  <div class="navbar">
    <h1>🔐 Key System Dashboard</h1>
    <a href="{{ url_for('logout') }}">Đăng xuất</a>
  </div>

  <div class="container">
    <div class="sidebar">
      <ul>
        <li><a href="#">🏠 Trang chủ</a></li>
        <li><a href="#">📜 Danh sách key</a></li>
        <li><a href="#">⚙️ Cài đặt</a></li>
      </ul>
    </div>

    <div class="content">
      <h2>✅ Chào mừng!</h2>
      <p>Bạn đã đăng nhập vào hệ thống quản lý Key.</p>

      <div class="keys-box">
        <h3>📜 Danh sách Key trong file</h3>
        <ul>
          {% for key in keys %}
            <li>{{ key }}</li>
          {% endfor %}
        </ul>
      </div>
    </div>
  </div>
</body>
</html>
"""

# ================= ROUTES ================= #
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        key = request.form.get("key")
        if key == VALID_KEY:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template_string(login_html, error="❌ Key không hợp lệ!")
    return render_template_string(login_html)

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    keys = load_keys()
    return render_template_string(dashboard_html, keys=keys)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
