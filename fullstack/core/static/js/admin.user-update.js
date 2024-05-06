$(document).ready(() => {
  $("button#user-change").on("click", (e) => {
    id = $("input[type='hidden']").val();
    login = $('input[name="login"]').val();
    console.log(login);
    $.ajax({
      method: "POST",
      url: "/admin/user/login_check",
      dataType: "html",
      data: {
        id: id,
        login: login,
      },
      success: () => {
        roles = [];
        $(".form-role__input:checked").each((i, input) => {
          roles.push(`${$(input).attr("name")}`);
        });
        console.log(roles);

        $.ajax({
          method: "POST",
          dataType: "html",
          data: {
            fio: $('input[name="fio"]').val(),
            role: roles.join(" "),
            login: $('input[name="login"]').val(),
            password: $("input[name=password]").val(),
          },
          success: (data) => {
            alert(JSON.parse(data).message)
            window.location.replace('/admin')
          },
        });
      },
      error: (xhr, status, error) => {
        var err = JSON.parse(xhr.responseText);
        alert(err.error);
      },
    });
  });
});
