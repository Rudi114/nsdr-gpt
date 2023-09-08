# NSDR AI Generator

## Installing dependencies / setup environment
This project uses a virtualenv to keep package versions in line

If you don't already have virtualenv installed, install it with:
```
sudo pip3 install virtualenv
```

created env with:
```sh
python3 -m venv nsdr_env
```

activate it with:
```sh
source nsdr_env/bin/activate
```

install existing deps with:
```sh
pip install -r requirements.txt
```

when adding new deps, update requirements.txt with:
```sh
pip freeze > requirements.txt
```

## Running
dev mode
```
flask --app nsdr run --debug
```
