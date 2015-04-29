
$(document).ready(function() {

        // JQuery code to be added in here.
    $(".form_datetime").datetimepicker({
            autoclose: true,
            format: "yyyy-mm-dd hh:ii",

    });
     $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");
    });
});

