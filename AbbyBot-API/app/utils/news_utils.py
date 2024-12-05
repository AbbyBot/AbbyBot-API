from ..utils.db import get_db_connection

def fetch_news():
    conn = get_db_connection("AbbyBot_Asuka")
    cursor = conn.cursor()

    try:
        query = """
        SELECT news.id, news.title, news.description, news.content, news.image_url, categories.name AS category, news.created_at, news.slug
        FROM news
        LEFT JOIN categories ON news.category_id = categories.id
        ORDER BY news.created_at DESC
        """
        cursor.execute(query)
        news = cursor.fetchall()
        return news
    finally:
        cursor.close()
        conn.close()

def fetch_news_by_slug(slug):
    conn = get_db_connection("AbbyBot_Asuka")
    cursor = conn.cursor()

    try:
        query = """
        SELECT news.id, news.title, news.description, news.content, news.image_url, categories.name AS category, news.created_at, news.slug
        FROM news
        LEFT JOIN categories ON news.category_id = categories.id
        WHERE news.slug = %s
        """
        cursor.execute(query, (slug,))
        news = cursor.fetchone()
        return news if news else {}
    finally:
        cursor.close()
        conn.close()

