"""
app.py — נקודת הכניסה של השרת.
כאן מגדירים את אפליקציית Flask ואת כל ה-routes.
פונקציות העזר לא נכתבות כאן — הן נמצאות ב-helpers.py ומיובאות לכאן.

בנה את הקובץ הזה לפי ההנחיות במסמכי docs/, שלב אחר שלב.
"""

from flask import Flask, jsonify
from helpers import load_vortim_for_parsha, load_single_vort, get_current_parsha
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "server is running"})


@app.route('/parshiot', methods=['GET'])
def get_parshiot():
    # כרגע רשימת הפרשות נשארת קבועה
    return jsonify(["bereshit", "noach", "lech_lecha"])


@app.route('/parshiot/<parsha>/vortim', methods=['GET'])
def get_vortim_by_parsha(parsha):
    vortim = load_vortim_for_parsha(parsha)

    if vortim is None:
        return jsonify({"error": f"Parsha '{parsha}' not found"}), 404

    return jsonify(vortim)


@app.route('/parshiot/<parsha>/vortim/<vort_id>', methods=['GET'])
def get_single_vort(parsha, vort_id):
    vort_data = load_single_vort(parsha, vort_id)

    if vort_data is None:
        return jsonify({"error": f"Vort '{vort_id}' not found in parsha '{parsha}'"}), 404

    return jsonify(vort_data)


@app.route('/current', methods=['GET'])
def current_parsha():
    parsha = get_current_parsha()
    return jsonify({"current_parsha": parsha})


@app.route('/current/vortim', methods=['GET'])
def current_parsha_vortim():
    parsha = get_current_parsha()

    vortim = load_vortim_for_parsha(parsha)

    if vortim is None:
        return jsonify({"error": f"No vortim found for current parsha '{parsha}'"}), 404

    return jsonify(vortim)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


