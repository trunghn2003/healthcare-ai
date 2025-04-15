@echo off
echo Khoi dong Healthcare AI System...
echo.

REM Dam bao cac thu muc shared ton tai
if not exist shared\models mkdir shared\models
if not exist shared\utils mkdir shared\utils

REM Khoi dong voi Docker Compose
docker-compose up --build

echo.
echo Luu y: Nhan Ctrl+C va sau do nhan Y de dung he thong.
