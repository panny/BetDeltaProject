Start Docker
docker-compose up

Stop Docker
docker-compose stop

Remove Docker
docker rmi -f $(docker images -qf dangling=true)

