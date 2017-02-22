LOCAL_PORT = 5005

# create the VM
create_machine:
						docker-machine create --driver virtualbox default

# zip up all of the files from the repo in preparation of being deployed to the container
package:
						./package_api.sh

# build docker image
build:
						docker build -t spsc/template:v1 .

# run daemonized docker container
run:
						docker run -d \
							 --env "AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID)" \
							 --env "AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY)" \
							 -p $(LOCAL_PORT):80 \
							 --name template spsc/template:v1

# run interactive bash shell after starting docker container
runi:
						docker run -t -i --name template spsc/template:v1 /bin/bash

# display info about the VM, docker container, and the state of the template
info:
						docker-machine ls
						docker ps -a
						python discover.py spsc/template

# tail template logs
tail:
						docker logs -f template

# start an interactive bash shell with a running docker container
ssh:
						docker exec -it template bash

restart:
						docker stop template
						docker start template

# stop the container and remove it
clean:
						docker stop template
						docker rm template

# stop the VM and remove it
destroy:
						docker-machine kill default
						docker-machine rm default

# perform all of the steps starting with nothing
all_the_things: create_machine package build run info tail
