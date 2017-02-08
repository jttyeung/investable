"use strict";

// Returns price of listing to the page

$('#search-bar').on('submit', getPrice);

function getPrice(evt) {
    evt.preventDefault();
    var fullAddress = { 'address': $('#address-search').val(),
                        'citystatezip': $('#citystatezip-search').val()
                      };
    $.get('/search', fullAddress, updatePrice);
}

function updatePrice(price) {
    $('#list-price').html(price);
}
