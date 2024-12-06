import gradio as gr
from gradio_sourceviewer import SourceViewer
from pyannote.audio import Pipeline
import os


def apply_pipeline(audio: str) -> tuple:
    pipeline = Pipeline.from_pretrained(
        "pyannote/speech-separation-ami-1.0", use_auth_token=os.environ["HF_TOKEN"]
    )
    return pipeline(audio)


with gr.Blocks() as demo:
    audio = gr.Audio(type="filepath")
    btn = gr.Button("Apply separation pipeline")
    source_viewer = SourceViewer(interactive=False)

    btn.click(fn=apply_pipeline, inputs=[audio], outputs=[source_viewer])


if __name__ == "__main__":
    demo.launch()
