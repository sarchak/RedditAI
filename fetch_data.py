import praw
import os
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.redditdb
submissions = db.submissions
comments = db.comments

reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                     client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                     user_agent='RedditAI')

def save_post(submission):
  try:
    sub = {
      'text': submission.title,
      'author': submission.author.name,
      'submission_id': submission.id,
      'subreddit': submission.subreddit.display_name,
      'score': submission.score
    }

    submissions.update({'submission_id': submission.id}, sub, upsert=True)
  except:
    x = 1

  for i, comment in enumerate(submission.comments.list()):
    try:
      comm = {
        'text' : comment.body,
        'author': comment.author.name,
        'score': comment.score,
        'comment_id': comment.id
      }
      comments.update({'comment_id': comment.id}, comm, upsert=True)
    except:
      x = 1

reddit_list = ['entrepreneur', 'smallbusiness', 'seo', 'marketing', 'bigseo', 'socialmedia',
               'PPC', 'AskMarketing', 'GrowthHacking', 'Emailmarketing', 'analytics', 'EntrepreneurRideAlong', 'digitalnomad']

for sr in reddit_list:
  for submission in reddit.subreddit(sr).hot(limit=2000):
      print("{}".format(submission.title))
      save_post(submission)
      print("------------------------")
