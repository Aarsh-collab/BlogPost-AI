import streamlit as st
from app.utils.image_renderer import render_blog
from app.pipeline.run import run_pipeline

st.set_page_config(page_title="BlogPostAI", layout="wide")

st.title("📝 BlogPostAI")
st.caption("Autonomous research → writing → image-aware blog generation")

# ----------------------------
# USER INPUTS
# ----------------------------

uploaded_images = st.file_uploader(
        "Upload images",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

# ----------------------------
# MAIN INPUT
# ----------------------------
user_prompt = st.text_area(
    "What do you want the blog to be about?",
    placeholder="e.g. My Disney trip, starting from the moment we left...",
    height=150
)

generate = st.button("🚀 Generate Blog")

# ----------------------------
# OUTPUT
# ----------------------------
if generate:
    if not user_prompt:
        st.warning("Please enter a blog prompt.")
    else:
        with st.spinner("Generating blog..."):
            # Normalize uploaded images
            user_images = []
            if uploaded_images:
                for idx, img in enumerate(uploaded_images, start=1):
                    user_images.append({
                        "image_id": f"image_{idx}",
                        "bytes": img.read(),
                        "mime": img.type
                    })

            # Call writer pipeline
            blog = run_pipeline(
                user_prompt=user_prompt,
                user_images=user_images
            )

            rendered_blog = render_blog(blog, user_images)

        st.success("Done!")
        st.markdown(rendered_blog, unsafe_allow_html=True)