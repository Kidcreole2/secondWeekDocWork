$(document).ready(() => {
  $("#specialisation-update").click(() => {
    $.ajax({
      method: "POST",
      url: "/admin/specialization/name_check",
      dataType: "html",
      data: {
        name: $("input[name='name']").val(),
        id: $("input[name='id']").val(),
      },
      error: (xhr, status, error) => {
        alert(JSON.parse(xhr.responseText).message);
      },
      success: (data) => {
        $.ajax({
          method: "POST",
          dataType: "html",
          data: {
            name: $("input[name='name']").val(),
            code: $("input[name='code']").val(),
            opop_id: $("select[name='director_opop_id'] option:selected").val(),
            institute_id: $(
              "select[name='spec-institute'] option:selected"
            ).val(),
          },
          success: (data) => {
            alert(JSON.parse(data).message);
          },
          error: (xhr, status, error) => {
            alert(JSON.parse(xhr.responseText).message);
          },
        });
      },
    });
  });
});
