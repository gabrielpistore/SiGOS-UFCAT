$(document).ready(function () {
  const table = $("#workorder-history-table").DataTable({
    serverSide: true,
    ajax: {
      url: "../../api/historico", // Replace with your API endpoint
      type: "GET",
    },
    language: portuguese, // Ensure the Portuguese translation is loaded
    columns: [
      { data: "title", name: "Ordem de Serviço" }, // WorkOrder Title
      {
        data: "history_date",
        name: "Data da Alteração",
        render: function (data) {
          return formatDate(data); // Format date as DD/MM/YYYY HH:mm:ss
        },
      },
      {
        data: "history_user",
        name: "Usuário",
        render: function (data) {
          return data || "Sistema"; // Fallback to "Sistema" if no user is logged
        },
      },
      { data: "prev_status", name: "Status Anterior" }, // Previous Status
      { data: "status", name: "Status Atual" }, // Current Status
      {
        data: "changes",
        name: "Alterações",
        orderable: false,
        render: function (data) {
          if (data && data.length > 0) {
            return data
              .map((change) => `<strong>${change.field}:</strong> ${change.old} → ${change.new}`)
              .join("<br>");
          }
          return "Criado inicialmente.";
        },
      },
    ],
    order: [[1, "desc"]], // Default sorting by "Data da Alteração" (descending)
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
      bottomEnd: "paginate",
    },
    createdRow: function (row, data, dataIndex) {
      $(row).addClass("border-b");
    },
  });

  // Helper function to format date
  function formatDate(dateString) {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const seconds = String(date.getSeconds()).padStart(2, "0");
    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
  }
});
