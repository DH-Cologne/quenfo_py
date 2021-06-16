from .models import OutputData, TrainingData

def create_output_object():
    output = OutputData(
        postingId='kdsflö',
        zeilennr=2,
        classID=34,
        content='dkjfsdöl'
    )
    return output

""" for class_instance in data:
    output = OutputData(

        postingId=class_instance.postingId,
        zeilennr=class_instance.zeilennr,
        classID=class_instance.classID,
        content=class_instance.content
    )

    #Base.metadata.tables["outputdata"].create(bind = engine)
    #print('######################') """
