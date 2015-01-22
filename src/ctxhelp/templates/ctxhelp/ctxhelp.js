$(function(){
    $('[data-toggle="popover"]')
        .popover({
            template: '<div class="popover" role="tooltip"><div class="arrow"></div><span class="close pull-right">&times;</span><div class="popover-content"></div></div>'
        })
        .on('shown.bs.popover', function(e){
            var popover = $(this);
            popover.parent().find('div.popover .close').on('click', function(e){
                popover.popover('hide');
            });
        })
        .on('show.bs.popover', function (e) {
            if ($(this).hasClass('popover-show')) {
                $(this).removeClass('popover-show'); // skip first time, i.e. on page load
            } else {
                var url = $(this).data('showurl');
                if (url) {
                    $.ajax(url);
                }
            }
        })
        .on('hide.bs.popover', function (e) {
            var url = $(this).data('hideurl');
            if (url) {
                $.ajax(url);
            }
        })
        .filter('.popover-show').popover('show');
});