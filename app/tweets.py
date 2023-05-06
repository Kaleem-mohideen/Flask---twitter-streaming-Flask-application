import time
from app import app, db
from datetime import datetime, timedelta
from app.models import Post
from app.utils import TwitterPosts
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INTERVAL = int(450)
def main():
    while True:
        
        posts = Post.query.all()
        current_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
        logger.info(f'{len(posts)} tweets found at {current_time.time()}')
        pst = TwitterPosts()
        posts = pst.getposts()
        for post in posts:
            exists = db.session.query(db.exists().where(Post.content == post[4])).scalar()
            if not exists:
                twitter_posts = Post(author=post[1], date_posted= datetime.strptime(post[3], "%Y-%m-%d %H:%M:%S.%f"), content=post[4], user_name=post[2], decription=post[5], image_file=post[6])
                db.session.add(twitter_posts)
                db.session.commit()
        
        time.sleep(INTERVAL)

if __name__ == '__main__':
    main()