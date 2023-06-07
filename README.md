# Commentaries API
<hr>

This service helps to organized commentaries page written on DRF. Only registered users can add commentaries. Commentary
can be commented. Files, such as .gif, .jpg, .png, and .txt can be added to commentary. 

## Structure:
![structure.svg](readme_img%2Fstructure.svg)

## Features:
<hr>

- JWT authenticated:
- Admin panel: /admin/
- Documentation is located at: /api/doc/swagger/
- Managing commentaries
- Adding file to commentary
- Ordering commentary by different key.

## Run with docker
<hr>

Docker should be installed

```python
git clone https://github.com/Terrrya/dZENcode-test.git
cd dZENcode-test
```
Create .env file and fill it as shown in .env_sample

```python
docker-compose up
```
Open in browser 127.0.0.1:8000/api/commentary/ 

## Getting access
<hr>

You can use following superuser:
- User: admin
- Password: 12345

Or create another one by yourself:
- create user via api/user/register/

To work with token use:
- get access token and refresh token via api/user/token/
- refresh access token via api/user/token/refresh/


### Note: **Make sure to send Token in api urls in Headers as follows**

```
key: Authorization
value: Bearer <token>
```

## Commentaries API allows:

- via api/admin/ --- Work with admin panel
- via /api/doc/swagger/ --- Detail api documentation by swagger
- via [POST] /api/user/register/ --- Register a new user
- via [POST] /api/user/token/ --- Obtain new Access and Refresh tokens via credential
- via [POST] /api/user/token/refresh/ --- Obtain new Access token via refresh token
- via [GET] /api/commentaries/ --- List commentaries
- via [POST] /api/commentary/ --- Create new commentary
