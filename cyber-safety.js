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

// === Smooth Scroll for All Internal Links (Custom Speed) ===
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", e => {
    const href = anchor.getAttribute("href");
    if (!href) return;
    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      smoothScrollTo(target, 1200); // 1200ms = 1.2 seconds (slower and smoother)
    }
  });
});

// === Smooth Scroll Function ===
function smoothScrollTo(target, duration = 1000) {
  const startY = window.scrollY;
  const targetY = target.getBoundingClientRect().top + startY;
  const diff = targetY - startY;
  let startTime;

  function easeInOutCubic(t) {
    return t < 0.5
      ? 4 * t * t * t
      : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  function animation(currentTime) {
    if (!startTime) startTime = currentTime;
    const timeElapsed = currentTime - startTime;
    const progress = Math.min(timeElapsed / duration, 1);
    const ease = easeInOutCubic(progress);
    window.scrollTo(0, startY + diff * ease);
    if (timeElapsed < duration) requestAnimationFrame(animation);
  }

  requestAnimationFrame(animation);
}
