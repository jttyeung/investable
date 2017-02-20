"use strict";

// Returns price of listing
$('#search-bar').on('submit', getPrices);

function getPrices(evt) {
    evt.preventDefault();

    // Gets the full address entered by the user
    var fullAddress = { 'address': $('#address-search').val(),
                        'citystatezip': $('#citystatezip-search').val()
                      };

    // Resets values after each search
    $('#list-price').html("");
    $('#mortgage-rate').val("");
    $('#mortgage-downpayment').val("");
    $('#neighborhood').html("");

    // Gets the price of the listing
    $.get('/search.json', fullAddress, updatePrice).success(
    // Gets the rent average for that listing
    $.get('/rent.json', fullAddress, updateAvgRentRate);)

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


// want to get the average rent when the search button is clicked
// then, if the user changes the avg rent filter, then it should update the average rent
// if a user changes the filter again, it should change it to the selected filter

// Returns average rent rate
// $('#search-bar').on('submit', getAvgRentRate);
$('#avg-rent-filter').on('change', updateAvgRentRate);

// function getAvgRentRate(evt){
//     evt.preventDefault();
    // // Gets the dropdown value of average rent filter
    // var avgRentFilter = {
    //     'filter': $('#avg-rent-filter').val()
    // };


//     $.get('/rent.json', avgRentFilter, updateAvgRentRage);
// }

function updateAvgRentRate(avgRent){
    byBedroom = avgRent['avg_rent_by_br']
    bySqft = avgRent['avg_rent_by_sqft']

    if ($('#avg-rent-filter').val() == 'bedrooms') {
        $('avg-rent').html(byBedroom);
    } else {
        $('avg-rent').html(bySqft);
    }
}
