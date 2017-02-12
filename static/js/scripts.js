"use strict";

// Returns price of listing
$('#search-bar').on('submit', getPrice);

function getPrice(evt) {
    evt.preventDefault();
    var fullAddress = { 'address': $('#address-search').val(),
                        'citystatezip': $('#citystatezip-search').val()
                      };
    $('#list-price').html("");
    $('#mortgage-rate').val("");
    $('#mortgage-downpayment').val("");
    $('#neighborhood').html("");
    $.get('/search.json', fullAddress, updatePrice);
}

function updatePrice(listing) {
    // Updates page with a price if list price is available,
    // Zillow price estimate if unit is off-market,
    // or error message if unit address is not found
    var price = listing.price;
    var twenty_percent_downpayment = Math.round(parseInt(price.replace(/\D/g,''))*0.20)
    //.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    var neighborhood = listing.neighborhood

    if (listing.response === 100){
        $('#list-price').html(price);
        $('#mortgage-downpayment').val(twenty_percent_downpayment);
        $('#neighborhood').html(neighborhood);
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

// Closes alerts on click
$('#div-message').on('click', function() {
    $('#div-message').html('')
    $('#div-message').removeClass('btn-info');
    $('#div-message').attr('hidden', 'hidden')
});

// Returns mortgage rate
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
