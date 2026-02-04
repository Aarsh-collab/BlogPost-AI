def render_blog(content: str, user_images: list[dict]) -> str:
    """
    Replaces image tokens like {{image:img_1}} with HTML placeholders.
    Real image rendering is handled by Streamlit later.
    """

    rendered = content

    for img in user_images:
        image_id = img.get("image_id")
        caption = img.get("caption", "")

        # Placeholder HTML (no URL required at this stage)
        html = f"<div class='image-block'>[IMAGE: {image_id}]<br/>{caption}</div>"

        rendered = rendered.replace(f"{{{{image:{image_id}}}}}", html)

    return rendered