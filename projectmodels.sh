file=$(date +%Y-%m-%d).dat
models="python manage.py projectmodels"
command $models > $file