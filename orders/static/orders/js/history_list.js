$(document).ready(function () {
  const table = $("#history-table").DataTable({
    serverSide: true,
    ajax: {
      url: "../../api/historico",
      type: "GET",
      error: function (xhr, error, thrown) {
        console.error("Error loading DataTable:", error, thrown);
        alert("Erro ao carregar os dados. Por favor, tente novamente.");
      },
    },
    language: portuguese,
    columns: [
      { data: "id", name: "ID" },
      { data: "title", name: "Ordem de Serviço" },
      {
        data: "history_user",
        name: "Usuário",
        render: function (data) {
          return data || "Sistema";
        },
      },
      { data: "status", name: "Status" },
      {
        data: "changes",
        name: "Categoria/Tipo",
        orderable: false,
      },
      {
        data: "history_date",
        name: "Data da Alteração",
        render: function (data) {
          return data ? new Date(data).toLocaleString() : "N/A";
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
