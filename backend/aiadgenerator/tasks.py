from celery import shared_task,chord
from .models import AdGeneration
from .services.gemini import generate_ad,generate_video,GemModel,Scene,gemclient
from rest_framework import serializers
import subprocess,tempfile,os
from pathlib import Path
@shared_task
def generate_task(ad_id):
    instance=AdGeneration.objects.get(id=ad_id)
    try:
        result=generate_ad(instance)
        validate_obj=GemModel.model_validate_json(result)
        scene_tasks=[
            generate_task2.s(validate_obj.model_dump(),scene.model_dump())for scene in validate_obj.scenes
        ]
        chord(scene_tasks)(combine_scenes.s(ad_id).on_error(generate_failed.s(ad_id)))
        return result
    except:
        instance.delete()
        print("Error while generating_ad")
        raise serializers.ValidationError("An error has occured")
@shared_task
def generate_task2(validate,scene_data):
    valid=GemModel.model_validate(validate)
    scene=Scene.model_validate(scene_data)
    video_ref=generate_video(valid,scene)
    temp_file=tempfile.NamedTemporaryFile(suffix=".mp4",delete=False)
    temp_file.close()
    gemclient().files.download(file=video_ref,destination=temp_file.name)
    return {"scene_number":scene_data["scene_number"],
            "path":temp_file.name}
@shared_task
def combine_scenes(scene_results,ad_id):
    concat_file=tempfile.NamedTemporaryFile(mode="w",suffix=".txt",delete=False)
    concat_file.close()
    try:
        with open(concat_file.name,"w") as file:
            for scene in scene_results:
                path=Path(scene["path"]).resolve()
                file.write(f"file '{path.as_posix()}'\n")
        subprocess.run(["ffmpeg","-f","concat","-safe","0","-i",concat_file.name,"-c","copy","final_file.mp4"],check=True)
        AdGeneration.objects.filter(id=ad_id).update(status="completed")
        return {"ad_id":ad_id}
    finally:
        os.unlink(concat_file.name)
        for scene in scene_results:
            os.unlink(scene["path"])
@shared_task
def generate_failed(request,exc,traceback,ad_id):
    return AdGeneration.objects.filter(id=ad_id).update(status="failed")

    

    



    
        


