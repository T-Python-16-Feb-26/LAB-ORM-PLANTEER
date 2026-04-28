function handlePlantSearch(event) {
    const searchInput = document.getElementById("search");
    const form = event.target.form;

    if (!searchInput) return true;

    const searchValue = searchInput.value.trim();

    if (searchValue !== "") {
        form.action = "{% url 'search_plants' %}";
    } else {
        form.action = "{% url 'plants_page' %}";
    }

    return true;
}