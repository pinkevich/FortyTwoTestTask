$(document).ready(function () {
    var oldTitle = document.title;
    var titleCount = 0;
    var isChangedTitle = false;
    var allRequests = [];

    function getRequests() {
        $.ajax({
            url: '/requests/',
            success: function (response) {
                _.each(JSON.parse(response), function (item) {
                    if (!$('#request-' + item.pk).length) {
                        var N = !item.fields.is_read ? '<span class="is-new">[N] </span>' : '';
                        $('.requests-menu').prepend(
                            '<p class="request-simple" data-id="' + item.pk + '" id="request-' + item.pk + '">' +
                            N + item.fields.page + '</p>'
                        );
                        if (!item.fields.is_read) {
                            titleCount += 1;
                        }
                        allRequests.push(item)
                    }
                });
            }
        });
        if (isChangedTitle && titleCount) {
            $(document).attr('title', titleCount + ' request(s)')
        }
    }

    $(window).focus(function () {
        isChangedTitle = false;
        $(document).attr('title', oldTitle);
    }).blur(function () {
        isChangedTitle = true;
    });

    function isRead(pk) {
        $.ajax({
            url: '/requests/',
            type: 'POST',
            dataType: 'json',
            data: {csrfmiddlewaretoken: csrftoken, request_pk: pk},
            success: function (response) {
                if (response.success) {
                    titleCount -= 1;
                }
            }
        });
    }

    $('body').on('click', '.request-simple', function (e) {
        var target = e.toElement || e.relatedTarget || e.target;
        $(target).find('.is-new').remove();
        var requestId = $(target).data('id');
        var requestsBody = $('.requests-body');
        _.find(allRequests, function (obj) {
            if (obj.pk == requestId) {
                requestsBody.children().remove();
                requestsBody.append(
                    '<div>' +
                    '<p>ID: ' + obj.pk + '</p>' +
                    '<p>Remote address: ' + obj.fields.ip + '</p>' +
                    '<p>Open page: <a href="' + obj.fields.page + '" target="_blank">' + obj.fields.page + '</a></p>' +
                    '<p>Date/Time: ' + obj.fields.time + '</p>' +
                    '<p>Headers:</p>' +
                    '<p>' + obj.fields.header + '</p>' +
                    '</div>'
                );
                isRead(requestId)
            }
        });
    });

    getRequests();
    setInterval(function () {
        getRequests();
    }, 1500);
});
