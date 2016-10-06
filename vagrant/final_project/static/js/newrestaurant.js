function validForm()
{
    var name=document.forms["newRestaurant"]["name"].value;
    return !(name==null || name=="")
}

function create(htmlStr) {
    var element = document.getElementById("newForm");
    element.insertAdjacentHTML( 'afterend', htmlStr )
}

$("input[type='text'], textarea").on("input", function () {
    var isValid = validate();
    if (isValid) {
      jQuery("#subnewtide").removeAttr("disabled");
    } else {
        jQuery("#subnewtide").attr("disabled", "disabled");
    }
});