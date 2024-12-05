from flask import Blueprint, jsonify
from datetime import datetime
from ..utils.news_utils import fetch_news, fetch_news_by_slug

news_list_bp = Blueprint('news_list', __name__)

@news_list_bp.route('/news', methods=['GET'])
def news_list():
    news = fetch_news()
    news_list = []
    for item in news:
        news_list.append({
            "id": item["id"],
            "title": item["title"],
            "description": item["description"],
            "content": item["content"],
            "image_url": item["image_url"],
            "category": item["category"],
            "created_at": item["created_at"],
            "slug": item["slug"]
        })
    return jsonify(news_list)

@news_list_bp.route('/news/<slug>', methods=['GET'])
def news_by_slug(slug):
    news = fetch_news_by_slug(slug)
    if news:
        news_dict = {
            "id": news["id"],
            "title": news["title"],
            "description": news["description"],
            "content": news["content"],
            "image_url": news["image_url"],
            "category": news["category"],
            "created_at": news["created_at"],
            "slug": news["slug"]
        }
        return jsonify(news_dict)
    return jsonify({})