$(document).ready(() => {
    let d = []
    $(".start-practice").submit(() => {
        d.push(submitForm.call(this))
    });
    $.ajax({
      method: "POST",
      url: "/opop_practice_start",
      data = {"data": d},
      success: () => {
        alert("Данные успешно сохранены")
        window.location.replace("/opop_practice_start");
      },
    });
  });