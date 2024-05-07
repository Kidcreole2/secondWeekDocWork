$(document).ready(() => {
  $(".practices-head-tools__button.toggle").on("click", () => {
    $(".users-list").toggle(200);
    $(this).toggleClass("hided");
  });

  $(".group-head-tools__button.toggle").on("click", () => {
    $(".institutes-list").toggle(200);
    $(this).toggleClass("hided");
  });

  $(".practices-list-tools__button.delete").on("click", (e) => {
    id = e.target.id;
    $.ajax({
      method: "POST",
      url: `/opop/practice/delete/${id}`,
      dataType: "html",
      success: () => {
        $(`li#practice_${id}`).hide(20);
        alert("Zaebis");
      },
      error: (xhr, status, error) => {
        var err = "(" + xhr.responseText + ")";
        alert(err);
      },
    });
  });

  $(".group-list-tools__button.delete").on("click", (e) => {
    id = e.target.id

    $.ajax({
        method: "POST",
        url: `/opop/group/delete/${id}`,
        dataType: 'html',
        success: () => {
            $(`li#group_${id}`).hide(20)
            alert("Zaebis")
        }
    })
  });
});
