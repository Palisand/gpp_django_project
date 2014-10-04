$('.selectpicker').selectpicker({
//    size: 10
});

$('.popover-hover').popover( {
    trigger: 'hover',
    html: true,
    placement: 'top',
});

$('.endless_page_current').wrap('<li class="active"></li>')
$('.endless_page_link').wrap('<li></li>')
$('.endless_separator').wrap('<li class="disabled"></li>')