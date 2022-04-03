import typing
import contextlib

from . import user_pipeline
from . import factory

from ..database import database
from ..database import user_pipeline_storage


class UserPipelineWrapper:
    def __init__(self, pipeline: user_pipeline.UserPipeline, state: dict):
        self._pipeline: user_pipeline.UserPipeline = pipeline
        self._state: dict = state

    def get_next_question(self) -> typing.Optional[str]:
        return self._pipeline.get_next_question(self._state)

    def put_answer(self, answer: str):
        return self._pipeline.put_answer(answer, self._state)


def create_new_pipeline(
        db: database.DataBase,
        user_id: str,
        pipeline_type: user_pipeline_storage.UserPipelineType
) -> str:
    pipeline = factory.UserPipelineFactory().get(pipeline_type)
    state = {}
    msg = pipeline.init(state)
    user_pipeline = user_pipeline_storage.UserPipeline(
        user_id=user_id,
        pipeline_type=pipeline_type,
        state=state,
    )
    db.user_pipeline.put(user_pipeline)
    return msg


@contextlib.contextmanager
def get_current_pipeline(db: database.DataBase, user_id: str):
   data = db.user_pipeline.get(user_id)
   if not data:
       return None
   pipeline = factory.UserPipelineFactory().get(data.pipeline_type)
   yield UserPipelineWrapper(pipeline, data.state)
   if pipeline.is_finished():
       db.user_pipeline.delete(user_id)
   else:
       db.user_pipeline.put(data)
