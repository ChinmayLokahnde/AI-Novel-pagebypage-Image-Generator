import os
import base64
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


STABILITY_KEY = os.getenv("STABILITY_API_KEY")

stability_api = client.StabilityInference(
    key=STABILITY_KEY,
    verbose=True,
)


def generate_image(prompt: str):

    if not STABILITY_KEY:
        return None

    answers = stability_api.generate(
        prompt=prompt,
        steps=30,
        width=512,
        height=512,
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                return base64.b64encode(artifact.binary).decode("utf-8")

    return None
