$(document).ready(() => {
    $("#student-practice-change").click(() => {
        let place_name = $("input[name=place_name]").val()
        let place_name_short = $("input[name=place_name_short]").val()
        $.ajax({
            method: "POST",
            dataType: "html",
            data: {
              place_city: $("input[name='place_city'").val(),
              place_address: $("input[name='place_address']").val(),
              place_name: place_name,
              place_name_short: (place_name_short !== "") ?  place_name_short : place_name,
              passed: ($("select[name='passed'] option:selected").val() === "Да") ? true : false,
              grade: $("select[name='grade'] option:selected").val(),
              demonstrated_qualities: $("input[name='demonstrated_qualities']").val(),
              overcoming_difficulties: $("select[name='overcoming_difficulties'] option:selected").val(),
              work_volume: $("select[name='work_volume'] option:selected").val(),
              remarks: $("input[name='remarks']").val(),
              reason: $("input[name='reason']").val()
            },
            success: () => {
                alert("Данные успешно переданы")
                window.location.replace('/studentPractice/student')
            }
        })
    })
})