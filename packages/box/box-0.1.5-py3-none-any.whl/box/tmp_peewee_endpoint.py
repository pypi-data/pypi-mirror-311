from typing import Optional, List
from peewee import IntegerField, Model, SqliteDatabase, TextField
from box.db_api_base import get_pagination

db = SqliteDatabase('comments.db', pragmas={'journal_mode': 'wal'})

class Comment(Model):
    id = TextField(primary_key=True)
    body = TextField()
    created_utc = IntegerField(index=True)
    link_id = TextField()
    score = IntegerField(index=True)
    subreddit = TextField(index=True)
    subreddit_id = TextField()
    class Meta:
        database = db

def get_clusters(*args, **kwargs):
    return None

def query_comments(
    text: Optional[str] = None,
    before: Optional[int] = None,
    after: Optional[int] = None,
    max_score: Optional[int] = None,
    subreddits: Optional[List[str]] = None,
    by_score: bool = False,
    page: int = 1,
    size: int = 50
) -> dict:
    q = Comment.select()
    conditions = []
    
    if text: conditions.append(Comment.body.contains(text))
    if before: conditions.append(Comment.created_utc <= before)
    if after: conditions.append(Comment.created_utc >= after)
    if max_score: conditions.append(Comment.score <= max_score)
    if subreddits: conditions.append(Comment.subreddit.in_(subreddits))
    
    if conditions:
        q = q.where(*conditions)
    
    total = q.count()
    
    return {
        'pagination': get_pagination(total, page, size),
        'clusters': {'subreddit': get_clusters(q, 'subreddit')},
        'results': list(
            q.order_by(
                Comment.score.desc() if by_score else Comment.created_utc.desc()
            ).paginate(page, size)
            .dicts()
        )
    }
