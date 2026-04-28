function openDeleteModal() {
    document.getElementById("deleteModal").classList.add("show");
    document.body.style.overflow = "hidden";
}

function closeDeleteModal() {
    document.getElementById("deleteModal").classList.remove("show");
    document.body.style.overflow = "";
}

window.addEventListener("click", function (e) {
    const modal = document.getElementById("deleteModal");
    if (e.target === modal) {
        closeDeleteModal();
    }
});