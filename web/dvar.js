$(document).ready(function(){
    $(".main").css("height",$(document).height());
    $(".side").css("height",$(document).height());
    $(".word").on("click", function() {
        var idx = $(this).attr("id");
        $("#d0").html(j2[idx].d0);
        $("#d0_instance").html(j2[idx].d0_count[0]);
        $("#d0_total").html(j2[idx].d0_count[1]);
        $("#d1").html(j2[idx].d1);
        $("#d1_instance").html(j2[idx].d1_count[0]);
        $("#d1_total").html(j2[idx].d1_count[1]);
        $("#d2").html(j2[idx].d2);
        $("#d2_instance").html(j2[idx].d1_count[0]);
        $("#d2_total").html(j2[idx].d2_count[1]);
    });
});
