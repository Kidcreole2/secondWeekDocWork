$(document).ready(() => {
    $("#student-practice-change").click(() => {
        place_name = $("input[name=place_name]").val()
        place_name_short = $("input[name=place_name_short]").val()
        $.ajax({
            method: "POST",
            dataType: "html",
            data: {
              place_city: $("input[name='place_city'").val(),
              place_address: $("input[name='place_address']"),
              place_name: $("input[name='place_name']").val(),
              place_name_short: (place_name_short !== "") ?  place_name_short : place_name,
            },
            success: () => {
                alert("Данные успешно переданы")
                window.location.replace('/studentPractice/student')
            }
        })
    })
})