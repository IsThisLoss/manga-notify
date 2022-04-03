from . import subscription_pipeline

from . import user_pipeline
from ..database import user_pipeline_storage


class UserPipelineFactory:
    def get(
            self,
            pipeline_type: user_pipeline_storage.UserPipelineType,
    ) -> user_pipeline.UserPipeline:
        if pipeline_type == user_pipeline_storage.UserPipelineType.SUBSCRIPTION:
            return subscription_pipeline.SubscriptionPipeline()

        raise ValueError(f'Unknow pipeline_type: {pipeline_type}')
