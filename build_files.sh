# build_files.sh
pip install -r requirements.txt
# make migrations
python manage.py makemigrations
python manage.py migrate


python3 manage.py collectstatic --noinput