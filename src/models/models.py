from src.models import db
from src.util import json_serializable


class Flashcard(db.Model):
    # __tablename__ = 'flashcards'
    __tablename__ = 'battles'

    id = db.Column(db.Integer(), primary_key=True)

    word = db.Column(db.String(100), nullable=False, unique=True)
    definition = db.Column(db.String(450), nullable=False)
    bin = db.Column(db.Integer(), nullable=False)  # start 0, up to 11
    num_times_incorrect = db.Column(db.Integer(), nullable=False)

    created_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    last_read_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)

    def row_as_dict(self):
        return {
            "id": self.id,
            "word": self.word,
            "definition": self.definition,
            "bin": self.bin,
            "num_times_incorrect": self.num_times_incorrect,
        }

    def __repr__(self):
        return "Battle(id={}, word={}, created_time={})".format(self.id, self.word, self.created_time)
