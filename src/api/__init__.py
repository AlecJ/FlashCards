from multiprocessing.sharedctypes import Value
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import json
from src.util import session_scope, loggingFactory
from src.api.service import get_card, get_all_cards, create_card, delete_card, update_card

_getLogger = loggingFactory('api')


"""
Routes and methods:

GET /
    When the user first arrives, they will be given a random flashcard from any that
    have past the required amount of time to be shown again.

GET /admin
    Get a list of all cards. This is for the admin screen where a user can view stats,
    and create or delete cards.

POST /
    The user sends a new word and definition, and a new flash card is created.

PUT /
    When a user makes a guess on a flash card, record if they were correct or incorrect.

DELETE /
    The user may delete flashcards by ID.

"""

api_blueprint = Blueprint('battle_api', __name__)
api = Api(api_blueprint)


class FlashCardAPI(Resource):
    def get(self):
        logger = _getLogger('FlashCardAPI.get')

        with session_scope() as session:
            # If admin view, return all cards
            if '/admin' in request.path:
                cards = get_all_cards(session)
                logger.debug(
                    "Sending {} card(s) to admin view.".format(len(cards)))
                return [card.row_as_dict() for card in cards], 200

            # Otherwise, query for a single card
            card = get_card(session)
            if card:
                logger.debug("Selected Card: {}".format(card))
                return card.row_as_dict(), 200
            else:
                logger.debug("No active cards to give user.")
                return None, 200

    def post(self):
        logger = _getLogger('FlashCardAPI.post')

        with session_scope() as session:
            # get word and definition form backend
            data = json.loads(request.data.decode('utf-8'))
            word = data.get('word')
            definition = data.get('definition')

            # If either value is empty, stop and return now
            if word is None or definition is None:
                logger.error(
                    'Word or Definition Value is None. Cannot create new card.')
                return None, 400

            # Otherwise, create and return the card
            card = create_card(session, word, definition)
            return card.row_as_dict(), 200

    def put(self):
        logger = _getLogger('FlashCardAPI.put')

        with session_scope() as session:
            data = json.loads(request.data.decode('utf-8'))
            logger.debug(data)
            id_to_update = data.get('data', {}).get('id')
            answer = data.get('data', {}).get('wasCorrect')

            if update_card(session, id_to_update, answer):
                # get new card for the user
                card = get_card(session)
                if card:
                    logger.debug("Selected Card: {}".format(card))
                    return card.row_as_dict(), 200
                else:
                    logger.debug("No active cards to give user.")
                    return None, 200
            else:
                return None, 400

    def delete(self):
        logger = _getLogger('FlashCardAPI.delete')

        with session_scope() as session:
            # convert byte object to int
            id_to_delete = request.data.decode('utf-8')

            # delete the card from the db
            if delete_card(session, id_to_delete):
                return True, 200
            else:
                return False, 400


api.add_resource(FlashCardAPI, '/api', '/api/admin')
