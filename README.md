Investable
======

Investable is a research tool for individuals looking to purchase rental real estate. Intended for smart investors, this app compares personal mortgage rates to average rent rates within the surrounding neighborhood of the point of interest. Using the estimated rental worth on the market, it helps users instantly determine which properties might bring in rental income. Users can search by address or region or use Google Maps directly to find a home of interest, and can filter down search results by number of bedrooms, bathrooms or the home listing price.


Installation
------

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
1. Python 2.7.0
2. Vagrant or other virtual machine
3. Set up a Python virtualenv
4. Install all requirements

```
pip install -r requirements
```
5. Make sure you have PostgreSQL running (psql)
6. Create a database named investable

```
CREATEDB investable;
```
7. Open the database, add the PostGIS database extension, and exit out of the database

```
psql investable

CREATE EXTENSION postgis;

\quit
```
8. Create tables in your database

```
python model.py
```
9. Start the Flask server

```
python server.py
```
10. Go to localhost:5000


## Built With

Python, PostgreSQL, SQLAlchemy, PostGIS, Flask, Jinja, JavaScript, jQuery, AJAX, HTML, CSS, Bootstrap, Scrapy, BeautifulSoup


## Authors

* **Joanne Yeung** - [LinkedIn](https://linkedin.com/in/jttyeung)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

