from .models import OutputData, TrainingData, ClassifyUnits


def create_output_object(obj, onestring):
    output = OutputData(
        postingId=obj.postingId,
        zeilennr=obj.zeilennr,
        classID=obj.classID,
        content=obj.content,
        prepro=onestring
    )
    return output

