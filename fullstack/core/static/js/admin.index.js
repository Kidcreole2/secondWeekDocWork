$(document).ready(() => {
  $(".users-head-tools__button.toggle").on("click", () => {
    $(".users-list").toggle(20);
    $(this).toggleClass("hided");
  });

  $(".institutes-head-tools__button.toggle").on("click", () => {
    $(".institutes-list").toggle(20);
    $(this).toggleClass("hided");
  });

  $(".specialization-head-tools__button.toggle").on("click", () => {
    $(".specializations-list").toggle(20);
    $(this).toggleClass("hided");
  });

  $(".users-list-tools__button.delete").on("click", (e) => {
    id = e.target.id;
    $.ajax({
      method: "POST",
      url: `/admin/user/delete/${id}`,
      dataType: "html",
      success: () => {
        $(`li#user_${id}`).hide(20);
        alert("Delete completed");
      },
      error: (xhr, status, error) => {
        var err = "(" + xhr.responseText + ")";
        alert(err);
      },
    });
  });

  $(".institutes-list-item-tools__button.delete").on("click", (e) => {
    id = e.target.id;
    $.ajax({
      method: "POST",
      url: `/admin/institute/delete/${id}`,
      dataType: "html",
      success: () => {
          $(`li#inst_${id}`).hide(20);
        alert("Delete completed");
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

  $(".institutes-head-tools__button.add").on("click", () => {
    window.location.replace("/admin/institute/create");
  });

  $(".specialization-head-tools__button.add").on("click", () => {
    window.location.replace("/admin/specialization/create");
  });

  $(".specializations-list-tools__button.delete").on("click", (e) => {
    id = e.target.id;

    $.ajax({
      method: "POST",
      url: `/opop/specialization/delete/${id}`,
      dataType: 'html',
      success: () => {
        $(`li#group_${id}`).hide(20)
        alert("Delete completed")
      }
    })
  });
});
