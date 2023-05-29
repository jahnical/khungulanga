# SmartSkin

AI powered mobile application for skin disease detection.

## Tools
* Tensorflow (Computer Vision)
* Django (Backend)
* Flutter (Frontend)

## Get started
Make sure you have [Python](https://www.python.org/downloads/), [Tensorflow](https://www.tensorflow.org/install), [Flutter](https://docs.flutter.dev/get-started/install) and [Django](https://www.djangoproject.com/download/) installed.

### 1. Install Dependencies
  1. In smartskin_app run `pub get`

### 2. Run App
  1. In smartskin run the django development server `python manage.py runserver`
     > You can test the api with postman or run it with port `python manage.py runserver 0.0.0.0:8000` and add host IP address to smartskin_app/lib/api_connection/endpoints `baseURL` to test it with the flutter app.  
     
  2. In smartskin_app run flutter app by `flutter run`
     > Recommended to run it on mobile phone or local machine.