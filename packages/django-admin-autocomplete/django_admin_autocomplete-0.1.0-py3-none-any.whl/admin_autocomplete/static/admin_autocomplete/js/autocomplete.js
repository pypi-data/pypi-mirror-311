'use strict';

window.addEventListener('load', function() {
    if (typeof django === 'undefined' || !django.jQuery) {
        console.error('Django jQuery not found');
        return;
    }

    const $ = django.jQuery;
    console.log('Admin autocomplete script loaded');
    
    const searchInput = document.querySelector('#searchbar');
    console.log('Search input found:', searchInput);
    if (!searchInput) return;

    // Create and append the autocomplete container
    const autocompleteContainer = $('<div id="admin-autocomplete-results" class="admin-autocomplete-results"></div>');
    $(searchInput).after(autocompleteContainer);
    console.log('Autocomplete container created');

    let currentRequest = null;

    $(searchInput).on('input', function() {
        console.log('Input event triggered');
        const term = $(this).val();
        console.log('Search term:', term);

        if (currentRequest) {
            currentRequest.abort();
        }

        if (!term) {
            autocompleteContainer.empty().hide();
            return;
        }

        currentRequest = $.ajax({
            url: 'autocomplete/',
            data: { term: term },
            success: function(data) {
                console.log('Received data:', data);
                autocompleteContainer.empty();

                if (data.results.length > 0) {
                    data.results.forEach(function(item) {
                        const resultItem = $('<div class="autocomplete-item"></div>')
                            .text(item.text)
                            .data('url', item.url)
                            .on('click', function() {
                                window.location.href = $(this).data('url');
                            });
                        autocompleteContainer.append(resultItem);
                    });
                    autocompleteContainer.show();
                } else {
                    autocompleteContainer.hide();
                }
            },
            error: function(xhr, status, error) {
                console.error('Error fetching results:', error);
                autocompleteContainer.empty().hide();
            }
        });
    });

    // Hide results when clicking outside
    $(document).on('click', function(e) {
        if (!$(e.target).closest('#admin-autocomplete-results, #searchbar').length) {
            autocompleteContainer.hide();
        }
    });

    // Handle keyboard navigation
    $(searchInput).on('keydown', function(e) {
        const items = autocompleteContainer.find('.autocomplete-item');
        const current = autocompleteContainer.find('.selected');
        
        switch(e.keyCode) {
            case 40: // Down arrow
                e.preventDefault();
                if (!current.length) {
                    items.first().addClass('selected');
                } else {
                    current.removeClass('selected').next().addClass('selected');
                }
                break;
            case 38: // Up arrow
                e.preventDefault();
                if (!current.length) {
                    items.last().addClass('selected');
                } else {
                    current.removeClass('selected').prev().addClass('selected');
                }
                break;
            case 13: // Enter
                e.preventDefault();
                if (current.length) {
                    window.location.href = current.data('url');
                }
                break;
            case 27: // Escape
                autocompleteContainer.hide();
                break;
        }
    });
});
