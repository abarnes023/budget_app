$(function() {
    $('a#set_month').bind('click', function() {
        $.getJSON(Flask.url_for("month"), {
            month: $('input[name="month"]').val()
        }, function(data) {
            document.getElementById("monthTitle").innerHTML = document.getElementById("month").value,
            document.getElementById("e_income").value = data.e_income,
            document.getElementById("a_income").value = data.a_income,
            document.getElementById("e_rent").value = data.e_rent,
            document.getElementById("a_rent").value = data.a_rent,
            document.getElementById("e_util").value = data.e_util,
            document.getElementById("a_util").value = data.a_util,
            document.getElementById("e_food").value = data.e_food,
            document.getElementById("a_food").value = data.a_food,
            document.getElementById("e_ent").value = data.e_ent,
            document.getElementById("a_ent").value = data.a_ent,
            document.getElementById("e_save").value = data.e_save,
            document.getElementById("a_save").value = data.a_save;
        });
    });
});