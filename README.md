# Maptool App

Quick Start
```
requirements: Vagrant and Virtualbox

git clone https://github.com/penzance/maptool.git
cd maptool
vagrant up
vagrant ssh
pip install -r maptool/requirements/local.txt --upgrade
python manage.py syncdb
python manage.py makemigrations
python manage.py migrate
python manage.py runsslserver 0.0.0.0:8000

now open a browser and enter:
https://localhost:8000/lti_tools/maptoolapp/tool_config

```

This project also contains the basic_lti_app application.
You can install this app using this url:
```
https://localhost:8000/lti_tools/basic_lti_app/tool_config
```


