# boostrap_lti

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
