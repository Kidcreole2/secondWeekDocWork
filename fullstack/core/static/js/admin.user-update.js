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
        login: login
      }, 
      success: () => {
        console.log($('form#change').serialize())
        $.ajax({
            method: "POST",
            dataType: "html",
            data: $("form#change").serialize(),
            success: (data) => {
                console.log(data)
            }
        })
      },
      error: (xhr, status, error) => {
        var err = JSON.parse(xhr.responseText) ;
        alert(err.error);
      },
    });
  });
});
