$(document).ready(() => {
  $("#specialisation-create").click(() => {
    $.ajax({
      method: "POST",
      dataType: "html",
      data: {
        name: $("input[name='name']").val(),
        code: $("input[name='specialization_code']").val(),
        opop_id: $("select[name='director_opop_id'] option:selected").val(),
        id: $("select[name='spec-institute'] option:selected").val(),
      },
      success: (data) => {
        alert(JSON.parse(data).message);
        window.location.replace("/admin")
      },
      error: (xhr, status, error) => {
        alert(JSON.parse(xhr.responseText).message);
      },
    });
  });
});
