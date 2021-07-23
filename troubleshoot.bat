cd %HOMEPATH%
cd Desktop
cd micronPro-worker
pip install virtualenv
virtualenv env
pip uninstall numpy
pip install numpy --upgrade
pip install porespy
pip install -r requirements.txt
pip install -r requirements.txt
cmd \k