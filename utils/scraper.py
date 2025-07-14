import praw
import json
from datetime import datetime
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
    
    def extract_username_from_url(self, url):
        """Extract username from Reddit profile URL"""
        if '/user/' in url:
            return url.split('/user/')[1].rstrip('/')
        return url
    
    def scrape_user_data(self, username, limit=100):
        """Scrape user posts and comments"""
        try:
            user = self.reddit.redditor(username)
            
            # Get user info
            user_info = {
                'username': username,
                'created_utc': user.created_utc,
                'comment_karma': user.comment_karma,
                'link_karma': user.link_karma,
                'is_verified': user.verified if hasattr(user, 'verified') else False
            }
            
            # Scrape posts
            posts = []
            for submission in user.submissions.new(limit=limit):
                posts.append({
                    'id': submission.id,
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'subreddit': str(submission.subreddit),
                    'score': submission.score,
                    'created_utc': submission.created_utc,
                    'url': f"https://reddit.com{submission.permalink}",
                    'type': 'post'
                })
            
            # Scrape comments
            comments = []
            for comment in user.comments.new(limit=limit):
                comments.append({
                    'id': comment.id,
                    'body': comment.body,
                    'subreddit': str(comment.subreddit),
                    'score': comment.score,
                    'created_utc': comment.created_utc,
                    'url': f"https://reddit.com{comment.permalink}",
                    'type': 'comment'
                })
            
            return {
                'user_info': user_info,
                'posts': posts,
                'comments': comments
            }
            
        except Exception as e:
            print(f"Error scraping user {username}: {str(e)}")
            return None
