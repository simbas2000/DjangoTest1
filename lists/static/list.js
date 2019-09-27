function isInputValid(text)
{
    return text.length;
}

function lvalidator_init() {
    var c_name = '.user_input_form'
    $(c_name).find("input").on("keypress", function () {
        $(c_name).find("input").removeClass('is-invalid').removeClass('is-valid')
        $(c_name).find(".invalid-feedback").remove();
    })
    $(c_name).find("input").on("blur", function () {
        $(c_name).find("input").each(function () {
            if (!isInputValid($(this).val())) {
                $(this).addClass("is-invalid");
                if(!$(c_name).find(".invalid-feedback").text().includes("empty")) {
                    $(c_name).append(`
                        <div class="invalid-feedback">
                            <div class="float-left">
                               You can't have an empty list item
                            </div>
                         </div>
                    `)
                }
            }
        })
    })
}

$(document).ready(lvalidator_init());