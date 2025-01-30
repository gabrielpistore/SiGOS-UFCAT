$(document).ready(function () {
  const table = $("#workorder-table").DataTable({
    serverSide: true,
    ajax: {
      url: "../api/ordens/",
      type: "GET",
      data: function (d) {
        // Add filter parameters to the request
        d.category = $("#filter-category").val();
        d.id = $("#filter-id").val();
        d.status = $("#filter-status").val();
        d.location = $("#filter-location").val();
        d.start_created_at = $("#filter-start-created-at").val();
        d.end_created_at = $("#filter-end-created-at").val();
      },
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
    order: [],
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

  // Apply filters
  $("#apply-filters").on("click", function () {
    table.ajax.reload(); // Reload the table with new filters
  });

  // Clear filters
  $("#clear-filters").on("click", function () {
    $("#filter-category").val("");
    $("#filter-id").val("");
    $("#filter-status").val("");
    $("#filter-location").val("");
    $("#filter-start-created-at").val("");
    $("#filter-end-created-at").val("");
    table.ajax.reload(); // Reload the table without filters
  });
});
