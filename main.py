import gradio as gr
from fastapi import FastAPI

from ai_skindoctor.app import CSS, iface, main


app = gr.mount_gradio_app(
    FastAPI(),
    iface,
    path="/",
    css=CSS,
    theme=gr.themes.Base(),
)


if __name__ == "__main__":
    main()
