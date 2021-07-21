cd %HOMEPATH%
cd Desktop
cd micronPro-worker
CALL .\env\Scripts\activate.bat
python -m flask run --host=0.0.0.0 --port=5080

