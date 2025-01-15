from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import os
from dotenv import load_dotenv
from api.chat import init_chat_routes

# 加载环境变量
load_dotenv()
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

app = Flask(__name__)
CORS(app)

# 从环境变量获取API key
VALID_API_KEYS = {os.getenv('DEEPSEEK_API_KEY')}

def get_api_key():
    """从请求头或环境变量获取API key"""
    return request.headers.get('X-API-Key') or os.getenv('DEEPSEEK_API_KEY')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = get_api_key()
        if api_key and api_key in VALID_API_KEYS:
            return f(*args, **kwargs)
        return jsonify({"error": "Invalid API key"}), 401
    return decorated_function

@app.route('/api/test', methods=['GET'])
@require_api_key
def test_api():
    return jsonify({"status": "success", "message": "API working"}), 200

# 初始化聊天路由
init_chat_routes(app)

if __name__ == '__main__':
    if not VALID_API_KEYS or '' in VALID_API_KEYS:
        print("Warning: DEEPSEEK_API_KEY not set in environment variables")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 