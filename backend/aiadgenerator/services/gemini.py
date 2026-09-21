from google import genai
from google.genai import types
import time
from aiadgenerator.models import AdGeneration
from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
class Scene(BaseModel):
    scene_number:int
    duration:int
    visual_prompt:str
    voiceover:str
class GemModel(BaseModel):
    title:str
    concept:str
    total_duration:int
    target_audience:str
    platform:str
    scenes:list[Scene]
    tone:str
def generate_ad(ad_instance):
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=f'''Create a model short advertisement for the following product.
                Product:
                {ad_instance.product_name}
                Description:
                {ad_instance.description}
                Target audience:
                {ad_instance.audience}
                Platform:
                {ad_instance.platform}
                Tone:
                {ad_instance.tone}
                Duration:
                {ad_instance.duration} seconds.
                Create a compelling advertising concept and divide the advertisement
                into scenes.
                For every scene provide:
                - duration
                - visual description
                - voiceover
                The visual description should be suitable as a prompt for a video
                generation model.
                Make the total scene duration equal to the requested advertisement
                duration.''',
        response_format={
            "type":"text",
            "mime_type":"application/json",
            "schema":GemModel.model_json_schema()
        }
    )
    json_string=interaction.output_text
    return json_string
def generate_video(validate,scene):
    # data2=generate_ad(ad_instance)
    # validate=GemModel.model_validate_json(data2)
    operation = client.models.generate_videos(
    model="veo-3.1-fast-generate-preview",
    prompt=f'''"{validate.title}->the title
                {validate.concept}->the overall concept
                {validate.target_audience}->the audience
                {validate.platform}-> the platform
                {scene.scene_number}->the scene number
                {scene.duration}->the scene duration
                {scene.visual_prompt}->the concept of that particular scene
                {validate.tone}"->the tone
                Create a realistic advertisement video based on these parameters
        
                    ''',
            )
        # Poll the operation status until the video is ready.
    while not operation.done:
        print("Waiting for video generation to complete...")
        time.sleep(10)
        operation = client.operations.get(operation)
                     # Download the generated video.
    return operation.response.generated_videos[0].video

def gemclient():
    return client

     