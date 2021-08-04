cd %HOMEPATH%
cd Doccuments
cd micronPro-worker
CALL .\env\Scripts\activate.bat
set FLASK_APP=worker
set FLASK_RUN_PORT=5080
python -m flask run --host=0.0.0.0
PAUSE

