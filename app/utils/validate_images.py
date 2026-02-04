import re

def validate_images(content: str, user_images: list[dict]):
    if not user_images:
        return
    allowed = {img["image_id"] for img in user_images}
    used = re.findall(r"\[\[IMAGE:(.*?)\]\]", content)

    for img_id in used:
        if img_id not in allowed:
            raise ValueError(f"Invalid image_id used: {img_id}") 