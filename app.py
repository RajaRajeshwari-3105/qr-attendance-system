from flask import Flask, request
import mysql.connector
import qrcode
import uuid

app = Flask(__name__)

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="qr_attendance"
)
cursor = conn.cursor()

# Teacher → Generate QR
@app.route('/generate')
def generate():
    session_id = str(uuid.uuid4())

    url = f"http://192.168.230.21:5000/mark?session={session_id}"

    img = qrcode.make(url)
    img.save("qr.png")

    return f"""
    <h2>QR Generated</h2>
    <p>Session: {session_id}</p>
    <img src="/qr.png">
    """

# Student → Scan QR
@app.route('/mark')
def mark():
    session = request.args.get('session')

    return f'''
    <h3>Mark Attendance</h3>
    <form method="post" action="/submit">
        Reg No: <input name="reg"><br><br>
        <input type="hidden" name="session" value="{session}">
        <input type="submit" value="Submit">
    </form>
    '''

# Save attendance
@app.route('/submit', methods=['POST'])
def submit():
    reg = request.form['reg']
    session = request.form['session']

    cursor.execute(
        "INSERT INTO attendance (reg_no, session_id) VALUES (%s, %s)",
        (reg, session)
    )
    conn.commit()

    return "✅ Attendance Marked"

# Show QR image
@app.route('/qr.png')
def qr():
    from flask import send_file
    return send_file("qr.png", mimetype='image/png')

app.run(debug=True, host='0.0.0.0')