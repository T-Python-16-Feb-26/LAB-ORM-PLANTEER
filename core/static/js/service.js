document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".reveal-up");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }
        });
    }, { threshold: 0.12 });

    cards.forEach((card, index) => {
        card.style.transitionDelay = `${index * 0.12}s`;
        observer.observe(card);
    });
});
