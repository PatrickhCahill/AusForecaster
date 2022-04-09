$(document).ready(function () {
    $("input[name$='btnradio']").click(function () {
        var test = $(this).val();
        $("div.desc").hide();
        $("#probv" + test).show();
    });
}); 