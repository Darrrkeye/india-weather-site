document.addEventListener("DOMContentLoaded", () => {
    const citySelect = document.getElementById("city");
    const searchInput = document.getElementById("search");
    const suggestionsBox = document.getElementById("search-suggestions");
    const locationsData = document.getElementById("locations-data");

    if (citySelect) {
        citySelect.addEventListener("change", () => {
            citySelect.form.submit();
        });
    }

    if (!searchInput || !suggestionsBox || !locationsData) {
        return;
    }

    const locations = Object.entries(JSON.parse(locationsData.textContent)).map(([key, location]) => ({
        key,
        name: location.name,
        state: location.state,
        tagline: location.tagline,
    }));

    let activeIndex = -1;

    function hideSuggestions() {
        suggestionsBox.classList.remove("show");
        suggestionsBox.innerHTML = "";
        searchInput.setAttribute("aria-expanded", "false");
        activeIndex = -1;
    }

    function navigateToSuggestion(location, query) {
        const url = new URL(window.location.origin);
        url.searchParams.set("city", location.key);
        url.searchParams.set("search", query);
        window.location.href = url.toString();
    }

    function renderSuggestions(matches, query) {
        if (!query || matches.length === 0) {
            hideSuggestions();
            return;
        }

        suggestionsBox.innerHTML = "";
        matches.forEach((location, index) => {
            const button = document.createElement("button");
            button.type = "button";
            button.className = "suggestion-item";
            button.setAttribute("role", "option");
            button.innerHTML = `<strong>${location.name}, ${location.state}</strong><span>${location.tagline}</span>`;
            button.addEventListener("click", () => navigateToSuggestion(location, query));
            button.addEventListener("mouseenter", () => {
                activeIndex = index;
                updateActiveSuggestion();
            });
            suggestionsBox.appendChild(button);
        });

        suggestionsBox.classList.add("show");
        searchInput.setAttribute("aria-expanded", "true");
    }

    function updateActiveSuggestion() {
        const items = suggestionsBox.querySelectorAll(".suggestion-item");
        items.forEach((item, index) => {
            item.classList.toggle("active", index === activeIndex);
        });
    }

    function findMatches(query) {
        const normalized = query.trim().toLowerCase();
        if (!normalized) {
            return [];
        }

        return locations
            .filter((location) =>
                location.name.toLowerCase().includes(normalized) ||
                location.state.toLowerCase().includes(normalized) ||
                location.tagline.toLowerCase().includes(normalized) ||
                location.key.toLowerCase().includes(normalized)
            )
            .slice(0, 6);
    }

    searchInput.addEventListener("input", () => {
        const matches = findMatches(searchInput.value);
        renderSuggestions(matches, searchInput.value.trim());
    });

    searchInput.addEventListener("keydown", (event) => {
        const items = suggestionsBox.querySelectorAll(".suggestion-item");
        if (!items.length) {
            return;
        }

        if (event.key === "ArrowDown") {
            event.preventDefault();
            activeIndex = (activeIndex + 1) % items.length;
            updateActiveSuggestion();
        } else if (event.key === "ArrowUp") {
            event.preventDefault();
            activeIndex = activeIndex <= 0 ? items.length - 1 : activeIndex - 1;
            updateActiveSuggestion();
        } else if (event.key === "Enter" && activeIndex >= 0) {
            event.preventDefault();
            items[activeIndex].click();
        } else if (event.key === "Escape") {
            hideSuggestions();
        }
    });

    document.addEventListener("click", (event) => {
        if (!event.target.closest(".search-box")) {
            hideSuggestions();
        }
    });
});
