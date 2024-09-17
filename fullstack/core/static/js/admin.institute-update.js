$("button#submit-data").click((e) => {
    e.preventDefault()
    console.log("123")
    $.ajax({
        method: "POST",
        dataType: "html",
        url: "/admin/institute/name_check",
        data: {
            name: $("input[name='name']").val(),
            id: $("input[name='id']").val(),
        },
        success: (data) => {
            $.ajax({
                method: "POST",
                dataType: "html",
                data: {
                    name: $("input[name='name']").val(),
                },
                success: (data) => {
                    alert(JSON.parse(data).message);
                },
                // error: (xhr, status, error) => {
                //     alert(JSON.parse(xhr.responseText).message);
                // },
            });
        }
    })
})