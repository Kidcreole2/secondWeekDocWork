$(document).ready(() => {
  $("#practice-update").on("click", () => {
    practiceName = $('input[name="name"]').val();
    $.ajax({
      method: "POST",
      url: "/opop/practice_name/check",
      dataType: "html",
      data: {
        name: practiceName,
      },
      error: (xhr, status, errror) => {
        alert(JSON.parse(xhr.responseText).error);
      },
      success: () => {
        start_practice = $('input[name="start_date"]').val();
        end_practice = $('input[name="end_date"]').val();
        type_of_practice = $('select[name="type_of_practice"] option:selected').val();
        kind_of_practice = $('select[name="kind_of_practice"] option:selected').val();
        director_practice_usu = $('select[name="director_practice_usu"] option:selected').val();
        director_practice_company = $(
          'select[name="director_practice_company"] option:selected'
        ).val();
        order = $('input[name="order"]').val();
        recomends = $('input[name="recomendations"]').val();

        groups = [];
        $(".group-checkbox:checked").each((i, el) => {
          group.push($(el).attr("name"));
        });

        $.ajax({
          method: "POST",
          dataType: "html",
          data: {
            name: practiceName,
            start_date: start_practice,
            end_date: end_practice,
            type_of_practice: type_of_practice,
            kind_of_practice: kind_of_practice,
            order: order,
            recomendations: recomends,
            groups: groups.join(" "),
          },
          success: (data) => {
            alert(JSON.parse(data).message);
            window.location.replace("/opop");
          },
        });
      }
    });
  });
});
