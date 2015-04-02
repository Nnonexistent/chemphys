$(function(){
    $('textarea').autosize();
});

$(window).load(function() {
    console.log('remove preload');
    $("body").removeClass("preload");
});
