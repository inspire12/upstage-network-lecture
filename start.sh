#!/bin/bash
set -e

export PATH="$HOME/.local/bin:$PATH"

# FastAPI 서버 시작 스크립트
# 기존 프로세스 종료 (PID 파일 사용)
echo "Stopping existing processes..."
if [ -f app.pid ]; then
  PID=$(cat app.pid)
  if ps -p $PID > /dev/null; then
    echo "Stopping process $PID"
    kill $PID
  fi
  rm -f app.pid
else
  echo "No PID file found"
fi

# 새 서버 시작
echo "Starting FastAPI server..."
nohup uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload > app.log 2>&1 &

# 프로세스 ID 저장
echo $! > app.pid

echo "FastAPI server started with PID: $(cat app.pid)"
echo "Logs: tail -f app.log"
echo "Health check: curl http://localhost:8000/hello"
