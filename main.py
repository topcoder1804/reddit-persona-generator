#!/usr/bin/env python3
"""
Reddit User Persona Generator - Groq Edition
Scrapes Reddit user data and generates detailed user personas using Groq's fast LLM API
"""

import sys
import json
import os
from datetime import datetime
from utils.scraper import RedditScraper
from utils.persona_builder import PersonaBuilder

def generate_persona_text(persona_data, user_data, behavioral_insights):
    """Generate formatted persona text file"""
    username = user_data['user_info']['username']
    
    persona_text = f"""
# USER PERSONA: {username.upper()}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated using: {persona_data.get('model_used', 'Groq API')}

## ACCOUNT OVERVIEW
- **Username**: {username}
- **Account Created**: {datetime.fromtimestamp(user_data['user_info']['created_utc']).strftime('%Y-%m-%d')}
- **Comment Karma**: {user_data['user_info']['comment_karma']:,}
- **Link Karma**: {user_data['user_info']['link_karma']:,}
- **Posts Analyzed**: {len(user_data['posts'])}
- **Comments Analyzed**: {len(user_data['comments'])}

## COMPREHENSIVE PERSONA ANALYSIS

{persona_data.get('analysis', 'Analysis not available')}

## BEHAVIORAL INSIGHTS

{behavioral_insights}

## ACTIVITY EVIDENCE

### Most Active Subreddits:
"""
    
    # Calculate and display subreddit activity
    subreddit_activity = {}
    for post in user_data['posts']:
        subreddit_activity[post['subreddit']] = subreddit_activity.get(post['subreddit'], 0) + 1
    for comment in user_data['comments']:
        subreddit_activity[comment['subreddit']] = subreddit_activity.get(comment['subreddit'], 0) + 1
    
    top_subreddits = sorted(subreddit_activity.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for i, (subreddit, count) in enumerate(top_subreddits, 1):
        persona_text += f"\n{i}. **r/{subreddit}** - {count} posts/comments"
    
    persona_text += "\n\n### Top Posts (Supporting Evidence):\n"
    
    # Add top posts as evidence
    top_posts = sorted(user_data['posts'], key=lambda x: x['score'], reverse=True)[:8]
    for i, post in enumerate(top_posts, 1):
        persona_text += f"\n{i}. **{post['title']}** (r/{post['subreddit']})\n"
        persona_text += f"   Score: {post['score']} | Date: {datetime.fromtimestamp(post['created_utc']).strftime('%Y-%m-%d')}\n"
        persona_text += f"   URL: {post['url']}\n"
        if post['selftext']:
            persona_text += f"   Content: {post['selftext'][:250]}...\n"
    
    persona_text += "\n### Top Comments (Supporting Evidence):\n"
    
    # Add top comments as evidence
    top_comments = sorted(user_data['comments'], key=lambda x: x['score'], reverse=True)[:12]
    for i, comment in enumerate(top_comments, 1):
        persona_text += f"\n{i}. **r/{comment['subreddit']}** (Score: {comment['score']})\n"
        persona_text += f"   Date: {datetime.fromtimestamp(comment['created_utc']).strftime('%Y-%m-%d')}\n"
        persona_text += f"   URL: {comment['url']}\n"
        persona_text += f"   Content: {comment['body'][:250]}...\n"
    
    return persona_text

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <reddit_profile_url>")
        print("Example: python main.py https://www.reddit.com/user/kojied/")
        sys.exit(1)
    
    profile_url = sys.argv[1]
    
    # Initialize components
    print("Initializing Reddit scraper and Groq-powered persona builder...")
    scraper = RedditScraper()
    persona_builder = PersonaBuilder()
    
    # Extract username
    username = scraper.extract_username_from_url(profile_url)
    print(f"Processing user: {username}")
    
    # Scrape user data
    print("Scraping Reddit data...")
    user_data = scraper.scrape_user_data(username, limit=150)  # Increased limit for better analysis
    
    if not user_data:
        print("Failed to scrape user data. Please check the username and try again.")
        sys.exit(1)
    
    print(f"Successfully scraped {len(user_data['posts'])} posts and {len(user_data['comments'])} comments")
    
    # Generate persona using Groq
    print("Generating comprehensive persona with Groq API...")
    persona_data = persona_builder.analyze_content(user_data)
    
    if not persona_data:
        print("Failed to generate persona. Please check your Groq API key and try again.")
        sys.exit(1)
    
    # Generate behavioral insights
    print("Generating behavioral insights...")
    behavioral_insights = persona_builder.generate_behavioral_insights(user_data, persona_data)
    
    # Generate final output
    print("Compiling final persona report...")
    persona_text = generate_persona_text(persona_data, user_data, behavioral_insights)
    
    # Save to file
    os.makedirs('output', exist_ok=True)
    output_file = f"output/{username}_persona.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(persona_text)
    
    print(f"✅ Persona successfully saved to: {output_file}")
    
    # Save raw data for reference
    with open(f"output/{username}_raw_data.json", 'w', encoding='utf-8') as f:
        json.dump(user_data, f, indent=2, default=str)
    
    print(f"✅ Raw data saved to: output/{username}_raw_data.json")
    print(f"✅ Process completed using {persona_data.get('model_used', 'Groq API')}")

if __name__ == "__main__":
    main()
