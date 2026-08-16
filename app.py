"""
app.py — נקודת הכניסה של השרת.
כאן מגדירים את אפליקציית Flask ואת כל ה-routes.
פונקציות העזר לא נכתבות כאן — הן נמצאות ב-helpers.py ומיובאות לכאן.

בנה את הקובץ הזה לפי ההנחיות במסמכי docs/, שלב אחר שלב.
"""

from flask import Flask, jsonify

app = Flask(__name__)

#ראוט בסיסי
@app.route('/', methods=['GET'])
def home():
    return jsonify({ "status": "server is running" })

#שממות פרשות
@app.route('/parshiot', methods=['GET'])
def get_parshiot():
    return jsonify(["Bereshit", "Noach", "Lech_Lecha"])

#רשימת וורטים קבועה של פרשה כלשהיא
@app.route('/parshiot/<parsha>/vortim', methods=['GET'])
def get_vortim_by_parsha(parsha):
    return jsonify([
        {"id": "vort_01", "title": f"Vort 1 for {parsha}"},
        {"id": "vort_02", "title": f"Vort 2 for {parsha}"}
    ])

#וורט בודד קבוע
@app.route('/parshiot/<parsha>/vortim/<vort_id>', methods=['GET'])
def get_single_vort(parsha, vort_id):
    return jsonify({
        "id": vort_id,
        "parsha": parsha,
        "title": "A Great Vort",
        "author": "Rabbi",
        "text": "This is a dummy text for the vort."
    })

#שם פרשה קבוע
@app.route('/current', methods=['GET'])
def current_parsha():
    return jsonify({"current_parsha": "Bereshit"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


