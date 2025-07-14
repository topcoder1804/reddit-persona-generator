from groq import Groq
import json
from datetime import datetime
from config import GROQ_API_KEY

class PersonaBuilder:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        # Use the specific Llama 4 Scout model you requested
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"
        
    def analyze_content(self, user_data):
        """Analyze scraped content to build persona using Llama 4 Scout"""
        
        # Prepare content for analysis
        content_summary = self._prepare_content_summary(user_data)
        
        # Create persona using Llama 4 Scout
        persona_prompt = f"""
        You are an expert user researcher who creates detailed user personas based on social media activity.
        
        Analyze the following Reddit user data and create a comprehensive user persona:
        
        {content_summary}
        
        Create a detailed persona including:
        
        ## DEMOGRAPHICS
        - Age estimate (with reasoning based on language patterns, references, life stage indicators)
        - Location hints (time zones, local references, cultural markers)
        - Occupation/education clues (technical knowledge, work references, schedule patterns)
        - Lifestyle indicators (hobbies, spending patterns, living situation)
        
        ## PERSONALITY TRAITS
        - Introvert vs Extrovert tendencies (based on interaction patterns)
        - Communication style (formal/casual, helpful/critical, analytical/emotional)
        - Emotional patterns (optimistic/pessimistic, reactive/measured)
        - Decision-making style (impulsive/deliberate, data-driven/intuitive)
        
        ## INTERESTS & EXPERTISE
        - Primary interests (ranked by engagement and knowledge depth)
        - Areas of expertise (demonstrated through detailed responses)
        - Learning preferences (how they seek and share information)
        - Content consumption patterns
        
        ## ONLINE BEHAVIOR PATTERNS
        - Posting frequency and timing patterns
        - Engagement style (lurker vs active participant vs content creator)
        - Response to controversy or disagreement
        - Community leadership or follower tendencies
        
        ## MOTIVATIONS & GOALS
        - What drives their online participation
        - Information seeking vs sharing patterns
        - Social connection needs and preferences
        - Achievement or recognition seeking behaviors
        
        ## FRUSTRATIONS & PAIN POINTS
        - Common complaints or concerns expressed
        - Technology or platform struggles
        - Social or professional challenges mentioned
        - Recurring themes in negative posts
        
        ## VALUES & BELIEFS
        - Core principles evident in their posts
        - Ethical stances and moral frameworks
        - Political or social leanings (if apparent)
        - Causes they support or oppose
        
        For each characteristic, provide specific citations from their posts/comments that support your analysis. Use direct quotes when possible and reference the subreddit context.
        
        Format your response with clear headings and detailed bullet points for easy reading.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert user researcher who creates detailed user personas based on social media activity. Provide thorough analysis with specific evidence from the user's content. Use the advanced reasoning capabilities of Llama 4 Scout to provide deep insights."},
                    {"role": "user", "content": persona_prompt}
                ],
                max_tokens=2500,  # Increased for more detailed analysis
                temperature=0.2,  # Lower for more consistent analysis
                stream=False
            )
            
            return {
                'analysis': response.choices[0].message.content,
                'model_used': self.model,
                'structured': True
            }
            
        except Exception as e:
            print(f"Error generating persona with Llama 4 Scout: {str(e)}")
            return None
    
    def _prepare_content_summary(self, user_data):
        """Prepare enhanced content summary for Llama 4 Scout analysis"""
        
        # Get top posts by engagement with more context
        top_posts = sorted(user_data['posts'], key=lambda x: x['score'], reverse=True)[:25]
        posts_text = "\n".join([
            f"POST #{i+1} (Score: {post['score']}, Subreddit: r/{post['subreddit']}, Date: {datetime.fromtimestamp(post['created_utc']).strftime('%Y-%m-%d')}):\n"
            f"Title: {post['title']}\n"
            f"Content: {post['selftext'][:500]}{'...' if len(post['selftext']) > 500 else ''}\n"
            f"---"
            for i, post in enumerate(top_posts) if post['selftext']
        ])
        
        # Get top comments with more context
        top_comments = sorted(user_data['comments'], key=lambda x: x['score'], reverse=True)[:35]
        comments_text = "\n".join([
            f"COMMENT #{i+1} (Score: {comment['score']}, Subreddit: r/{comment['subreddit']}, Date: {datetime.fromtimestamp(comment['created_utc']).strftime('%Y-%m-%d')}):\n"
            f"{comment['body'][:400]}{'...' if len(comment['body']) > 400 else ''}\n"
            f"---"
            for i, comment in enumerate(top_comments)
        ])
        
        # Enhanced subreddit activity analysis
        subreddit_activity = {}
        post_times = []
        comment_times = []
        
        for post in user_data['posts']:
            subreddit_activity[post['subreddit']] = subreddit_activity.get(post['subreddit'], 0) + 1
            post_times.append(post['created_utc'])
            
        for comment in user_data['comments']:
            subreddit_activity[comment['subreddit']] = subreddit_activity.get(comment['subreddit'], 0) + 1
            comment_times.append(comment['created_utc'])
        
        top_subreddits = sorted(subreddit_activity.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # Calculate activity patterns
        total_karma = user_data['user_info']['comment_karma'] + user_data['user_info']['link_karma']
        account_age_days = (datetime.now().timestamp() - user_data['user_info']['created_utc']) / (24 * 3600)
        
        return f"""
        USER PROFILE COMPREHENSIVE SUMMARY:
        
        Username: {user_data['user_info']['username']}
        Account Created: {datetime.fromtimestamp(user_data['user_info']['created_utc']).strftime('%Y-%m-%d')}
        Account Age: {account_age_days:.0f} days
        Comment Karma: {user_data['user_info']['comment_karma']:,}
        Link Karma: {user_data['user_info']['link_karma']:,}
        Total Karma: {total_karma:,}
        Posts Analyzed: {len(user_data['posts'])}
        Comments Analyzed: {len(user_data['comments'])}
        
        TOP SUBREDDITS BY ACTIVITY (Community Engagement Patterns):
        {chr(10).join([f"{i+1}. r/{sub}: {count} posts/comments" for i, (sub, count) in enumerate(top_subreddits)])}
        
        TOP POSTS BY ENGAGEMENT (Content Creation Patterns):
        {posts_text}
        
        TOP COMMENTS BY ENGAGEMENT (Interaction Patterns):
        {comments_text}
        """
    
    def generate_behavioral_insights(self, user_data, initial_persona):
        """Generate advanced behavioral insights using Llama 4 Scout's reasoning capabilities"""
        
        insight_prompt = f"""
        Using advanced behavioral analysis, examine this Reddit user's activity patterns and provide deeper insights:
        
        Initial Persona Analysis:
        {initial_persona['analysis']}
        
        Conduct advanced analysis in these areas:
        
        1. **Communication Patterns & Style**:
           - Sentence structure and complexity
           - Vocabulary sophistication and technical language use
           - Emotional expression patterns
           - Argument construction and persuasion techniques
        
        2. **Social Dynamics & Relationships**:
           - How they build rapport with others
           - Conflict resolution or escalation patterns
           - Leadership vs follower behaviors
           - Community integration strategies
        
        3. **Cognitive Patterns**:
           - Problem-solving approaches
           - Information processing preferences
           - Decision-making frameworks
           - Learning and adaptation patterns
        
        4. **Temporal & Engagement Patterns**:
           - Activity timing and consistency
           - Response speed and thoughtfulness
           - Long-term vs short-term engagement
           - Seasonal or cyclical behavior patterns
        
        5. **Content Strategy & Curation**:
           - What they choose to share vs keep private
           - How they position themselves in discussions
           - Their role in information ecosystems
           - Influence and authority building
        
        6. **Psychological Indicators**:
           - Stress responses and coping mechanisms
           - Motivation drivers and reward systems
           - Risk tolerance and novelty seeking
           - Social validation needs
        
        Provide specific examples from their activity to support each insight. Use Llama 4 Scout's advanced reasoning to identify subtle patterns and connections.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an advanced behavioral analyst using Llama 4 Scout's superior reasoning capabilities. Provide deep psychological and behavioral insights with specific evidence and sophisticated analysis."},
                    {"role": "user", "content": insight_prompt}
                ],
                max_tokens=2000,
                temperature=0.1,  # Very low for consistent deep analysis
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating behavioral insights: {str(e)}")
            return "Advanced behavioral insights not available due to API error."
