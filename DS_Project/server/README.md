**Server**

this is a project created for .

in the root folder of project do the following:

1.activate a virtualenv with python version 3
`virtualenv venv -p python3`
then activate it (in linux do  `source venv/bin/activate`)

2.`pip install -r requirements.txt`

3.`python manage.py migrate`

4.`python manage.py runserver`

5.open browser and go to localhost:8001