cd %HOMEPATH%
cd Doccuments
cd micronPro-worker
pip install virtualenv
virtualenv env
CALL .\env\Scripts\activate.bat
pip install -r requirements.txt
PAUSE
