# PAWaves

# Development
Create a virtual environment: `python -m venv ./.venvs/pawavesvenv` and activate it `source <path-to-venv>/bin/activate`.

Install requirements: `pip install -r requirements.txt`.

`cd` in the directory that contains the `manage.py` file (root). Start the web server by running `python manage.py runserver`. You can now see changes in your site by going to `http://127.0.0.1:8000/`.

When you edit any static files (i.e css, js, presets) you need to apply them with `python manage.py collectstatic`.

# Deploying
Upload code to git.

Then, in a [PythonAnywhere console](https://www.pythonanywhere.com/consoles/) run:
```
cd ~/<your-pythonanywhere-domain>.pythonanywhere.com
git pull
```

Activating your virtualenv if it's not still active from earlier (PythonAnywhere uses a command called workon to do this, it's just like the source myenv/bin/activate command you use on your own computer):

```
workon <your-pythonanywhere-domain>.pythonanywhere.com
python manage.py collectstatic
```
Then go to the ["Web" page](https://www.pythonanywhere.com/web_app_setup/) and hit Reload. Changes should now be visible.

# Todos
- [ ] Adjust to different screen sizes.