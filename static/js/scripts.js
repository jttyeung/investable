"use strict";

// Page load defaults
$('div .row.fourth').hide();
$('.property-info').hide();

// Page scrolling down animation on search click
$('#search-button').on('click', function() {
  // Show the property details div
  $('div .row.fourth').show();
  $('html,body').animate({
    scrollTop: $('.fourth').offset().top},
    'slow');
  displayMap();
  }
);

// Add onMouseOver cursor to change to pointer
$('#page-up').css('cursor', 'pointer');

// Page scrolling up animation on new search
$('#page-up').on('click', function() {
  // Show the property details div
  $('div .row.third').show();
  $('html,body').animate({
    scrollTop: $('.third').offset().top},
    300);
  displayMap();
  }
);

// Display map after search
function displayMap(){
  initMap();
}

// Format currency with commas and dollar sign
function formatCurrency(number){
  return '$' + formatNumWithCommas(number);
}

// Format currency with commas and dollar sign
function formatNumWithCommas(number){
  return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Price slider
$(function() {
  $("#slider-range").slider({
    range: true,
    min: 50000,
    max: 20000000,
    step: 1000,
    values: [50000, 20000000],
    slide: function( event, ui ) {
      $("#amount").val(formatCurrency(ui.values[0]) + " - " + formatCurrency(ui.values[1]));
    }
  });
  $("#amount").val(formatCurrency($("#slider-range").slider("values", 0)) +
    " - " + formatCurrency($("#slider-range").slider("values", 1)));
} );

function resetValues(){
  // Resets page values on new search
  $('#list-price').html('');
  $('#hoa').html('');
  $('#bedrooms').html('');
  $('#bathrooms').html('');
  $('#sqft').html('');
  $('#monthly-payment').html('');
  $('#suggested-downpayment-amt').html('');
  $('#total-payment').html('');
  $('#avg-rent-by-br').html('');
  $('#avg-rent-by-sqft').html('');
  $('#potential-income').html('');
}

var markers = new Set();
var currentMarker = null;
// var selectedMarkers = new Set();
var map;


// Initialize Google Map on the global scope
// window.initMap = function() {
function initMap() {
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
    if (markers.size > 1 || markers.size < 1){
      deleteMarkers();
      if (map.zoom >= 13){
      // Once map is zoomed in, change to click instructions
      // then check search filters before returning listing results
        checkFilters();
      }
    }
    if (map.zoom < 13){
      // Hide address and property info
      $('#address').hide();
      $('.property-info').hide();
      // If map isn't zoomed in enough, tell user to zoom in
      zoomMapInstructions();
    } else {
      clickMapInstructions();
    }

  });

  // Waits for search button to be clicked before geocoding
  document.getElementById('search-button').addEventListener('click', function(evt) {
    evt.preventDefault();
    geocodeAddress(geocoder, map);
  });
}


// Shows user interaction map instructions
function zoomMapInstructions(){
  $('#map-notification').html('Zoom in on map to see listings for sale in the area.');
}


// Hides user interaction map instructions
function clickMapInstructions(){
  $('#map-notification').html('Select a listing on the map to see more details.');
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


// Deletes all markers in the array by removing references to them
function deleteMarkers() {
  clearMarkers();
  markers.clear();
}


// Set selected marker to blue
function setMarkerSelection(marker, listing) {
  marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png');
  // Save the current marker selection
  currentMarker = marker;
  // Get average rent rate on marker selection
  var listing = JSON.stringify(listing);

  $.get('/avgrent.json', {'listing': listing}, updateAvgRentRate);
}


// Reset all marker colors to red on new marker selection
function resetMarkerSelections(marker) {
  if (currentMarker){
    currentMarker.setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png');
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
  resetValues();

  // Gets the full address (street, city, state, zip) entered by the user
  var fullAddress = { 'address': document.getElementById('address-search').value,
                      'citystatezip': document.getElementById('citystatezip-search').value
                    };

  // If only city and state or zipcode is entered,
  // geocode that location on the map and
  // get the location of all listings for sale in that area
  if (fullAddress.address === ''){
    // resetValues();
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
  deleteMarkers();
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


// Adds a listener to price filter
$('#slider-range').on('slidechange', function(){ deleteMarkers(); checkFilters();});


// Filter + and - button listeners
$('#bed-minus').on('click', decrementBeds);
$('#bed-plus').on('click', incrementBeds);
$('#bath-minus').on('click', decrementBaths);
$('#bath-plus').on('click', incrementBaths);


// Decrements beds filter
function decrementBeds() {
  var bedrooms = parseInt($('#bedroom-filter').html());

  if (!isNaN(bedrooms) && bedrooms > 1){
    bedrooms -= 1;
    $('#bedroom-filter').html(bedrooms + '+ ');
    checkFilters();
  } else if (bedrooms === 1){
    bedrooms = 'Any';
    $('#bedroom-filter').html(bedrooms);
    checkFilters();
  }
}


// Decrements baths filter
function decrementBaths() {
  var bathrooms = parseInt($('#bathroom-filter').html());

  if (!isNaN(bathrooms) && bathrooms > 1){
    bathrooms -= 1;
    $('#bathroom-filter').html(bathrooms + '+ ');
    checkFilters();
  } else if (bathrooms === 1){
    bathrooms = 'Any';
    $('#bathroom-filter').html(bathrooms);
    checkFilters();
  }
}


// Increments beds filter
function incrementBeds() {
  var bedrooms = parseInt($('#bedroom-filter').html());

  if (isNaN(bedrooms)){
    bedrooms = 1;
    $('#bedroom-filter').html(bedrooms + '+ ');
    checkFilters();
  } else if (bedrooms < 5){
    bedrooms += 1;
    $('#bedroom-filter').html(bedrooms + '+ ');
    checkFilters();
  }
}


// Increments baths filter
function incrementBaths() {
  var bathrooms = parseInt($('#bathroom-filter').html());

  if (isNaN(bathrooms)) {
    bathrooms = 1;
    $('#bathroom-filter').html(bathrooms + '+ ');
    checkFilters();
  } else if (bathrooms < 5){
    bathrooms += 1;
    $('#bathroom-filter').html(bathrooms + '+ ');
    checkFilters();
  }
}


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
  var bedroomFilter = $('#bedroom-filter').html();
  if (bedroomFilter === 'Any') {
    bedroomFilter = 0;
  } else {
    bedroomFilter = parseInt(bedroomFilter)
  }
  var bathroomFilter = $('#bathroom-filter').html();
  if (bathroomFilter === 'Any') {
    bathroomFilter = 0;
  } else {
    bathroomFilter = parseInt(bathroomFilter)
  }
  var filters = {'geoBounds': geoBounds, 'lowPrice': lowPrice, 'highPrice': highPrice, 'bedroomFilter': bedroomFilter, 'bathroomFilter': bathroomFilter}

  $.get('/listings.json', filters, addListingMarkers)
}


// Calculates 20% downpayment of the price of the listing
function calculateTwentyPercentDownpayment(price) {
  return Math.round(parseInt(price)*0.20);
}


// Recalculates downpayment percentage
function calculateDownpaymentPercentage(price, downpayment) {
  var price = $('#list-price').html().replace(/\D/g,'');
  var downpayment = $('#mortgage-downpayment').val();
  var percentage = Math.round(parseInt(downpayment)/parseInt(price)*100);

  $('#downpayment-percentage').html(percentage + '%');
}


function getUnitInfo(evt) {
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
  var displayPrice = formatCurrency(price);
  var twentyPercentDownpayment = calculateTwentyPercentDownpayment(price);
  //.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  var avgRent = listing.rent_avgs;
  var latitude = parseFloat(listing.latitude);
  var longitude = parseFloat(listing.longitude);
  if (listing.response === 100){
    // Resets all marker colors
    resetMarkerSelections(marker);

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

    // Sets clicked marker to new color
    setMarkerSelection(marker, listing);

    // Get the current rate and downpayment amount
    var rate = $('#mortgage-rate').val();
    var downpayment = $('#mortgage-downpayment').val();

    // Show address and property info
    $('#address').show();
    $('.property-info').show();

    // Update the property details information on the page
    $('#address').html(listing.street + ', ' + listing.city + ', ' + listing.state + ' ' + listing.zipcode);
    $('#bedrooms').html(listing.bedrooms);
    $('#bathrooms').html(listing.bathrooms);
    $('#list-price').html(displayPrice);
    $('#mortgage-downpayment').val(twentyPercentDownpayment);
    // .trigger('change');
    // Format sqft if it exists
    if (listing.sqft){
      var sqft = listing.sqft.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
    $('#sqft').html(sqft);
    // Format HOA if it exists
    if (listing.hoa){
      var hoa = formatCurrency(listing.hoa);
      $('#hoa').html(hoa);
    } else {
      $('#hoa').html('None');
    }

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
$('#mortgage-downpayment').bind('keyup change', checkValueChanges);
$('#mortgage-rate').bind('keyup change', checkValueChanges);
$('#mortgage-loan-type').on('change', checkValueChanges);


// Check if the details on page have changed
function checkValueChanges() {
  var val = $(this).val();
  // If changes in value, update the monthly payment and downpayment percentage
  if( $(this).data('last') != val ){
    getMonthlyPayment();
    calculateDownpaymentPercentage();
  }
  $(this).data('last', val);
}


// Calculates the mortgage payment for the home price listed
function getMonthlyPayment(evt){
  // If event type is object (new click event), prevent event default action
  if (typeof(evt) === typeof({})) {
    evt.preventDefault();
  }

  // Get mortgage details from user inputs
  var mortgageDetails = {
    'price': $('#list-price').html().replace(/\D/g,''),
    'hoa': $('#hoa').html().replace(/\D/g,''),
    'rate': $('#mortgage-rate').val(),
    'downpayment': $('#mortgage-downpayment').val(),
    'loan': $('#mortgage-loan-type').val()
  };

  $.get('/calculator', mortgageDetails, updateMonthlyPayment);
}


// Returns a monthly mortgage and total mortgage amount
function updateMonthlyPayment(rate) {
  $('#monthly-payment')
    .animate({opacity: 0, left: -5})
    .html(rate.mortgage)
    .animate({opacity: 100, left: 0});
  $('#total-payment')
    .html(rate.total_mortgage);
  calculatePotentialIncome();
}


// Returns nearby average rent rates by bedroom or sqft
function updateAvgRentRate(avgRent){
  getMonthlyPayment();
  calculateDownpaymentPercentage();

  // Get the current bedroom and sqft rates
  var byBedroom = formatCurrency(avgRent['avg_rent_by_br']);
  var bySqft = formatCurrency(avgRent['avg_rent_by_sqft']);

  $('#avg-rent-by-br')
    .animate({opacity: 0, left: -5})
    .html(byBedroom)
    .animate({opacity: 100, left: 0});
  $('#avg-rent-by-sqft').html(bySqft);
}


// If changes in monthly mortgage value, recalculates potential income
function calculatePotentialIncome(){
  var potentialIncome = Number($('#avg-rent-by-br').html().replace(/\D/g,''))
                      - Number($('#monthly-payment').html().replace(/\D/g,''));
  $('#potential-income').html(potentialIncome);
}

