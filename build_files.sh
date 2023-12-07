# build_files.sh
pip install -r requirements.
#make migrations
python manage.py migrate
python manage.py collectstatic