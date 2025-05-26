// Script for collapsible filters
function toggleFilter(index) {
    const content = document.getElementById(`filter-content-${index}`);
    const icon = document.getElementById(`filter-icon-${index}`);
    const isOpen = content.style.maxHeight && content.style.maxHeight !== "0px";
    if (isOpen) {
        content.style.maxHeight = "0px";
        if (icon) icon.style.transform = "rotate(0deg)";
    } else {
        content.style.maxHeight = content.scrollHeight + "px";
        if (icon) icon.style.transform = "rotate(180deg)";
    }
}
document.addEventListener("DOMContentLoaded", function () {
    const catalogContainer = document.querySelector("catalog-container");
    const filtersForm = document.getElementById("filters-form");

    // Обновление контента каталога
    async function updateCatalog(url) {
        try {
            const response = await fetch(url, {
                headers: { "X-Requested-With": "XMLHttpRequest" }
            });
            const text = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, "text/html");

            const newCatalog = doc.querySelector("catalog-container");
            if (newCatalog) {
                catalogContainer.innerHTML = newCatalog.innerHTML;
                attachPaginationLinks();
                attachSortLinks();
            }
        } catch (error) {
            console.error("Ошибка при обновлении каталога:", error);
        }
    }

    // Подключение событий к пагинации
    function attachPaginationLinks() {
        catalogContainer.querySelectorAll("a[href*='?page=']").forEach(link => {
            link.addEventListener("click", function (e) {
                e.preventDefault();
                updateCatalog(this.href);
                window.history.pushState({}, "", this.href);
            });
        });
    }

    // Подключение событий к сортировке
    function attachSortLinks() {
        document.querySelectorAll("#filter-content-sort a").forEach(link => {
            link.addEventListener("click", function (e) {
                e.preventDefault();
                updateCatalog(this.href);
                window.history.pushState({}, "", this.href);
            });
        });
    }

    // Обработка отправки формы фильтрации
    filtersForm.addEventListener("change", function (e) {
        const formData = new FormData(filtersForm);
        const params = new URLSearchParams();

        for (let pair of formData.entries()) {
            params.append(pair[0], pair[1]);
        }

        const url = `${window.location.pathname}?${params.toString()}`;
        updateCatalog(url);
        window.history.pushState({}, "", url);
    });

    // Повторное подключение событий после загрузки страницы
    attachPaginationLinks();
    attachSortLinks();

    // Поддержка навигации назад/вперёд в истории браузера
    window.addEventListener("popstate", () => {
        updateCatalog(location.href);
    });
    document.addEventListener("click", function (event) {
        const sortButton = document.getElementById("filter-btn-sort");
        const sortContent = document.getElementById("filter-content-sort");

        const isClickInside = sortButton.contains(event.target) || sortContent.contains(event.target);
        const isOpen = sortContent.style.maxHeight && sortContent.style.maxHeight !== "0px";

        if (!isClickInside && isOpen) {
            sortContent.style.maxHeight = "0px";
            const icon = document.getElementById("filter-icon-sort");
            if (icon) icon.style.transform = "rotate(0deg)";
        }
    });
});