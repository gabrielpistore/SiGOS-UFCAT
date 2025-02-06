document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    document.querySelectorAll(".toast").forEach(function (toast) {
      toast.style.transition = "opacity 0.5s";
      toast.style.opacity = "0";
      setTimeout(() => toast.remove(), 500);
    });
  }, 3000);
});
