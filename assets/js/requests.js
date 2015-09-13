$(document).ready(function () {
    var oldTitle = document.title;
    var titleReqCount = 0;
    var dataRequests = {};
    var getRequests = function () {
        $.ajax({
            url: '/requests/'
        }).done(function (response) {
            dataRequests = JSON.parse(response);
            _.each(dataRequests, function (item) {
                if (!$('#request-' + item.pk).length) {
                    $('.requests-menu').append(
                        '<p class="request-simple" data-id="' + item.pk + '" id="request-' + item.pk + '">' +
                        '<span class="is-new">[N] </span>' + item.fields.page + '</p>'
                    );
                    titleReqCount += 1;
                }
            });
        });
        changeTitle();
    };

    var changeTitle = function () {
        if (titleReqCount) {
            $(document).attr('title', titleReqCount + ' request(s)')
        } else {
            $(document).attr('title', oldTitle)
        }
    };

    var isRead = function (pk) {
        $.ajax({
            url: '/requests/',
            type: 'POST',
            dataType: 'json',
            data: {csrfmiddlewaretoken: csrftoken, request_pk: pk},
            success: function (response) {
                if (response.success) {
                    titleReqCount -= 1;
                }
            }
        })
    };

    $('body').on('click', '.request-simple', function (e) {
        event.preventDefault();
        $(e.toElement).find('.is-new').remove();
        var requestsBody = $('.requests-body');
        var requestId = $(e.toElement).data('id');
        var dataRequest = _.find(dataRequests, function (obj) {
            return obj.pk == requestId
        });
        requestsBody.children().remove();
        requestsBody.append(
            '<div>' +
            '<p>ID: ' + dataRequest.pk + '</p>' +
            '<p>Remote address: ' + dataRequest.fields.ip + '</p>' +
            '<p>Open page: <a href="' + dataRequest.fields.page + '" target="_blank">' + dataRequest.fields.page + '</a></p>' +
            '<p>Date/Time: ' + dataRequest.fields.time + '</p>' +
            '<p>Headers:</p>' +
            '<p>' + dataRequest.fields.header + '</p>' +
            '</div>'
        );
        isRead(requestId);
    });

    getRequests();
    setInterval(function () {
        getRequests();
    }, 1000);
});
