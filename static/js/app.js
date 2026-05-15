document.addEventListener("DOMContentLoaded", () => {
    const citySelect = document.getElementById("city");

    if (!citySelect) {
        return;
    }

    citySelect.addEventListener("change", () => {
        citySelect.form.submit();
    });
});
