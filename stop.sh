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