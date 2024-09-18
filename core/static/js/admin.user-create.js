$(".form-login-post").hide();
$(".form-login-group").hide();

$(document).ready(() => {

  $("select[name='user-type']").change(() => {
    switch ($("select[name='user-type'] option:selected").val()) {
      case "student":
        $(".form-login-group").show();
        $(".form-login-post").hide();
        break;
      default:
        $(".form-login-group").hide();
        $(".form-login-post").show();
        break;
    }
  });

  $("button#user-create").on("click", () => {
    roles = [];
    $(".form-role__checkbox:checked").each((i, el) => {
      roles.push($(el).attr("name"));
    });


    $.ajax({
      method: "POST",
      dataType: "html",
      data: {
        fio: $('input[name="fio"]').val(),
        role: roles.join(" "),
        password: $("input[name='passwordConfirm']").val(),
        login: $("input[name='login']").val(),
        post: $("input[name='post']").val()
      },
      success: (data) => {
        alert(JSON.parse(data).message) 
        window.location.replace("/admin")
      },
      error: (xhr, status, error) => {
        alert(JSON.parse(xhr.responseText).message)
      }
    });
  });
});
