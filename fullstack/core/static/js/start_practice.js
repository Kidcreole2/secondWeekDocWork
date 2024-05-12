$(document).ready(() => {
  $("#startPractice").click(() => {
    $("form").each((i, el) => {
      let student_id = $(el).children("input[name='student_id']").val();
      let practice_id = $(el).children("input[name='practice_id']").val();
      let paid = $(el).children("input[name='paid']:checked") ? true : false;
      let kind_of_contract = $(el)
        .find("select[name='kind_of_contract'] option:selected")
        .val();
      let director_of_practice_organization = $(el)
        .find(
          "select[name='director'] option:selected"
        )
        .val();
        console.log(kind_of_contract)
      $.ajax({
        method: "POST",
        url: `/opop/practice/start/${practice_id}`,
        dataType: "html",
        data: {
          student_id,
          paid,
          kind_of_contract,
          director_of_practice_organization,
        },
        success: () => {
            alert("Практика успешно запущенна")
            window.location.replace("/opop")
        },
        error: (xhr, status, error) => {
            alert(xhr.responseText)
        }
      });
    });
  });
});
