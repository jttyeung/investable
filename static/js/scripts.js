"use strict";

// Returns price of listing to the page
$('#search-bar').on('submit', getPrice);

function getPrice(evt) {
    evt.preventDefault();
    var fullAddress = { 'address': $('#address-search').val(),
                        'citystatezip': $('#citystatezip-search').val()
                      };
    $.get('/search.json', fullAddress, updatePrice);
}

function updatePrice(listing) {
    var price = listing.price;

    if (listing.response === 100){
        $('#list-price').html(price);
        console.log('hello');
    } else if (listing.response === 200) {
        $('#div-message').html('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' + price);
        $('#div-message').addClass('btn-info');
        $('#div-message').removeAttr('hidden');
        console.log('second');
    } else if (listing.response === 300){
        $('#div-message').html('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' + price);
        $('#div-message').addClass('btn-danger');
        $('#div-message').removeAttr('hidden');
        console.log('everything else');
    } else {
        console.log('something went terribly wrong')
    }
}

// Closes alerts on click

$('#div-message').on('click', function() {
    $('#div-message').html('')
    $('#div-message').removeClass('btn-info');
    $('#div-message').attr('hidden', 'hidden')
    console.log('whatever');
})
