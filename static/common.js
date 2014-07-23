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
        $('.component:not(.grouped)').animate({
            opacity: "0.1"
        }, 500);
    } else {
        $('.component:not(.grouped)').animate({
            opacity: "0.6"
        }, 500);
    }
}

function showOrHideIssuesDiv(component, version, issueStatus) {
    version = version.replace(".","");
    $("#" + component + "-" + version + "-" + issueStatus).slideToggle();
}

/* Pull requests functions */

$( document ).ready(function() {
$(".branch-name").click( function(){
    $(this).parent().next(".pull-content").slideToggle(100);
})
});

/* Key mappings */
$( document ).on( 'keydown', function ( e ) {
    if ( e.keyCode === 27 ) { // ESC
        $('.tickets').hide('clip');
    }
});

/* Manage pull requests retesting */
function sendRetestQuery(current_org, current_repo, current_pull_number) {
    $.get( "retest", { organization: current_org, repository: current_repo, pull_number: current_pull_number }, function(data) {
    if (data == "success") {
        $("#confirmation-dialog").hide();
        $("#success-dialog").show(100).delay(1000).hide(100);
    } else {
        $("#confirmation-dialog").hide();
        $("#error-dialog").show(100).delay(3000).hide(100);
    }
});
}

function showConfirmationDialog(organization, repository, pull_number) {
    $("#confirmation-dialog").slideToggle(100);

    $("#confirmation-dialog #confirm-button").unbind('click');
    $("#confirmation-dialog #confirm-button").click(function() {
        sendRetestQuery(organization, repository, pull_number);
    });

    $("#confirmation-dialog #cancel-button").unbind('click');
    $("#confirmation-dialog #cancel-button").click(function() {
        $("#confirmation-dialog").hide(100);
    });
}
