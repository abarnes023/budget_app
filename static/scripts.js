
// Update budget values when the month is changed

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
            smiles(data.a_rent, data.a_income, "rent");
            smiles(data.a_save, data.a_income, "saved");
        });
    });
});

// Call smileChange function when income, rent, or savings values changed

$("#a_income, #a_rent, #a_save").onchange = smileChange();

function smileChange() {
    // Set variables
    var a_income = document.getElementById("a_income").value;
    var a_rent = document.getElementById("a_rent").value;
    var a_save = document.getElementById("a_save").value;
    
    smiles(a_rent, a_income, "rent");
    smiles(a_save, a_income, "saved");
}

// Calculate the percent an expense is of the income and update smile

function smiles(expense, income, smile) {
    // calculate spending percentage
    var percent = (parseFloat(expense))/ (parseFloat(income)) * 100;
    
    // set smiles based on spending percent
    if (smile == "rent") {
        if (percent >= 0 && percent < 25) {
            document.getElementById(smile).innerHTML = '<span style="color:green; font-size: 20px">&#9786;</span><span style="color:green;"> You\'re looking great!</span>';
        }
        else if (percent >= 25 && percent < 35) {
            document.getElementById(smile).innerHTML = '<span style="color:#e1e509; font-size: 20px">&#9863;</span><span style="color:#e1e509;"> Rent spending is okay</span>';
        }
        else if (percent >= 35) {
            document.getElementById(smile).innerHTML = '<span style="color:red; font-size: 20px">&#9785;</span><span style="color:red;"> Spending too much on rent</span>';
        }
        else {
            document.getElementById(smile).innerHTML = '<span style="color:gray;">Enter actual income and rent</span>';
        }
    }
    else if (smile == "saved") {
        if (percent >= 0 && percent < 10) {
            document.getElementById(smile).innerHTML = '<span style="color:red; font-size: 20px">&#9785;</span><span style="color:red;"> Cut back and save more</span>';
        }
        else if (percent >= 10 && percent < 20) {
            document.getElementById(smile).innerHTML = '<span style="color:#e1e509; font-size: 20px">&#9863;</span><spanstyle="color:#e1e509;"> Consider saving a bit more</span>';
        }
        else if (percent >= 20) {
            document.getElementById(smile).innerHTML = '<span style="color:green; font-size: 20px">&#9786;</span><span style="color:green;"> Great job saving!</span>';
        }
        else {
            document.getElementById(smile).innerHTML = '<span style="color:gray;">Enter actual income and rent</span>';
        }
    }
}