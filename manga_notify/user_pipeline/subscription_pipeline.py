from . import user_pipeline


class States:
    WAIT_FOR_URL = 'wait_for_url'
    WAIT_FOR_NAME = 'name'


class SubscriptionPipeline(user_pipeline.UserPipeline):
    def init(self, state: dict) -> str:
        state['is_finished'] = False
        state['state'] = States.WAIT_FOR_URL
        return 'Введи ссылку на фид'

    def get_next_question(self, state: dict) -> str:

    def put_answer(self, answer: str, state: dict) -> str:
        if state['state'] == States.WAIT_FOR_URL:
            state['url'] = answer
            state['state'] = States.WAIT_FOR_NAME
            return
        # HERE
        # handle subscription

    def is_finished(self, state: dict) -> bool:
        return state['is_finished']
