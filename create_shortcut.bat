@echo off

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

'strDesktop = WshShell.SpecialFolders("Desktop")
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%

echo sLinkFile = "%USERPROFILE%\Desktop\DA_SkypeManager.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%CD%\python-3.9.7\pythonw.exe" >> %SCRIPT%
echo oLink.Arguments = """%CD%\main.py""" >> %SCRIPT%
echo oLink.WorkingDirectory = "%CD%"  >> %SCRIPT%
echo oLink.IconLocation = "%CD%\logos\title.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%