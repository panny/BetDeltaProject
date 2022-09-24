# uwsgi --socket 0.0.0.0:8050 --protocol=http -w wsgi:server --enable-threads
# uwsgi --socket 0.0.0.0:8050 --protocol=http -w wsgi:app --enable-threads
nohup uwsgi --socket 0.0.0.0:60288 --protocol=http -w testing_middleware2:app --enable-threads &
