$(document).ready(function () {
    var oldTitle = document.title;
    var titleCount = 0;
    var isChangedTitle = false;
    var isFirstOpenPage = true;
    var newRequests = [];
    var tempRequests = [];
    var allRequests = [];

    function getRequests() {
        $.ajax({
            url: '/requests/',
            success: function (response) {
                newRequests = JSON.parse(response);
                _.each(newRequests, function (item) {
                    if (!$('#request-' + item.pk).length) {
                        $('.requests-menu').append(
                            '<p class="request-simple" data-id="' + item.pk + '" id="request-' + item.pk + '">' +
                            '<span class="is-new">[N] </span>' + item.fields.page + '</p>'
                        );
                        titleCount += 1;
                        tempRequests.push(item);
                        allRequests.push(item)
                    }
                });
            },
            complete: function () {
                if (isChangedTitle) {
                    if (titleCount) {
                        $(document).attr('title', titleCount + ' request(s)')
                    }
                }
                if (isFirstOpenPage) {
                    isFirstOpenPage = false;
                    isRead();
                }
            }
        });
    }

    getRequests();

    $(window).focus(function () {
        isChangedTitle = false;
        $(document).attr('title', oldTitle);
        isRead();
    }).blur(function () {
        isChangedTitle = true;
    });

    function isRead() {
        _.each(tempRequests, function (item) {
            $.ajax({
                url: '/requests/',
                type: 'POST',
                dataType: 'json',
                data: {csrfmiddlewaretoken: csrftoken, request_pk: item.pk},
                success: function (response) {
                    if (response.success) {
                        titleCount -= 1;
                    }
                },
                complete: function () {
                    tempRequests = [];
                }
            });
        });
    }

    $('body').on('click', '.request-simple', function (e) {
        event.preventDefault();
        $(e.toElement).find('.is-new').remove();
        var requestsBody = $('.requests-body');
        var item = _.find(allRequests, function (obj) {
            return obj.pk == $(e.toElement).data('id');
        });
        requestsBody.children().remove();
        requestsBody.append(
            '<div>' +
            '<p>ID: ' + item.pk + '</p>' +
            '<p>Remote address: ' + item.fields.ip + '</p>' +
            '<p>Open page: <a href="' + item.fields.page + '" target="_blank">' + item.fields.page + '</a></p>' +
            '<p>Date/Time: ' + item.fields.time + '</p>' +
            '<p>Headers:</p>' +
            '<p>' + item.fields.header + '</p>' +
            '</div>'
        );
    });

    setInterval(function () {
        getRequests();
    }, 1000);
});
