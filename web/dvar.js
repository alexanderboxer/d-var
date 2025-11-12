$(document).ready(function(){
    $(".word").on("click", function() {
        var idx = $(this).attr("id");
        alert(j1[idx].A);
    });
});

const j1 = JSON.parse('{"1.1.1.1": {"A": 1, "B": 2}, "1.1.1.2": {"A": 15, "B": 16}}');


