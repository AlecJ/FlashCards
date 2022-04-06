from sqlalchemy import exc, or_, and_
from sqlalchemy.sql.expression import func
from datetime import datetime, timedelta, timezone
import pytz
from src.util import loggingFactory
from src.models.models import Flashcard


_getLogger = loggingFactory('api.service')


"""
Handles CRUD operations.

The operations that will be performed are:

get_card -
get_all_cards -
create_card -
update_card -
delete_card -

Flashcard Logic:
There are 12 bins of cards, each representing increasing levels of mastery.
Each user-word starts out in bin 0.
If a user gets a word right, it moves to the next bin, up to bin 11.
If a user gets a word wrong, it goes back to bin 1.
Bins 1-11 are associated with the following timespans:
5 seconds, 1
25 seconds, 2
2 minutes, 3
10 minutes, 4
1 hour, 5
5 hours, 6
1 day, 7
5 days, 8
25 days, 9
4 months, 10
and never. 11
The timespans reflect the amount of time to wait before the next review of that card.

Reviewing Words:
If any words at bin 1 or higher have reached 0 time or less, review these first.
For the subset above, review higher-numbered bins before lower bins.
Between two words of the same bin and same time for review, order does not matter.
If all words in bin 1 or higher have positive timers on them, start drawing new words from bin 0 (order does not matter).
If there are no words in bin 0 and all other words still have positive timers, display a message: “You are temporarily done; please come back later to review more words.”

Forgetting Words:
If a user has gotten any single word wrong 10 times ever (even if they got the word right in between; this is a lifetime count), the word gets put into a “hard to remember” bin and is never shown again.
If all words are either in the last bin (never review) or in “hard to remember”, display a message “you have no more words to review; you are permanently done!”


"""


def get_card(session):
    """
    Determine if the user has any words to study, if so, show them one of the
    valid words

    To query here is a bit complex to handle our Bin logic. Start at the highest bin with the longest time
    and search downward until a bin has at least one word to review in it. Then return that word.

    The following query is used:

        SELECT * from flashcard
        WHERE num_times_incorrect < 10
        AND (bin = 10 AND CUR_TIME - 4 months (16 weeks) > last_time_read
        OR (bin = 9 AND CUR_TIME - 25 days > last_time_read
        OR (bin = 8 AND CUR_TIME - 5 days > last_time_read
        OR (bin = 7 AND CUR_TIME - 1 day > last_time_read
        OR (bin = 6 AND CUR_TIME - 5 hours > last_time_read
        OR (bin = 5 AND CUR_TIME - 1 hour > last_time_read
        OR (bin = 4 AND CUR_TIME - 10 min > last_time_read
        OR (bin = 3 AND CUR_TIME - 2 min > last_time_read
        OR (bin = 2 AND CUR_TIME - 25 sec > last_time_read
        OR (bin = 1 AND CUR_TIME - 5 sec > last_time_read
        OR bin = 0
        ORDER BY bin

    :param session: The current session
    :return: A Flashcard object
    """
    logger = _getLogger('get_card')
    try:
        current_time = datetime.utcnow()

        # Perform the query to select the highest bin, ready-to-show, flashcard
        card = session.query(Flashcard) \
            .filter(and_(Flashcard.bin < 11,
                         Flashcard.num_times_incorrect < 10,
                         or_(and_(Flashcard.bin == 10, current_time - timedelta(weeks=16) > Flashcard.last_read_time),
                             and_(Flashcard.bin == 9, current_time -
                                  timedelta(days=25) > Flashcard.last_read_time),
                             and_(Flashcard.bin == 8, current_time -
                                  timedelta(
                                      days=5) > Flashcard.last_read_time),
                             and_(Flashcard.bin == 7, current_time -
                                  timedelta(
                                      days=1) > Flashcard.last_read_time),
                             and_(Flashcard.bin == 6, current_time -
                                  timedelta(
                                      hours=5) > Flashcard.last_read_time),
                             and_(Flashcard.bin == 5, current_time -
                                  timedelta(
                                      hours=1) > Flashcard.last_read_time),
                             and_(Flashcard.bin == 4, current_time -
                                  timedelta(
                                      minutes=10) > Flashcard.last_read_time),
                             and_(Flashcard.bin == 3, current_time -
                                  timedelta(
                                      minutes=2) > Flashcard.last_read_time),
                             and_(Flashcard.bin == 2, current_time -
                                  timedelta(
                                      seconds=25) > Flashcard.last_read_time),
                             and_(Flashcard.bin == 1, current_time -
                                  timedelta(seconds=5) > Flashcard.last_read_time),
                             Flashcard.bin == 0))) \
            .order_by(Flashcard.bin.desc()) \
            .first()
        logger.debug('Card retrieved for user: \n{}'.format(card))
        return card

    except (exc.SQLAlchemyError, AttributeError) as e:
        logger.error(e)
        return None


def get_all_cards(session):
    """
    """
    logger = _getLogger('get_all_cards')
    try:
        cards = session.query(Flashcard).all()
        return cards

    except exc.SQLAlchemyError as e:
        logger.error(e)
        return False


def create_card(session, word, definition):
    """
    Insert a new flashcard into the database.

    :param session: The current session
    :param word: The new word being added
    :param definition: The definition of the new word
    :return: The newly created card
    """
    logger = _getLogger('create_word')
    try:
        new_card = Flashcard(word=word,
                             definition=definition,
                             bin=0,
                             num_times_incorrect=0,
                             created_time=datetime.utcnow(),
                             last_read_time=datetime.utcnow())
        session.add(new_card)
        session.commit()
        logger.debug(
            'New object successfully inserted into DB: \n{}'.format(new_card))
        return new_card
    except exc.SQLAlchemyError as e:
        logger.error(e)
        return None


def update_card(session, id, result):
    """
    If the user was correct, move the card to a higher bin.
    If the user was incorrect, update the incorrect count.
    Update last_read_time.

    :param session:
    :param id:
    :return: None
    """
    logger = _getLogger('update_card')
    try:
        card = session.query(Flashcard).filter(
            Flashcard.id == id).one_or_none()

        # Make sure the card is active
        if not _validate_bin_time(card):
            return False

        # If the user got the answer right, increment the bin
        if result:
            card.bin += 1
        # Otherwise increment incorrect count
        else:
            card.num_times_incorrect += 1

        # Finally, update the last guess time
        card.last_read_time = datetime.utcnow()
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        logger.error(e)
        return False


def delete_card(session, id):
    """
    Remove the card from the database by ID.

    :param session:
    :param id:
    :return: None
    """
    logger = _getLogger('delete_card')
    try:
        session.query(Flashcard).filter(Flashcard.id == id).delete()
        return True
    except exc.SQLAlchemyError as e:
        logger.error(e)
        return False


def _validate_bin_time(card):
    """
    Helper function to make sure users cannot
    say they got a card right that they didnt see.

    Given a card, make sure their bin and last read time
    are valid.

    :param card: A card DB object
    :return: Bool, if the card is active
    """
    logger = _getLogger('_validate_bin_time')

    # A card is not active if its in bin 11 or has failed 10 times
    if card is None or card.bin >= 11 or card.num_times_incorrect >= 10:
        return False

    # Bin 0 is always active
    if card.bin == 0:
        return True

    # Handle the rest of the bins with their different time cooldowns
    cur_time = datetime.now(timezone.utc)

    if card.bin == 10:
        return cur_time - timedelta(weeks=16) > card.last_read_time
    elif card.bin == 9:
        return cur_time - timedelta(days=25) > card.last_read_time
    elif card.bin == 8:
        return cur_time - timedelta(days=5) > card.last_read_time
    elif card.bin == 7:
        return cur_time - timedelta(days=1) > card.last_read_time
    elif card.bin == 6:
        return cur_time - timedelta(hours=5) > card.last_read_time
    elif card.bin == 5:
        return cur_time - timedelta(hours=1) > card.last_read_time
    elif card.bin == 4:
        return cur_time - timedelta(minutes=10) > card.last_read_time
    elif card.bin == 3:
        return cur_time - timedelta(minutes=2) > card.last_read_time
    elif card.bin == 2:
        return cur_time - timedelta(seconds=25) > card.last_read_time
    elif card.bin == 1:
        return cur_time - timedelta(seconds=5) > card.last_read_time

    else:
        logger.error("Card has invalid bin data:\n{}".format(card))
        raise BaseException("Invalid DB row.")
