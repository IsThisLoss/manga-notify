import abc


class UserPipeline:
    @abc.abstractmethod
    def init(self, state: dict) -> str:
        pass

    @abc.abstractmethod
    def get_next_question(self, state: dict) -> str:
        pass

    @abc.abstractmethod
    def put_answer(self, answer: str, state: dict) -> str:
        pass

    @abc.abstractmethod
    def is_finished(self):
        pass
