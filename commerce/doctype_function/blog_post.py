import frappe

def validate(doc, method):
    doc.content = convert_custom_content(doc.custom_content)

def before_save(doc, method):
    if doc.name:
        store_settings_base_url_blog_post = frappe.get_single("Store Settings").get("base_url_blog_post")
        if store_settings_base_url_blog_post:
            doc.url_website = "{store_settings_base_url_blog_post}/#/blog/{blog_name}".format(store_settings_base_url_blog_post = store_settings_base_url_blog_post, blog_name = doc.name)

# --- Hooks end --- 

#DEWE: Function
# - to convert content Rich Text Type into iframe when there's link youtube
def convert_custom_content(content):
    import re
    iframes = re.findall("&lt;&lt;.*&gt;&gt;", content)
    for iframe in iframes:
        youtube_links = re.findall('\\"https://www.youtube.com/watch\?v=[^\\"]*', iframe)
        for youtube_link in youtube_links:
            youtube_link = youtube_link.replace('\"','').replace('watch?v=','embed/')
            content = content.replace(iframe, '<iframe width="560" height="315" src="{youtube_link}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(youtube_link=youtube_link))
    return content