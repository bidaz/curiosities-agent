from datetime import datetime
import os
import streamlit as st

from ai import generate_post, generate_image_file
from database import get_db

conn = get_db()

st.set_page_config(
    page_title="Kurioses Agent",
    layout="wide"
)

st.title("🌍 Kurioses aus aller Welt")

if st.button("Neuen Beitrag erzeugen"):
    with st.spinner("Generiere Beitrag und Bild..."):
        post = generate_post()

        os.makedirs("images", exist_ok=True)
        image_path = f"images/post_{datetime.now().timestamp()}.png"

        image_url = generate_image_file(
            post["image_prompt"],
            image_path
        )

        conn.execute(
            """
            INSERT INTO posts(
                topic,
                title,
                body,
                hashtags,
                image_prompt,
                image_url,
                status,
                created_at
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                post["topic"],
                post["title"],
                post["body"],
                post["hashtags"],
                post["image_prompt"],
                image_url,
                "PENDING",
                datetime.now().isoformat()
            )
        )

        conn.commit()

    st.success("Beitrag mit Bild erstellt")

rows = conn.execute(
    """
    SELECT id, topic, title, body, hashtags, image_prompt, image_url, status, created_at
    FROM posts
    ORDER BY id DESC
    """
).fetchall()

for row in rows:
    (
        post_id,
        topic,
        title,
        body,
        hashtags,
        image_prompt,
        image_url,
        status,
        created_at
    ) = row

    with st.expander(f"{title} | {status}"):

        if image_url:
            st.image(image_url, use_container_width=True)

        st.subheader(topic)
        st.write(body)

        st.markdown("### Hashtags")
        st.write(hashtags)

        st.markdown("### Bild-Prompt")
        st.code(image_prompt)

        col1, col2 = st.columns(2)

        if col1.button(f"Freigeben {post_id}"):
            conn.execute(
                "UPDATE posts SET status='APPROVED' WHERE id=?",
                (post_id,)
            )
            conn.commit()
            st.rerun()

        if col2.button(f"Ablehnen {post_id}"):
            conn.execute(
                "UPDATE posts SET status='REJECTED' WHERE id=?",
                (post_id,)
            )
            conn.commit()
            st.rerun()
