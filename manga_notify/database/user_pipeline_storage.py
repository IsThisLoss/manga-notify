import typing
import json
import dataclasses

import sqlite3

class UserPipelineType:
    SUBSCRIPTION = 'subscription'

@dataclasses.dataclass
class UserPipeline:
    user_id: str
    pipeline_type: UserPipelineType
    state: dict

class UserPipelineStorage:
    def __init__(self, conn: sqlite3.Connection):
        self._connection = conn

    def get(self, user_id: str) -> typing.Optional[UserPipeline]:
        row = self._connection.execute("""
            SELECT
                user_id,
                pipeline_type,
                state
            FROM
                user_pipeline
            WHERE
                user_id = ?
            LIMIT 1
        """, (user_id,)).fetchone()
        
        if not row:
            return None

        user_id, pipeline_type, state = row
        return UserPipeline(
            user_id=user_id,
            pipeline_type=pipeline_type,
            state=json.loads(state),
        )

    def put(self, user_pipeline: UserPipeline):
        user_id = user_pipeline.user_id
        pipeline_type = str(user_pipeline.pipeline_type)
        state = str(json.dumps(user_pipeline.state))
        self._connection.execute("""
            INSERT INTO user_pipeline (
              user_id,
              pipeline_type,
              state
            ) VALUES (
                ?,
                ?
            ) ON CONFLICT (user_id) DO UPDATE SET
              pipeline_type = excluded.pipeline_type,
              state = excluded.state
        """, (user_id, pipeline_type, state,))

    def delete(self, user_id: str):
        self._connection.execute("""
            DELETE FROM user_pipeline
            WHERE
               user_id = ?
        """, (user_id,))

