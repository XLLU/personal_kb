from flask import jsonify, request
import requests
import json

def init_chat_routes(app):
    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.get_json()
            if not data or 'message' not in data:
                return jsonify({"error": "No message provided"}), 400

            # Deepseek API 配置
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {request.headers.get('X-API-Key')}"
            }

            # 准备发送给 Deepseek 的数据
            chat_data = {
                "messages": [
                    {"role": "user", "content": data['message']}
                ],
                "model": "deepseek-chat",
                "temperature": 0.7
            }

            # 调用 Deepseek API
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=chat_data
            )

            if response.status_code != 200:
                return jsonify({"error": "Failed to get response from Deepseek"}), 500

            response_data = response.json()
            return jsonify({
                "message": response_data['choices'][0]['message']['content']
            }), 200

        except Exception as e:
            print(f"Chat Error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500 