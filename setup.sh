#!/bin/bash
echo 'Setting up your environment...'
sudo apt-get update
sudo apt-get install -y build-essential
sudo apt-get install -y curl
sudo apt-get install -y python3.9
python3.9 -m pip install Jinja2==3.1.6 MarkupSafe==3.0.2 Werkzeug==3.1.3 asgiref==3.8.1 blinker==1.9.0 click==8.1.8 cryptography==44.0.2 docutils==0.21.2 importlib_metadata==8.6.1 itsdangerous==2.2.0 packaging==24.2 pallets_sphinx_themes==2.3.0 python-dotenv==1.1.0 typing_extensions==4.13.1
