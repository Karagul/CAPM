$(function() {
    $('topup').click(function() {
        $.ajax({
            url: '/topup',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});