@echo off
chcp 950
::DHCP
::01[DKP1611004]
::python D:\python\AmigoAuto\01websiteDKP1611004_0001website.py
set LOG_FILE=D:\python\AmigoAuto\execution_log.txt
python D:\python\AmigoAuto\01websiteDKP1611004_0001website.py >> %LOG_FILE% 2>&1
timeout /t 0 > nul