@echo off

echo Cleaning old containers...
for /f "tokens=*" %%i in ('docker ps -q') do docker stop %%i

echo Starting new container...
docker run -d -p 5000:5000 interview-chatbot

timeout /t 3

start http://localhost:5500