$(document).ready(() => {
  $(".users-head-tools__button+.toggle").on("click", () => {
    $(".users-list").toggle();
    $(this).toggleClass("hided");
  });

  $(".institutes-head-tools__button+.toggle").on("click", () => {
    $(".institutes-list").toggle();
    $(this).toggleClass("hided");
  });

  $(".users-list-tools__button.delete").on("click", (e) => {
    id = e.target.id;
    $.ajax({
      method: "POST",
      url: `/admin/users/delete/${id}`,
      dataType: "html",
      success: () => {
        $(`li#${id}`);
        alert("Zaebis");
      },
      error: (xhr, status, error) => {
        var err = "(" + xhr.responseText + ")";
        alert(err);
      },
    });
  });

  $(".institutes-list-tools__button.delete").on("click", (e) => {
    id = e.target.id;
    $.ajax({
      method: "POST",
      url: `/admin/institutes/delete/${id}`,
      dataType: "html",
      success: () => {
        alert("Zaebis");
      },
      error: (xhr, status, error) => {
        var err = "(" + xhr.responseText + ")";
        alert(err);
      },
    });
  });

  $(".users-head-tools__button.add").on("click", () => {
    window.location.replace("/admin/user/create");
  });
});
