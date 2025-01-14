#!/bin/bash

# 检查并激活 Python 虚拟环境
if [ -d "backend/venv" ]; then
    source backend/venv/bin/activate
else
    echo "Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# 安装前端依赖（如果需要）
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# 启动应用
npm run dev 