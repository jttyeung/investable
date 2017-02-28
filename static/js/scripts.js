"use strict";

// Page load defaults
// $('#property-details-page').hide()

var markers = [];
var map;


// Initialize Google Map on the global scope
window.initMap = function() {
    var unitedStates = {lat: 37.8037745, lng: -100.7662268}
    var geocoder = new google.maps.Geocoder();

    map = new google.maps.Map(document.getElementById('map'), {
        center: unitedStates,
        zoom: 4,
        styles: [{"featureType":"administrative","elementType":"all","stylers":[{"visibility":"on"},{"lightness":33}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2e5d4"}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#c5dac6"}]},{"featureType":"poi.park","elementType":"labels","stylers":[{"visibility":"on"},{"lightness":20}]},{"featureType":"road","elementType":"all","stylers":[{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry","stylers":[{"color":"#c5c6c6"}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#e4d7c6"}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#fbfaf7"}]},{"featureType":"water","elementType":"all","stylers":[{"visibility":"on"},{"color":"#acbcc9"}]}]
    });

    // Waits for search button to be clicked before geocoding
    document.getElementById('search').addEventListener('click', function(evt) {
        evt.preventDefault();
        geocodeAddress(geocoder, map);
    });
}


// Sets all markers on map
function setMapOnAll(map){
    for (var i = 0; i < markers.length; i++){
        markers[i].setMap(map);
    }
}


// Removes the markers from the map, but keeps them in the array
function clearMarkers() {
    setMapOnAll(null);
}

// // Shows any markers currently in the array
// function showMarkers() {
//     setMapOnAll(map);
// }


// Deletes all markers in the array by removing references to them
function deleteMarkers() {
    clearMarkers();
    markers = [];
}


// Geocodes the location of the user-entered address
function geocodeAddress(geocoder, map) {
    deleteMarkers();

    // Gets the full address (street, city, state, zip) entered by the user
    var fullAddress = { 'address': document.getElementById('address-search').value,
                        'citystatezip': document.getElementById('citystatezip-search').value
                      };

    // If only city and state or zipcode is entered,
    // geocode that location on the map and
    // get the location of all listings for sale in that area
    if (fullAddress.address === ''){
        // Create geocoder
        var geocoder = new google.maps.Geocoder();
        console.log('inside fulladdress empty');
        // Geocode just the city and state or zipcode
        geocoder.geocode({'address': fullAddress.citystatezip}, function(results, status) {

            // If the location is found via geocoder
            if (status === 'OK') {
                // Set the zoom and center of the map to that location
                map.setCenter(results[0].geometry.location);
                map.setZoom(13);
                // Extract the map boundaries provided by the geocoder
                var geoBounds = JSON.stringify(results[0].geometry.bounds);
                // Get all listings for sale within the map boundaries
                $.get('/listings.json', {'geoBounds': geoBounds}, addListingMarkers);
            }
        });

        // } else {
        //     alert('Geocode was not successful for the following reason: ' + status);

    // If an exact location is entered, take that location and get the unit's information
    } else {
        console.log('inside fulladdress else');
        getUnitInfo();
    }
}


// For all locations within the bounds of the map,
// show markers for each location
function addListingMarkers(listings){
    for (var i=0; i < listings.length; i++){
        var listing = listings[i];
        var latitude = parseFloat(listing['latitude']);
        var longitude = parseFloat(listing['longitude']);

        // Creates a marker for each listing
        var marker = new google.maps.Marker({
            map: map,
            position: {lat: latitude, lng: longitude},
            details: listing
        });
        attachListener(marker, listing);

        // Stores each marker in global markers array
        markers.push(marker);
    }
}


function attachListener(marker, listing) {
    marker.addListener('click', function() {
        updatePrice(listing, marker);
    });
}



function getUnitInfo(evt) {
    // Resets page values on new search
    $('#list-price').html('');
    $('#mortgage-rate').val('');
    $('#mortgage-downpayment').attr('placeholder', 0);
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


// Calculates 20% downpayment of the price of the listing
function calculateTwentyPercentDownpayment(price) {
    return Math.round(parseInt(price)*0.20);
}


function updatePrice(listing, marker) {
    console.log(listing);
    // Updates page with unit details if the unit is available,
    // only shows an alert with a Zillow price estimate if unit is off-market,
    // or error message if unit address is not found.

    // Creating variable values from the server's response
    var price = listing.price;
    // if (typeof price == 'string'){
    //     price = price.replace(/\D/g,'');
    // }
    var twentyPercentDownpayment = calculateTwentyPercentDownpayment(price);
    //.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    var avgRent = listing.rent_avgs;
    var latitude = parseFloat(listing.latitude);
    var longitude = parseFloat(listing.longitude);

    // If successfully found listing on Zillow and listing is for sale
    // if (listing.response === 999){
    //     map.setCenter({lat: latitude, lng: longitude});
    //     // map.setZoom(14);
    //     // Show the property details div
    //     $('#property-details-page').show()
    //     // Update the property details information on the page
    //     $('#list-price').html(price);
    //     $('#mortgage-downpayment').attr('placeholder', twentyPercentDownpayment);
    //     // Get the average rent rate in the surrounding area
    //     updateAvgRentRate(avgRent);
    // } else
    if (listing.response === 100){
        // deleteMarkers();
        // Add a google maps marker

        // If markers do not exist, then it is a new search listing
        if (!marker.position){
            // Add new marker
            var marker = new google.maps.Marker({
                map: map,
                position: {lat: latitude, lng: longitude},
                icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
            });
            // Store marker in markers array
            markers.push(marker);
        }
        // Reset center and zoom to marker locations
        resetMarkerSelections();
        setMarkerSelection(marker);
        map.setCenter({lat: latitude, lng: longitude});
        // map.setZoom(14);
        // Show the property details div
        $('#property-details-page').show()
        // Update the property details information on the page
        $('#list-price').html(price);
        $('#mortgage-downpayment').attr('placeholder', twentyPercentDownpayment);
        // Get the average rent rate in the surrounding area
        updateAvgRentRate(avgRent);

    // If listing is found on Zillow, but it is not for sale
    } else if (listing.response === 200) {
        $('#div-message').html('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' + listing.message);
        $('#div-message').addClass('btn-info');
        $('#div-message').removeAttr('hidden');

    // Or if no such listing exists on Zillow
    } else {
        $('#div-message').html('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' + listing.message);
        $('#div-message').addClass('btn-danger');
        $('#div-message').removeAttr('hidden');
    }
}


// Reset all marker colors to red on new marker selection
function resetMarkerSelections() {
    for (var i=0; i < markers.length; i++){
        markers[i].setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png');
    }
}


// Set selected marker to blue
function setMarkerSelection(marker) {
    marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png');
}


// Closes any div "alerts" on click
$('#div-message').on('click', function() {
    $('#div-message').html('');
    $('#div-message').removeClass('btn-info');
    $('#div-message').attr('hidden', 'hidden');
});


// Gets user-entered mortgage details on submit
$('#mortgage-calculator').on('submit', getMonthlyPayment);

// Calculates the mortgage payment for the home price listed
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

// Returns a monthly mortgage and total mortgage amount
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
