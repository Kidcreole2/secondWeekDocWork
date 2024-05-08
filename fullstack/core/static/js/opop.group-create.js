$(document).ready(() => {
    $.ajax({
        method: "POST",
        dataType: "html",
        data: {
            name: $("input[name='name']").val(),
            specialization_id: $("select[name='specialization_id'] option:selected").val(),
            course: $("input[name='course']").val(),
            form: $("select[name='form'] option:selected").val()
        }, 
        success: () => {
            alert("Группа была успешно создана")
        },
        error: (xhr, status, error) =>  {
            alert(JSON.parse(xhr.responseText).message)
        }
    })
})