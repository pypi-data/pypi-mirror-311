$(document).ready(function() {
    $('.hide-toolbar').click(function() {
        $(this).hide();
        $('.show-toolbar').show();
        $('.admin-link').hide();
    });

    $('.show-toolbar').click(function() {
        $(this).hide();
        $('.hide-toolbar').show();
        $('.admin-link').show();
    });
});
