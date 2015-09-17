$(document).ready(function () {
    var oldTitle = document.title;
    var titleCount = 0;
    var dataRequests = [];
    var newRequests = null;

    var getRequests = function () {
        $.ajax({
            url: '/requests/'
        }).done(function (response) {
            newRequests = JSON.parse(response);
            _.each(newRequests, function (item) {
                if (!$('#request-' + item.pk).length) {
                    $('.requests-menu').append(
                        '<p class="request-simple" data-id="' + item.pk + '" id="request-' + item.pk + '">' +
                        '<span class="is-new">[N] </span>' + item.fields.page + '</p>'
                    );
                    titleCount += 1;
                    dataRequests.push(item);
                }
            });
        });
        changeTitle();
    };

    $(window).focus(function () {
        if (dataRequests.length) {
            isRead();
        }
        $(document).attr('title', oldTitle);
    });

    var changeTitle = function () {
        if (titleCount) {
            $(document).attr('title', titleCount + ' request(s)')
        }
    };

    var isRead = function () {
        _.each(dataRequests, function (item) {
            $.ajax({
                url: '/requests/',
                type: 'POST',
                dataType: 'json',
                data: {csrfmiddlewaretoken: csrftoken, request_pk: item.pk},
                success: function (response) {
                    if (response.success) {
                        titleCount -= 1;
                    }
                }
            })
        });
        dataRequests = [];
    };

    $('body').on('click', '.request-simple', function (e) {
        event.preventDefault();
        $(e.toElement).find('.is-new').remove();
        var requestsBody = $('.requests-body');
        var newRequest = _.find(newRequests, function (obj) {
            return obj.pk == $(e.toElement).data('id');
        });
        requestsBody.children().remove();
        requestsBody.append(
            '<div>' +
            '<p>ID: ' + newRequest.pk + '</p>' +
            '<p>Remote address: ' + newRequest.fields.ip + '</p>' +
            '<p>Open page: <a href="' + newRequest.fields.page + '" target="_blank">' + newRequest.fields.page + '</a></p>' +
            '<p>Date/Time: ' + newRequest.fields.time + '</p>' +
            '<p>Headers:</p>' +
            '<p>' + newRequest.fields.header + '</p>' +
            '</div>'
        );
    });

    getRequests();
    setInterval(function () {
        getRequests();
    }, 1000);
});
