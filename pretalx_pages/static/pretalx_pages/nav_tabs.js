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

    // Try multiple selectors and log what we find
    var selectors = [".schedule-nav", "nav.nav", ".nav-tabs", "ul.nav", ".nav", "nav ul", "header nav"];
    var nav = null;
    for (var i = 0; i < selectors.length; i++) {
        var found = document.querySelector(selectors[i]);
        console.log("pretalx-pages: selector '" + selectors[i] + "' found:", found);
        if (found && !nav) nav = found;
    }

    if (!nav) {
        console.log("pretalx-pages: no nav element found with any selector");
        return;
    }

    console.log("pretalx-pages: using nav element:", nav);
    var currentPath = window.location.pathname;

    pages.forEach(function(page) {
        var li = document.createElement("li");
        li.className = "nav-item";
        var a = document.createElement("a");
        a.href = page.url;
        a.textContent = page.title;
        a.className = "nav-link";
        if (currentPath.indexOf(page.url) !== -1 || page.url.indexOf(currentPath) !== -1) {
            a.classList.add("active");
        }
        li.appendChild(a);
        nav.appendChild(li);
        console.log("pretalx-pages: added tab for", page.title);
    });
})();
