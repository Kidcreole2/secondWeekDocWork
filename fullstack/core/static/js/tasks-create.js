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
    $(".tasks").append(`<form class="col-sm-4 edit-form new-form">
    <div class="form__content">
        <label class="text-white fs-6">Название</label>
        <input class="form-control" type="text" name="name">
    </div>
    <div class="form__content">
        <label class="text-white fs-6">Дата</label>
        <input class="form-control" type="date" name="date">
    </div>
    </form>`);
  });
});
