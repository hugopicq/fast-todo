import random
import time
import datetime

from fast_todo.app.token.token_maker import get_token_maker, TokenMaker

def test_token_ok():
    user_id = random.randint(1, 5000)
    token_maker = next(get_token_maker())

    token = token_maker.create_token(user_id)
    assert len(token) > 0

    decoded_token = token_maker.decode_token(token)
    assert decoded_token is not None
    assert decoded_token.expired_at > time.time()
    assert decoded_token.user_id == user_id

def test_expired_token():
    user_id = random.randint(1, 5000)
    token_maker = next(get_token_maker())

    token = token_maker.create_token(user_id, -datetime.timedelta(minutes=1))
    assert len(token) > 0

    decoded_token = token_maker.decode_token(token)
    assert decoded_token is None