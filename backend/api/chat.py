from flask import jsonify, request
import os
import requests

def init_chat_routes(app):
    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
            if not DEEPSEEK_API_KEY:
                return jsonify({"error": "API key not configured"}), 500
                
            # 获取请求数据
            data = request.get_json()
            if not data or 'message' not in data:
                return jsonify({"error": "No message provided"}), 400

            # Deepseek API 配置
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
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
                error_message = f"DeepSeek API error: {response.text}"
                print(error_message)
                return jsonify({"error": error_message}), 500

            response_data = response.json()
            return jsonify({
                "message": response_data['choices'][0]['message']['content']
            }), 200
            
        except Exception as e:
            print(f"Error in chat endpoint: {str(e)}")  # 添加错误日志
            return jsonify({"error": str(e)}), 500 