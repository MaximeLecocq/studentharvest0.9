// document.getElementById('reset-filters').addEventListener('click', function() {
//     // Clear all inputs and checkboxes
//     document.getElementById('id_title').value = '';
//     document.getElementById('id_city').value = '';
    
//     // Uncheck all checkboxes
//     document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
//         checkbox.checked = false;
//     });

//     // Submit the form to reload the page without filters
//     document.querySelector('form').submit();
// });


document.getElementById('reset-filters').addEventListener('click', function() {
    const url = new URL(window.location.href);

    // Clear the query string parameters (filters)
    url.searchParams.delete('title');
    url.searchParams.delete('city');
    url.searchParams.delete('categories');
    
    // Optionally reset the form fields visually
    document.querySelector('form').reset();

    // Redirect the page to the URL without filters
    window.location.href = url.pathname;
});


// document.getElementById('reset-filters').addEventListener('click', function() {
//     const form = document.querySelector('form');
//     form.reset();  // Reset the form fields

//     // Clear the URL query parameters
//     const url = new URL(window.location.href);
//     url.search = '';  // Remove all search parameters
//     window.history.pushState({}, '', url.href);

//     // Reload the page to reflect the changes
//     window.location.reload();  // Reload the page after resetting the filters
// });
