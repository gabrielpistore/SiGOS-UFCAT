document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    document.querySelectorAll(".message").forEach(function (message) {
      message.style.transition = "opacity 0.5s";
      message.style.opacity = "0";
      setTimeout(() => message.remove(), 500);
    });
  }, 3000);
});
