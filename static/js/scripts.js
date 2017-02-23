"use strict";

// Page load defaults
// $('#property-details-page').hide()

// Returns price of listing and average rent rate
// $('#search-bar').on('submit', getUnitInfo);



// Initialize Google Map
function initMap() {
    var sanFrancisco = {lat: 37.7678149, lng: -122.4108119}
    var geocoder = new google.maps.Geocoder();
    var map = new google.maps.Map(document.getElementById('map'), {
        center: sanFrancisco,
        zoom: 12
    });

    // Waits for search button to be clicked before geocoding
    document.getElementById('search').addEventListener('click', function() {
        geocodeAddress(geocoder, map);
    });


    // Using user's entered address, geocodes location to make map markers
    function geocodeAddress(geocoder, map) {
        var address = document.getElementById('address-search').value;
        var citystatezip = document.getElementById('citystatezip-search').value;

        // If only city/state/zip is entered and no address is entered,
        // find the center of that location on the map and
        // show markers for all listings available in that area
        if (address === ''){
            geocoder.geocode({'address': citystatezip}, function(results, status) {
                if (status === 'OK') {
                    map.setCenter(results[0].geometry.location);
                    // For all locations within the bounds of the map,
                    // show markers for each, up to ???
                    $.get('/listings.json', function (listingResults){
                        for (var i=0; i < listingResults.length < i++){
                            var latitude = listingResults.latitude;
                            var longitude = listingResults.longitude;
                            var marker = new google.maps.Marker({
                                map: map,
                                position: {lat: latitude, lng: longitude}
                            });
                        }
                    }
                    // var marker = new google.maps.Marker({
                    //     map: resultsMap,
                    //     position: results[0].geometry.location
                    // });
                // } else {
                //     alert('Geocode was not successful for the following reason: ' + status);
                }
            });
        // If an exact location is entered, take that location and get the unit's information
        } else {
            document.getElementById('search-bar').addEventListener('submit', getUnitInfo);
        }
    }


    function getUnitInfo(evt) {
        evt.preventDefault();

        // Resets page values on new search
        $('#list-price').html('');
        $('#mortgage-rate').val('');
        $('#mortgage-downpayment').attr('placeholder', 0);
        $('#neighborhood').html('');
        $('#monthly-payment').html('');
        $('#total-payment').html('');
        $('#avg-rent-by-br').html('');
        $('#avg-rent-by-sqft').html('');

        // Gets the full address entered by the user
        var fullAddress = { 'address': $('#address-search').val(),
                            'citystatezip': $('#citystatezip-search').val()
                          };

        // Gets the details of the listing from calling the server
        $.get('/search.json', fullAddress, updatePrice);
}

    function updatePrice(listing) {
        // Updates page with unit details if the unit is available,
        // only shows an alert with a Zillow price estimate if unit is off-market,
        // or error message if unit address is not found.

        // Creating variable values from the server's response
        var price = listing.price;
        var twenty_percent_downpayment = Math.round(parseInt(price.replace(/\D/g,''))*0.20);
        //.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        var neighborhood = listing.neighborhood;
        var avgRent = listing['rent_avgs'];
        var latitude = parseFloat(listing.latitude);
        var longitude = parseFloat(listing.longitude);

        // If successfully found listing on Zillow and listing is for sale
        if (listing.response === 100){
            // Add a google maps marker
            var marker = new google.maps.Marker({
                map: map,
                position: {lat: latitude, lng: longitude}
            });
            // Show the property details div
            $('#property-details-page').show()
            // Update the property details information on the page
            $('#list-price').html(price);
            $('#mortgage-downpayment').attr('placeholder', twenty_percent_downpayment);
            $('#neighborhood').html(neighborhood);
            // Get the average rent rate in the surrounding neighborhood
            updateAvgRentRate(avgRent);

        // If listing is found on Zillow, but it is not for sale
        } else if (listing.response === 200) {
            $('#div-message').html('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' + price);
            $('#div-message').addClass('btn-info');
            $('#div-message').removeAttr('hidden');

        // Or if no such listing exists on Zillow
        } else {
            $('#div-message').html('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' + price);
            $('#div-message').addClass('btn-danger');
            $('#div-message').removeAttr('hidden');
        }
    }

}


// Closes any div "alerts" on click
$('#div-message').on('click', function() {
    $('#div-message').html('');
    $('#div-message').removeClass('btn-info');
    $('#div-message').attr('hidden', 'hidden');
});


// Returns calculated mortgage rate
$('#mortgage-calculator').on('submit', getMonthlyPayment);

function getMonthlyPayment(evt){
    evt.preventDefault();

    var mortgageDetails = {
        'price': $('#list-price').html(),
        'rate': $('#mortgage-rate').val(),
        'downpayment': $('#mortgage-downpayment').val(),
        'loan': $('#mortgage-loan-type').val()
    };

    $.get('/calculator', mortgageDetails, updateMonthlyPayment);
}

function updateMonthlyPayment(rate){
    $('#monthly-payment').html(rate.mortgage);
    $('#total-payment').html(rate.total_mortgage);
}


// Returns nearby average rent rates by bedroom or sqft
function updateAvgRentRate(avgRent){
    var byBedroom = avgRent['avg_rent_by_br'];
    var bySqft = avgRent['avg_rent_by_sqft'];

    $('#avg-rent-by-br').html(byBedroom);
    $('#avg-rent-by-sqft').html(bySqft);
}
