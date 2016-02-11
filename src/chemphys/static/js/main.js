$(function(){
    $('textarea').autosize();
    $('[data-toggle="tooltip"]').tooltip();
    $('.nav-tabs').stickyTabs();
});

$(window).load(function() {
    $("body").removeClass("preload");
});
