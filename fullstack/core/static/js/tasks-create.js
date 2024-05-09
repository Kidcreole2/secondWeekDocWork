$(document).ready(() => {
    $("button#tasks-create").click(() => {
        $('.tasks > form').each(() => {
            $.ajax({
                method: "POST",
                dataType: "html",
                data: {
                    date: $(this).children("input[name='date']").val(),
                    name: $(this).children("input[name='name']").val()
                }, 
            })
        })

        window.location.replace($("a#goBack").attr("href"))
    })

    $("button#add").click(() => {
        $(".tasks").append(`<form>
        <div>
            <label>Название</label>
            <input type="text" name="name">
        </div>
        <div>
            <label>Дата</label>
            <input type="date" name="date">
        </div>
    </form>`)
    })
})