from flask import Flask, request, render_template, jsonify
import httpx
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')  # ⚠ 在 Render 設定環境變數
user_points = {}  # 簡單用字典記錄分數

@app.route('/')
def home():
    return render_template('webapp.html')

@app.route('/webapp')
def webapp():
    user_id = request.args.get('user_id', '0')
    return render_template('webapp.html', user_id=user_id)

@app.route('/reward', methods=['POST'])
def reward_user():
    data = request.get_json()
    user_id = int(data['user_id'])
    user_points[user_id] = user_points.get(user_id, 0) + 5

    try:
        message = f"🎉 已通过看广告获得代币！ 目前代币总额 : {user_points[user_id]}"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": user_id, "text": message}
        httpx.post(url, data=payload)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
