document.addEventListener("DOMContentLoaded", function () {
    const header = document.getElementById("main-header");

    window.addEventListener("scroll", function () {
      if (window.scrollY > 20) {
        header.classList.add("bg-white", "shadow-lg", "backdrop-blur", "py-2", "text-black");
        header.classList.remove("bg-white/50", "backdrop-blur-md", "py-3");
      } else {
        header.classList.remove("bg-white", "shadow-lg", "backdrop-blur", "py-2");
        header.classList.add("bg-white/50", "backdrop-blur-md", "py-3");
      }
    });
  });