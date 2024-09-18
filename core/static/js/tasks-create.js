'use strict';

$(document).ready(() => {
  $("button#tasks-create").click(() => {
    alert($(".tasks > form").length)
    $(".tasks > form").each(function (i, el) {
      let date = $(el).find("input[name='date']").val()
      let name = $(el).find("input[name='name']").val()
      $.ajax({
        async: false,
        method: "POST",
        dataType: "html",
        data: {
          date: date,
          name: name,
        },
        error: (xhr, status, error) => {
          console.log(error)
        },
        success: (data) => {
          console.log(data)
        },
      })
    });

    window.location.replace($("a#goBack").attr("href"))
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
