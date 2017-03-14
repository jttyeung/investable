Investable
======

Investable is a research tool for individuals looking to purchase rental real estate. Intended for smart investors, this app compares personal mortgage rates to average rent rates within the surrounding neighborhood of the point of interest. Using the estimated rental rate on the market, it helps users instantly determine which properties might bring in rental income. Users can search by address or region or use Google Maps directly to find a home of interest, and can filter down search results by number of bedrooms, bathrooms or the home listing price.

Database Model (See full model in the <kbd>model.py</kbd> file.)
![Investable DB Model](/static/images/database_model.png)

Landing Page
![Investable Homepage](/static/images/investable_1.png)

![Investable Second Page](/static/images/investable_2.png)


Table of Contents
------
* [Technologies Used](#technology)
* [How Run Investable Locally](#run)
* [How to Use Investable](#use)
* [Future Features](#nextversion)
* [Author](#author)
* [License](#license)


## <a name="technology"></a>Tech Stack

<b>Backend:</b> Python, Flask, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, BeautifulSoup, Scrapy<br/>
<b>Frontend:</b> JavaScript, jQuery, AJAX, JSON, Jinja2, Bootstrap, HTML, CSS<br/>
<b>APIs:</b> Zillow, Google Maps<br/>


## <a name="run"></a>How to Run Investable Locally

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

1. Python 2.7.0
2. PostgreSQL

### Installation Instructions
1. Clone this repository:
  ```
  $ git clone https://github.com/jttyeung/investable.git
  ```

2. Set up a Python virtualenv and activate it.
  ```
  $ virtualenv env
  $ source env/bin/activate
  ```

3. Install all app dependencies listed in requirements.txt.
  ```
  $ pip install -r requirements.txt
  ```

4. Make sure you have PostgreSQL running (psql).
5. Create a database named investable.
  ```
  $ CREATEDB investable
  ```

6. Open the database, add the PostGIS database extension, and exit out of the database.
  ```
  $ psql investable

  CREATE EXTENSION postgis;
  \quit
    ```
7. Create tables in your database.
  ```
  $ python model.py
  ```

8. Set up a <kbd>secrets.sh</kbd> file using the following API key variables, and fill in the template with your own API key values.
  ```
  export APP_KEY='your app secret key'
  export ZWSID='your zillow api key'
  export GMAPS_JS='your google maps api key'
  ```

9. Source the secrets file.
  ```
  $ source secrets.sh
  ```

10. Start the Flask server.
  ```
  $ python server.py
  ```

11. Go to localhost:5000 to view the application.


## <a name="use"></a>How to Use Investable
1. Edit the list of `start_urls` in `/rent_scraper/rent_scraper/spiders/craigslist.py` with the Craigslist URL for the city you would like rent averages from.
2. Edit the `CLOSESPIDER_ITEMCOUNT` in `/rent_scraper/rent_scraper/spiders/settings.py` to indicate how many rental properties to include in the average. Please scrape responsibly.
3. Search for a listing of interest by full address. **Note**: Cannot search by city/region due to Zillow API call restrictions.
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

Joanne Yeung is a full-stack engineer in San Francisco, CA.
Learn more on LinkedIn: [https://linkedin.com/in/jttyeung](https://linkedin.com/in/jttyeung)


## <a name="license"></a>License

This project is licensed under the [MIT License](LICENSE.md).

