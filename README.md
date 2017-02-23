# python-template
A Python Flask aplication that utilizes Docker, Nginx, and Supervisor to ensure stability and compartmentalization. Connects to oracle database. Template for API development.

### How to use this template for your own application
1. Clone or download the repository as a zip file locally
2. Copy the contents into your own git repository
3. Replace instances of 'template' with whatever you want your app to be named in folder names, file names, and file contents
4. Start developing your Flask application inside app.py!

### Building and running locally in docker
Run 'make clean package build runi tail' (use 'run' instead of 'runi' if you don't want an interactive session, only use 'clean' if you need to clean a previous build)

### What does the Makefile actually do?
- Cleans any old docker containers using `docker stop` and `docker rm`
- Packages your application into a nice .zip file through the use of a custom bash script
    - The bash script ignores files that aren't necessary for building/running
- Builds the docker container using the Dockerfile, which does the following:
    - Installs/updates packages
    - Installs/configures cx_Oracle with the instantclient
    - Makes a working directory and copies the .zip file with the app into it
    - Unzips the app
    - Installs app-specific packages
    - Configures the application
    - Configures nginx using the template.nginx.conf file
    - sets permissions and users
    - Runs nginx on port 80 (exposes that port)
    - Runs a supervisor using the template.supervisor.conf file, which sets the follwing:
        - Generic supervisor settings
        - The template program settings, including the run command `uswgi` using the uwsgi.ini file, which sets the socket at 5005 and the application start file as app.py
- Runs aforementioned docker container using all necessary environment variables
- Logs to console using `docker logs`

### Building and running locally in debug mode
1. Make sure you have python 2.7 installed using `brew install python` or `apt-get install python`
2. Download this file https://bootstrap.pypa.io/get-pip.py and install pip using `python get-pip.py`
3. Install virtualenv by running `pip install virtualenv`
4. Navigate to the root directory and run `virtualenv -p /usr/bin/python2.7 template-venv` (name it whatever you want for your project instead of template-venv)
5. Activate the virtual environment by running `source template-venv/bin/activate`
6. Run the instructions in the dockerfile locally to set up the oracle instantclient and install the pip packages
7. Navigate to python-template/template and run `python app.py`
