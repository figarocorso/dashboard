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

    $("#filter-failure").click(function(){
        $(".build-failure").toggle();
        $("#filter-failure").toggleClass("unchecked");
    });

    $("#filter-sucess").click( function(){
        $(".build-success").toggle();
        $("#filter-sucess").toggleClass("unchecked");
    });

    $("#filter-none").click( function(){
        $(".build-none").toggle();
        $("#filter-none").toggleClass("unchecked");
    });

    $(".filter-btn").click( function(){
        $(this).next(".dropdown").slideToggle(100);
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
        $("#confirmation-dialog").fadeOut(200);
        $("#success-dialog").show(100).delay(1000).fadeOut(100, function(){
            $("#fade").fadeOut(100);
        });
    } else {
        $("#confirmation-dialog").hide();
        $("#error-dialog").show(100).delay(3000).hide(100, function(){
            $("#fade").fadeOut(200);
        });
    }
});
}

function showConfirmationDialog(organization, repository, pull_number) {
    $("#fade").fadeIn(200)
    $("#confirmation-dialog").fadeIn(200);

    $("#confirmation-dialog #confirm-button").unbind('click');
    $("#confirmation-dialog #confirm-button").click(function() {
        sendRetestQuery(organization, repository, pull_number);
    });

    $("#confirmation-dialog #cancel-button").unbind('click');
    $("#confirmation-dialog #cancel-button").click(function() {
        $("#confirmation-dialog").fadeOut(200, function(){
            $("#fade").fadeOut(200);
        });
    });
}
