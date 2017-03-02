"use strict";

// Page load defaults
// $('#property-details-page').hide()

// Price slider
$(function() {
  $("#slider-range").slider({
    range: true,
    min: 50000,
    max: 5000000,
    step: 100,
    values: [50000, 5000000],
    slide: function( event, ui ) {
        $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
    }
  });
  $("#amount").val("$" + $("#slider-range").slider("values", 0) +
    " - $" + $("#slider-range").slider("values", 1));
} );


var markers = new Set();
// var selectedMarkers = new Set();
var map;


// Initialize Google Map on the global scope
window.initMap = function() {
  var unitedStates = {lat: 37.8037745, lng: -100.7662268};
  var geocoder = new google.maps.Geocoder();

  map = new google.maps.Map(document.getElementById('map'), {
    center: unitedStates,
    zoom: 4,
    styles: [{"featureType":"administrative","elementType":"all","stylers":[{"visibility":"on"},{"lightness":33}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2e5d4"}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#c5dac6"}]},{"featureType":"poi.park","elementType":"labels","stylers":[{"visibility":"on"},{"lightness":20}]},{"featureType":"road","elementType":"all","stylers":[{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry","stylers":[{"color":"#c5c6c6"}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#e4d7c6"}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#fbfaf7"}]},{"featureType":"water","elementType":"all","stylers":[{"visibility":"on"},{"color":"#acbcc9"}]}]
  });

  // Adds map listener; updates map markers on changes to map once user
  // idles from map panning/zooming
  map.addListener('idle', function() {
    // If the user is searching within a region use the map listener,
    // otherwise a single address search should not update
    // listings shown on map when the map view changes
    if (markers.size > 1){
      deleteMarkers();
      // showSelectedMarkers();

      // If map isn't zoomed in enough, tell user to zoom in
      if (map.zoom < 12){
        zoomMapInstructions();
      // Once map is zoomed in, change to click instructions
      // then check search filters before returning listing results
      } else {
        clickMapInstructions();
        checkFilters();
      }
    }

  });

  // Waits for search button to be clicked before geocoding
  document.getElementById('search').addEventListener('click', function(evt) {
    evt.preventDefault();
    geocodeAddress(geocoder, map);
  });
}


// Shows user interaction map instructions
function zoomMapInstructions(){
  $('#map-notification').html('Zoom in to see listings for sale in the area.')
}


// Hides user interaction map instructions
function clickMapInstructions(){
  $('#map-notification').html('Click on each listing for more details.')
}


// Sets all markers on map
function setMapOnAll(map){
  for (let marker of markers){
    marker.setMap(map);
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
  markers.clear();
}


// function showSelectedMarkers() {
//     for (let marker of selectedMarkers){
//         // marker.setIcon('http://maps.google.com/mapfiles/ms/icons/pink-dot.png');
//         marker.setMap(map);
//     }
// }


// Set selected marker to blue
function setMarkerSelection(marker, listing) {
  var selectedMarker = marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png');
  // selectedMarkers.add(selectedMarker);
  // Get average rent rate on marker selection
  var listing = JSON.stringify(listing);
  $.get('/avgrent.json', {'listing': listing}, updateAvgRentRate);
}


// Reset all marker colors to red on new marker selection
function resetMarkerSelections(marker) {
  for (let marker of markers){
    marker.setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png');
  }
}


// Adds a click listener to each marker to update price when clicked
function attachListener(marker, listing) {
  marker.addListener('click', function(evt) {
    updatePrice(listing, marker);
  });
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

    // Geocode just the city and state or zipcode
    geocoder.geocode({'address': fullAddress.citystatezip}, function(results, status) {

      // If the location is found via geocoder
      if (status === 'OK') {
        // Set the zoom and center of the map to that location
        map.setCenter(results[0].geometry.location);
        map.setZoom(13);

        checkFilters();

      // If the location cannot be geocoded, raise error message to user
      } else {
        $('#div-message').html('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' + "We weren't able to find that location. Please try your search again.");
        $('#div-message').addClass('btn-danger');
        $('#div-message').removeAttr('hidden');
      }
    });

  // If an exact location is entered, take that location and get the unit's information
  } else {
    getUnitInfo();
  }
}


// For all locations for sale within the map boundaries,
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
      details: listing,
      icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
    });
    attachListener(marker, listing);

    // Stores each marker in global markers array
    if (!(markers.has(marker))){
      markers.add(marker);
    }
  }
}


// Adds a listener to bedroom, bathroom, and price filters
$('#slider-range').on('slidechange', function(){ deleteMarkers(); checkFilters();});
$('#bedroom-filter').on('change', function(){ deleteMarkers(); checkFilters();});
$('#bathroom-filter').on('change', function(){ deleteMarkers(); checkFilters();});


// Gets filter values and requests the server for a database query on those values
function checkFilters(){
  // Extract the map boundaries from geocoded location
  var bounds = map.getBounds();
  if (bounds){
    var geoBounds = JSON.stringify(bounds);
  // If no boundaries exist, use map viewport box from geocoded location
  } else {
    var viewport = results[0].geometry.viewport;
    var geoBounds = JSON.stringify(viewport);
  }

  // Grab filter values and send to server as an object
  var priceFilter = $("#slider-range").slider("values");
  var lowPrice = priceFilter[0];
  var highPrice = priceFilter[1];
  var bedroomFilter = $('#bedroom-filter').val();
  var bathroomFilter = $('#bathroom-filter').val();
  var filters = {'geoBounds': geoBounds, 'lowPrice': lowPrice, 'highPrice': highPrice, 'bedroomFilter': bedroomFilter, 'bathroomFilter': bathroomFilter}

  $.get('/listings.json', filters, addListingMarkers)
}


// Calculates 20% downpayment of the price of the listing
function calculateTwentyPercentDownpayment(price) {
  return Math.round(parseInt(price)*0.20);
}


function getUnitInfo(evt) {
  // Resets page values on new search
  $('#list-price').html('');
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


function updatePrice(listing, marker) {

  // Updates page with unit details if the unit is available,
  // only shows an alert with a Zillow price estimate if unit is off-market,
  // or error message if unit address is not found.

  // Creating variable values from the server's response
  var price = listing.price;
  var twentyPercentDownpayment = calculateTwentyPercentDownpayment(price);
  //.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  var avgRent = listing.rent_avgs;
  var latitude = parseFloat(listing.latitude);
  var longitude = parseFloat(listing.longitude);

  if (listing.response === 100){
      // Add a google maps marker
      // If markers do not exist, then it is a new search listing
      if (markers.size === 0){
        // Add new marker
        var marker = new google.maps.Marker({
          map: map,
          position: {lat: latitude, lng: longitude},
          icon : 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
        });
        // Zoom in on marker
        map.setZoom(14);
        map.setCenter(marker.position);
        // Store marker in markers array
        markers.add(marker);
      }

      // Resets all marker colors
      resetMarkerSelections(marker);
      // Sets clicked marker to new color
      setMarkerSelection(marker, listing);

      var rate = $('#mortgage-rate').val();
      var downpayment = $('#mortgage-downpayment').val();
      if (rate && downpayment){
        getMonthlyPayment(price);
      }
      // Show the property details div
      $('#property-details-page').show();
      // Update the property details information on the page
      $('#bedrooms').html(listing.bedrooms);
      $('#bathrooms').html(listing.bathrooms);
      $('#sqft').html(listing.sqft);
      $('#hoa').html(listing.hoa);
      $('#list-price').html(price);
      $('#suggested-downpayment').html(twentyPercentDownpayment);

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
  // If event type is object (new click event), prevent event default action
  if (typeof(evt) === typeof({})){
    evt.preventDefault();
  }

  // Get mortgage details from user inputs
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
