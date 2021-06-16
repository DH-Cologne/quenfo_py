from .models import OutputData, TrainingData


def create_output_object(obj):
    output = OutputData(
        postingId=obj.postingId,
        zeilennr=obj.zeilennr,
        classID=obj.classID,
        content=obj.content
    )
    return output
