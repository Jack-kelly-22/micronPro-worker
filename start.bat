cd %HOMEPATH%
cd OneDrive
cd micronPro-worker
CALL .\env\Scripts\activate.bat
set FLASK_APP=worker.py
python -m flask run --host=0.0.0.0 --port=5080

