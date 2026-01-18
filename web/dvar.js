$(document).ready(function(){
    $(".main").css("height",$(document).height());
    $(".side").css("height",$(document).height());
    $(".word").on("click", function() {
        var idx = $(this).attr("id");
        $("#d0").html(j2[idx].d0);
    });
});
