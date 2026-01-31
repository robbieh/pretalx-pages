from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _
from pretalx.cfp.signals import footer_link, html_head
from pretalx.common.signals import activitylog_display, activitylog_object_link
from pretalx.common.urls import build_absolute_uri
from pretalx.orga.signals import event_copy_data, nav_event

from .models import Page


@receiver(nav_event)
def show_pages_to_orgnisers(sender, request=None, **kwargs):
    if not request.user.has_perm("event.update_event", request.event):
        return []
    url = f"/orga/event/{request.event.slug}/pages/"
    return [
        {
            "label": _("Pages"),
            "url": reverse(
                "plugins:pretalx_pages:index", kwargs={"event": request.event.slug}
            ),
            "active": request.path.startswith(url),
            "icon": "file-text",
        }
    ]


@receiver(signal=event_copy_data, dispatch_uid="pages_copy_data")
def event_copy_data_receiver(sender, other, **kwargs):
    for p in Page.objects.filter(event__slug__iexact=other):
        p.pk = None
        p.event = sender
        p.save()


@receiver(signal=activitylog_display)
def pretalx_activitylog_display(sender, activitylog, **kwargs):
    event_type = activitylog.action_type
    names = {
        "pretalx_pages.page.added": _("The page has been created."),
        "pretalx_pages.page.changed": _("The page has been modified."),
        "pretalx_pages.page.deleted": _("The page has been deleted."),
    }
    return names.get(event_type)


@receiver(signal=activitylog_object_link)
def pretalx_activitylog_object_link(sender, activitylog, **kwargs):
    if isinstance(activitylog.content_object, Page):
        url = build_absolute_uri(
            "plugins:pretalx_pages:show",
            kwargs={"event": sender.slug, "slug": activitylog.content_object.slug},
        )
        return (
            _("Page")
            + f' <a href="{url}">{escape(activitylog.content_object.title)}</a>'
        )


@receiver(footer_link, dispatch_uid="pages_footer_links")
def footer_link_pages(sender, request=None, **kwargs):
    return [
        {
            "label": page.title,
            "url": build_absolute_uri(
                "plugins:pretalx_pages:show",
                event=sender,
                kwargs={"event": sender.slug, "slug": page.slug},
            ),
        }
        for page in Page.objects.filter(event=sender, link_in_footer=True)
    ]


@receiver(html_head, dispatch_uid="pages_nav_tabs")
def inject_nav_tabs(sender, request=None, **kwargs):
    """Inject JavaScript to add navigation tabs for pages marked as 'link_in_footer'."""
    pages = Page.objects.filter(event=sender, link_in_footer=True).order_by("position", "title")
    if not pages:
        return ""

    # Build the pages data as JavaScript
    pages_js = []
    for page in pages:
        url = build_absolute_uri(
            "plugins:pretalx_pages:show",
            event=sender,
            kwargs={"event": sender.slug, "slug": page.slug},
        )
        # Get the title as a string (handles i18n)
        title = str(page.title)
        pages_js.append(f'{{url: "{url}", title: "{escape(title)}"}}')

    pages_array = "[" + ", ".join(pages_js) + "]"

    return f'''
<script>
document.addEventListener("DOMContentLoaded", function() {{
    var pages = {pages_array};
    var nav = document.querySelector(".schedule-nav, nav.nav, .nav-tabs, ul.nav");
    if (!nav) return;

    var currentPath = window.location.pathname;

    pages.forEach(function(page) {{
        var li = document.createElement("li");
        li.className = "nav-item";
        var a = document.createElement("a");
        a.href = page.url;
        a.textContent = page.title;
        a.className = "nav-link";
        if (currentPath.indexOf(page.url) !== -1 || page.url.indexOf(currentPath) !== -1) {{
            a.classList.add("active");
        }}
        li.appendChild(a);
        nav.appendChild(li);
    }});
}});
</script>
'''
