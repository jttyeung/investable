Investable
======

Investable is a research tool for individuals looking to purchase rental real estate. Intended for smart investors, this app compares personal mortgage rates to average rent rates within the surrounding neighborhood of the point of interest. Using the estimated rental rate on the market, it helps users instantly determine which properties might bring in rental income. Users can search by address or region or use Google Maps directly to find a home of interest, and can filter down search results by number of bedrooms, bathrooms or the home listing price.

![Investable Homepage](/static/images/investable.png)


Table of Contents
------
* [How Run Investable Locally](#run)
* [Technologies Used](#technology)
* [How to Use Investable](#use)
* [Version 2.0](#nextversion)
* [Author](#author)
* [License](#license)


## <a name="run"></a>How to Run Investable Locally

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

1. Python 2.7.0
2. Vagrant or other virtual machine

### Installation Instructions

1. Set up a Python virtualenv and activate it.
2. Install all app dependencies listed in requirements.txt.
    ```
    pip install -r requirements.txt
    ```
3. Make sure you have PostgreSQL running (psql).
4. Create a database named investable.
    ```
    CREATEDB investable
    ```
5. Open the database, add the PostGIS database extension, and exit out of the database.
    ```
    psql investable

    CREATE EXTENSION postgis;

    \quit
    ```
6. Create tables in your database.
    ```
    python model.py
    ```
7. Start the Flask server.
    ```
    python server.py
    ```
8. Go to localhost:5000 to view the application.


## <a name="technology"></a>Technologies Used

* Python
* PostgreSQL, PostGIS
* SQLAlchemy, GeoAlchemy2
* Flask
* Jinja2
* JavaScript, jQuery, AJAX, JSON
* HTML
* CSS
* Bootstrap
* Scrapy
* BeautifulSoup
* Zillow API
* Google Maps API


## <a name="use"></a>How to Use Investable
1. Edit the list of 'start_urls' in `/rent_scraper/rent_scraper/spiders/craigslist.py` with the Craigslist URL for the city you would like rent averages from.
2. Edit the 'CLOSESPIDER_ITEMCOUNT' in `/rent_scraper/rent_scraper/spiders/settings.py` to indicate how many rental properties to include in the average. Please scrape responsibly.
3. Search for a listing of interest. **Note**: Cannot search by city due to Zillow API restrictions.
4. Enter your mortgage customizations to compare rent rate vs. mortgage rate, or search again.


## <a name="nextversion"></a>Version 2.0
* Improve application security
* Add Airbnb rates comparison as rental income option
* Add user login to save favorite listings
* Using sessions, mark visited markers a different color
* Address normalization for search
* Make price slider range dynamic to database data
* Show graphs of rental or home prices over time
* Build a Chrome extension for app


## <a name="author"></a>Author

* Joanne Yeung is a full-stack engineer in San Francisco, CA. Learn more here: [https://linkedin.com/in/jttyeung](https://linkedin.com/in/jttyeung)


## <a name="license"></a>License

This project is licensed under the [MIT License](LICENSE.md)

