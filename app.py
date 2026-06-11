import os
from datetime import datetime

import streamlit as st

from ai import generate_post
from database import get_db

conn = get_db()

st.set_page_config(
    page_title="Kurioses Agent",
    layout="wide"
)

st.title("🌍 Kurioses aus aller Welt")

if st.button("Neuen Beitrag erzeugen"):

    with st.spinner("Generiere Beitrag..."):

        post = generate_post()

        conn.execute(
            """
            INSERT INTO posts(
                topic,
                title,
                body,
                hashtags,
                image_prompt,
                status,
                created_at
            )
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                post["topic"],
                post["title"],
                post["body"],
                post["hashtags"],
                post["image_prompt"],
                "PENDING",
                datetime.now().isoformat()
            )
        )

        conn.commit()

    st.success("Beitrag erstellt")

rows = conn.execute(
    """
    SELECT *
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
        status,
        created_at
    ) = row

    with st.expander(f"{title} | {status}"):

        st.subheader(topic)

        st.write(body)

        st.markdown("### Hashtags")
        st.write(hashtags)

        st.markdown("### Bild-Prompt")
        st.code(image_prompt)

        col1, col2 = st.columns(2)

        if col1.button(f"Freigeben {post_id}"):

            conn.execute(
                """
                UPDATE posts
                SET status='APPROVED'
                WHERE id=?
                """,
                (post_id,)
            )

            conn.commit()
            st.rerun()

        if col2.button(f"Ablehnen {post_id}"):

            conn.execute(
                """
                UPDATE posts
                SET status='REJECTED'
                WHERE id=?
                """,
                (post_id,)
            )

            conn.commit()
            st.rerun()
