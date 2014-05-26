function groupFolding(group) {
    $('.'+group).slideToggle();
    $('.component').toggleClass('not-focus');
    $('.grouped').toggleClass('focus');
    $('#'+group+'_grouped').toggleClass('important');
    $('div[id*="group"]').slideToggle(0);
    $('#'+group+'_grouped').slideToggle(0);
}
