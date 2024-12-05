from flask import Blueprint, jsonify
from datetime import datetime
from ..utils.news_utils import fetch_news, fetch_news_by_slug

news_list_bp = Blueprint('news_list', __name__)

@news_list_bp.route('/news', methods=['GET'])
def news_list():
    news = fetch_news()
    return jsonify(news)

@news_list_bp.route('/news/<slug>', methods=['GET'])
def news_by_slug(slug):
    news = fetch_news_by_slug(slug)
    return jsonify(news)