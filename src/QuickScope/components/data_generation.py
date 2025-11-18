from QuickScope.logger.custom_logger import logger
from QuickScope.entity import DataGenerationConfig
from QuickScope.utils.common import create_directories

import pandas as pd
from pathlib import Path
import os
import asyncpraw
from dotenv import load_dotenv #accessing .env vars
import os


class DataGeneration:
    def __init__(self, data_generation_config:DataGenerationConfig):
        self.config = data_generation_config
        load_dotenv()
        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.USER_AGENT = os.getenv("USER_AGENT")

    async def init_connection(self):
        
        self.reddit = asyncpraw.Reddit(
            client_id = self.CLIENT_ID,
            client_secret = self.CLIENT_SECRET,
            user_agent= self.USER_AGENT
        )
        self.reddit.read_only = True
        logger.info("Data Generation: Connection Initialized... ")
        return self.reddit
    
    async def fetch_data(self,topic):
        # Fetching comments from a descussion
        async def get_comments(submission):
            comments = []
            submission.comment_limit = 5  # optional
            await submission.load()       # make sure full data is fetched

            # Handle cases where comments may not exist
            if not hasattr(submission, "comments") or submission.comments is None:
                return ["No comments available"]

            try:
                await submission.comments.replace_more(limit=0)
                async for comment in submission.comments:
                    comments.append(f"▲ {comment.score} | {comment.body[:250]}")
            except Exception as e:
                print(f"Error fetching comments for post {submission.id}: {e}")
                comments.append("Error fetching comments")

            if not comments:
                comments.append("No comments found")

            return comments
        
        
        async def get_news(topic): # returns a list of top 3 relevent news from the specified topic
            n=0
            relevant_news = []
            subreddit = await self.reddit.subreddit(self.config.sub_reddit)
            async for post in subreddit.search(
                query=topic,
                sort=self.config.sort,
                time_filter=self.config.time_filter,
                limit=self.config.limit
            ):
                news_string = ''
                n+=1
                news_string+='News number : '+str(n)+"\n Score : "+str(post.score)+" \n "
                news_string+='title : '+post.title[:300]+"\n content : "+post.selftext[:500]+'\n '
                # if no body text is found, then the comments are fetched
                if post.selftext == '':
                    comments = await get_comments(post)
                    for comm in comments:
                        news_string+='comment : '+comm+'\n '
                news_string+='END \n '
                # appending each news to the news list
                relevant_news.append(news_string)
            return relevant_news
        
        news_data = await get_news(topic)
        return news_data
    
    # Creating Data For Training
    def create_dataset(self,all_topics:list) -> Path:
        logger.info("Data Generation: fetching news... ")
        
        # creating dataframe for storing the data
        df = pd.DataFrame(columns=['topic','input','output'])
        df['topic'] = all_topics
        df['input'] = df['topic'].apply(self.fetch_single_data)
        
        create_directories(self.config.root_dir)
        df.to_csv(self.config.out_dir_path)
        logger.info("Data Generation: news stored... ")

        return self.config.out_dir_path
    
    # After data generation N8N automation is done for getting summary for all the news generated
