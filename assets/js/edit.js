$(document).ready(function () {

    function readURL(input) {

        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#photo-preview').attr('src', e.target.result);
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#id_photo").change(function () {
        readURL(this);
    });

    $('body').on('click', function () {
        $('#bio-messages > *').remove();
        $('.form-group > .text-danger').remove();
    });

    var options = {
        beforeSend: function () {
            $('#bio-form').find('button').prop('disabled', true);
            $('#preloader').removeClass('hidden');
        },
        success: function (response) {
            var resp = JSON.parse(response);
            if (resp.success) {
                $('#bio-messages').append('<p class="text-success">Changes have been save</p>')
            } else {
                _.each(resp.errors, function (error, field) {
                    $('input[name=' + field + ']').parent().append('<p class="text-danger">' + error + '</p>');
                });
            }
        },
        complete: function () {
            $('#bio-form').find('button').prop('disabled', false);
            $('#preloader').addClass('hidden');
        }
    };
    $('#bio-form').ajaxForm(options);
});
