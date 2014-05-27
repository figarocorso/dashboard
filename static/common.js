function groupFolding(group) {
    $('.'+group).slideToggle();
    $('#'+group+'_grouped').toggleClass('important');
    toggleFocusToNonGroupComponents();
    $('.grouped').animate({
        opacity: "0.6"
    }, 500);
}

function toggleFocusToNonGroupComponents() {
    if ($('div[id*="_grouped"]').hasClass('important')) {
//        $('.component').addClass('not-focus');
        $('.component:not(.grouped)').animate({
            opacity: "0.1"
        }, 500);
    } else {
//        $('.component').removeClass('not-focus');
        $('.component:not(.grouped)').animate({
            opacity: "0.6"
        }, 500);
    }
}
