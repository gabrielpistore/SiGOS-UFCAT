$(document).ready(function () {
  $("#workOrdersTable").DataTable({
    serverSide: true,
    ajax: {
      url: "../api/ordens/",
      type: "GET",
    },
    language: portuguese,
    columns: [
      { data: "id" },
      { data: "title" },
      { data: "category" },
      { data: "created_at" },
      { data: "status" },
      { data: "actions", orderable: false },
    ],
    order: [[3, "desc"]],
    pagingType: "simple",
    layout: {
      topStart: "",
      topEnd: "",
      bottomStart: [
        "pageLength",
        {
          div: {
            className: "text-gray-400",
            text: "|",
          },
        },
        "info",
      ],
      bottemEnd: "paginate",
    },
    createdRow: function (row, data, dataIndex) {
      $(row).addClass("border-b");
    },
  });
});
