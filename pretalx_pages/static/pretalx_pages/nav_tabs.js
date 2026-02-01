// pretalx-pages nav tabs injection
(function() {
    var dataEl = document.getElementById('pretalx-pages-data');
    if (!dataEl) {
        console.log("pretalx-pages: no data element found");
        return;
    }

    var version = dataEl.dataset.version || "unknown";
    console.log("pretalx-pages fork loaded:", version);

    var pages;
    try {
        pages = JSON.parse(dataEl.dataset.pages || "[]");
    } catch (e) {
        console.log("pretalx-pages: error parsing pages data:", e);
        return;
    }

    console.log("pretalx-pages: pages to add:", pages);

    if (pages.length === 0) {
        console.log("pretalx-pages: no pages with link_in_nav=true");
        return;
    }

    // Pretalx uses #header-tabs with <a class="header-tab"> elements
    var nav = document.getElementById('header-tabs');
    console.log("pretalx-pages: #header-tabs found:", nav);

    if (!nav) {
        console.log("pretalx-pages: no #header-tabs element found");
        return;
    }

    var currentPath = window.location.pathname;

    pages.forEach(function(page) {
        var a = document.createElement("a");
        a.href = page.url;
        a.className = "header-tab";

        // Add icon - use custom icon from data, default to fa-file-text-o
        var icon = document.createElement("i");
        var iconClass = page.icon || "fa-file-text-o";
        // Ensure it has "fa " prefix
        if (!iconClass.startsWith("fa ")) {
            iconClass = "fa " + iconClass;
        }
        icon.className = iconClass;
        a.appendChild(icon);
        a.appendChild(document.createTextNode(" " + page.title + " "));

        // Check if this is the current page
        if (currentPath.indexOf("/page/" + page.url.split("/page/")[1]) !== -1) {
            a.classList.add("active");
        }

        nav.appendChild(a);
        console.log("pretalx-pages: added tab for", page.title, "with icon", iconClass);
    });
})();
