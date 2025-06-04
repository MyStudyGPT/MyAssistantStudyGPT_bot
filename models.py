
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, unique=True, nullable=False)
    username = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    request_count = db.Column(db.Integer, default=0)

    def can_make_request(self, max_requests):
        return self.request_count < max_requests

    def increment_request_count(self):
        self.request_count += 1
        db.session.commit()

class BotMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message_text = db.Column(db.Text)
    response_text = db.Column(db.Text)
    response_time_ms = db.Column(db.Integer)

class BotStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_requests = db.Column(db.Integer, default=0)

    @staticmethod
    def get_current_stats():
        stats = BotStats.query.first()
        if not stats:
            stats = BotStats(total_requests=0)
            db.session.add(stats)
            db.session.commit()
        return stats

    def update_stats(self):
        self.total_requests += 1
        db.session.commit()
