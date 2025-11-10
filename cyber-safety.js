// === Theme Toggle (works with body.light-mode and html[data-theme]) ===
const themeToggleBtn = document.getElementById("theme-toggle");

// Apply saved theme on load
window.addEventListener("DOMContentLoaded", () => {
  const saved = localStorage.getItem("theme"); // "light" | "dark" | null
  const isLight = saved === "light";
  document.body.classList.toggle("light-mode", isLight);
  document.documentElement.setAttribute("data-theme", isLight ? "light" : "dark");
});

// Toggle on click (no button text changes)
if (themeToggleBtn) {
  themeToggleBtn.addEventListener("click", () => {
    const isLightNow = !document.body.classList.contains("light-mode");
    document.body.classList.toggle("light-mode", isLightNow);
    document.documentElement.setAttribute("data-theme", isLightNow ? "light" : "dark");
    localStorage.setItem("theme", isLightNow ? "light" : "dark");
  });
}

// === Smooth Scroll for All Internal Links ===
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", e => {
    const href = anchor.getAttribute("href");
    if (!href) return;
    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth" });
    }
  });
});

// === Subtle Animation on Scroll ===
const sections = document.querySelectorAll("section, header, footer, .intro, .heading");
const revealOnScroll = () => {
  const triggerBottom = window.innerHeight * 0.85;
  sections.forEach(section => {
    const rect = section.getBoundingClientRect();
    if (rect.top < triggerBottom) section.classList.add("visible");
    else section.classList.remove("visible");
  });
};
window.addEventListener("scroll", revealOnScroll);
revealOnScroll();
