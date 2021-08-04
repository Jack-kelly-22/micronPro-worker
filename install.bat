cd %HOMEPATH%
cd Documents
cd micronPro-worker
python -m pip install virtualenv
virtualenv env
CALL .\env\Scripts\activate.bat
pip install -r requirements.txt
PAUSE
