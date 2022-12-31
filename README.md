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

# How to consume the API

The API offers different endpoints to consume, you can perform requests
against these endpoints to retreive resources from the server.

Available request methods:

* GET
* POST
* PUT
* DELETE

You can use different tools to perform the HTTP requests. Here are some
examples:

### Using cURL

#### GET

```sh
curl http://127.0.0.1:5000/api/frameworks
```

#### GET (it also includes the responde headers)

```sh
curl --include http://127.0.0.1:5000/api/frameworks/1
```

#### POST

```sh
curl \
  --data '{ "name": "AngularJS" }' \
  --request POST \
  --header "Content-Type: application/json" \
  --include \
  http://127.0.0.1:5000/api/frameworks
```

### PUT

This is basically the same as a POST request but instead of
using raw data you can also pass data retrived from a file:

```sh
curl \
  --data @fourth_framework.json
  --request PUT \
  --header "Content-Type: application/json" \
  --include \
  http://127.0.0.1:5000/api/frameworks/2
```

The file `fourth_framework.json` has this content:

```
{
	"name": "AngularJS"
}
```

Of course, you could also use raw data just as in the POST request.

### DELETE

This is the easiest one. Since this endpoint returns no content in case
of finding and destroying a framework successfully, you can use the
flag `--include` to see the response's status code which will be 204
and that HTTP code status means: NO CONTENT ("The server successfully
processed the request, and is not returning any content.")

```sh
curl --include http://127.0.0.1:5000/api/frameworks/2
```

## Other tools to perform HTTP requests

There are other tools that allow you to perform HTTP requests such
as the popular Postman. It's recommended to use a python program
called HTTPie due to how simple is to use it.

### How to install and use HTTPie

In order to install HTTPie you could use a python virtual
environment, activate it and execute the following command:

```sh
# How to install HTTPie
pip install httpie
```

After that, you'll have the command `http` available:

```sh
# Run HTTPie
http
# You'll get a simple help text after executing the last command
```

You can perform a request a request, that could be seen as intimidating in
cURL, in HTTPie just easy as this:

```sh
http POST :5000/api/frameworks name=VueJS
```

Much cleaner, much easier. The request URL is assumed to be "localhost" or
"http://127.0.0.1" and that's the reason why only the port needs to be
specified. The request is sent as JSON content type automatically.

If you need more examples you may want to execute:

```sh
http --help
```

# Credits and refereces

This repository was created by [CodeNoSchool](https://github.com/codenoschool).

- Links:
	- [CodeNoSchool](https://www.youtube.com/c/CodeNoSchool)
	- [ISC School](https://www.youtube.com/@ISCSchool)
	- [Blog (Blogger)](https://codenoschool.blogspot.mx/)
	- [Blog (Vivaldi)](https://codenoschool.vivaldi.net/)
	- [Twitter](https://twitter.com/codenoschool)
