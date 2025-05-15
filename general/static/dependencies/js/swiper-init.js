document.addEventListener("DOMContentLoaded", function () {
  const swiper = new Swiper(".mySwiper", {
    effect: "cube",
    grabCursor: true,
    speed: 1500, // ⬅️ Увеличена длительность анимации (плавнее)
    cubeEffect: {
      shadow: true,
      slideShadows: true,
      shadowOffset: 20,
      shadowScale: 0.94,
    },
    loop: true,
    autoplay: {
      delay: 6000, // ⬅️ Более длительная пауза между слайдами
      disableOnInteraction: false,
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });
});