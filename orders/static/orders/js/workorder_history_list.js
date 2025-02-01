$(document).ready(function () {
  const table = $("#history-table").DataTable({
    serverSide: true,
    ajax: {
      url: "../../api/historico",
      type: "GET",
      error: function (xhr, error, thrown) {
        console.error("Error loading DataTable:", error, thrown);
        alert("Erro ao carregar os dados. Por favor, tente novamente."); // User-friendly error message
      },
    },
    language: portuguese, // Ensure the Portuguese translation is loaded
    columns: [
      {
        data: "title",
        name: "Ordem de Serviço",
      }, // WorkOrder Title
      {
        data: "history_date",
        name: "Data da Alteração",
        render: function (data) {
          return data ? new Date(data).toLocaleString() : "N/A"; // Format date or show "N/A"
        },
      },
      {
        data: "history_user",
        name: "Usuário",
        render: function (data) {
          return data || "Sistema"; // Fallback to "Sistema" if no user is logged
        },
      },
      {
        data: "prev_status",
        name: "Status Anterior",
      }, // Previous Status
      {
        data: "status",
        name: "Status Atual",
      }, // Current Status
      {
        data: "changes",
        name: "Alterações",
        orderable: false,
        render: function (data) {
          if (data && Array.isArray(data) && data.length > 0) {
            return data
              .map(
                (change) =>
                  `<strong>${change.field}:</strong> ${change.old || "N/A"} → ${
                    change.new || "N/A"
                  }`
              )
              .join("<br>");
          }
          return "Criado inicialmente."; // Default message if no changes
        },
      },
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
});
