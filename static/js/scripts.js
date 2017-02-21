"use strict";

// Page load defaults
// $('#property-details-page').hide()

// Returns price of listing and average rent rate
$('#search-bar').on('submit', getPrices);

function getPrices(evt) {
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

    // Gets the price and nearby average rent of the listing
    $.get('/search.json', fullAddress, updatePrice);
}

function updatePrice(listing) {
    // Updates page with a price if list price is available,
    // Zillow price estimate if unit is off-market,
    // or error message if unit address is not found

    var price = listing.price;
    var twenty_percent_downpayment = Math.round(parseInt(price.replace(/\D/g,''))*0.20);
    //.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    var neighborhood = listing.neighborhood;
    var avgRent = listing['rent_avgs'];

    if (listing.response === 100){
        // Show the property details div
        $('#property-details-page').show()
        // Update the property details information on the page
        $('#list-price').html(price);
        $('#mortgage-downpayment').attr('placeholder', twenty_percent_downpayment);
        $('#neighborhood').html(neighborhood);
        // Get the average rent rate in the surrounding neighborhood
        updateAvgRentRate(avgRent);

    } else if (listing.response === 200) {
        $('#div-message').html('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' + price);
        $('#div-message').addClass('btn-info');
        $('#div-message').removeAttr('hidden');

    } else {
        $('#div-message').html('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' + price);
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
