document.addEventListener("DOMContentLoaded", () => {
  console.log("SaNeMart JS loaded.");

  const cards = document.querySelectorAll(".product-card");
  cards.forEach((card, index) => {
    card.style.animation = `fadeInUp 0.5s ease forwards`;
    card.style.animationDelay = `${index * 0.1}s`;
  });

  // Optional welcome alert (remove if not needed)
  if (sessionStorage.getItem("loginSuccess")) {
    alert("Welcome back!");
    sessionStorage.removeItem("loginSuccess");
  }

  // Scroll reveal on elements with class .scroll-reveal
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("active");
      }
    });
  }, {
    threshold: 0.15
  });

  document.querySelectorAll('.scroll-reveal').forEach(el => {
    observer.observe(el);
  });
});
