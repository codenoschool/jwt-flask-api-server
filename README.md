# Introduction

This projects aims for creating a web application using Flask, which is a
micro-framework based on Python, that serves as an API server that requires
authentication trough JWT.

# How to run the web application

Running the WA is pretty straight forward:

* Clone this repository
* Install a recent version of Python >= 3.9.2 and pip >= 22.3.1
* Create a Python Virtual Environment and install the required packages for
the WA which are specified inside the requirements file (that file is also
included in this repository).
* Run the application by executing `flask run`.

Demonstratiton:

```sh
# Clone this repository
git clone https://github.com/codenoschool/jwt-flask-api-server
# Move inside the cloned repository
cd jwt-flask-api-server
# Create a python virtual enviroment
python3 -v env env
# Activate the python virtual environment
source env/bin/activate
# Install the required packages
pip install -r requirements.historical_reference
# Run the application (you can remove the --debug flag)
flask --debug run
```

... And that's it.

# Credits and refereces

This repository was created by [CodeNoSchool](https://github.com/codenoschool).

- Links:
	- [CodeNoSchool](https://www.youtube.com/c/CodeNoSchool)
	- [ISC School](https://www.youtube.com/@ISCSchool)
	- [Blog (Blogger)](https://codenoschool.blogspot.mx/)
	- [Blog (Vivaldi)](https://codenoschool.vivaldi.net/)
	- [Twitter](https://twitter.com/codenoschool)
