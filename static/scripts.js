$(function() {
    $('a#set_month').bind('click', function() {
        $.getJSON(Flask.url_for("month"), {
            month: $('#month').val()
        }, function(data) {
            $("#e_income").number(data.e_income),
            $("#a_income").number(data.a_income),
            $("#e_rent").number(data.e_rent),
            $("#a_rent").number(data.a_rent),
            $("#e_util").number(data.e_util),
            $("#a_util").number(data.a_util),
            $("#e_food").number(data.e_food),
            $("#a_food").number(data.a_food),
            $("#e_ent").number(data.e_ent),
            $("#a_ent").number(data.a_ent),
            $("#e_save").number(data.e_save),
            $("#a_save").number(data.a_save);
        });
        return false;
    })
})