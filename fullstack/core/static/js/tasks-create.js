$(document).ready(() => {
  $("button#tasks-create").click(() => {
    $(".tasks > form").each((i, el) => {
      $.ajax({
        method: "POST",
        dataType: "html",
        data: {
          date: $(el).find("input[name='date']").val(),
          name: $(el).find("input[name='name']").val(),
        },
      });
    });

    window.location.replace($("a#goBack").attr("href"));
  });

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
    </form>`);
  });
});
