import gradio as gr

from ai import ai_interaction
from voices import gen_voices, read_text_list

artists = gen_voices()

def ui():
    with gr.Blocks() as demo:
        gr.Markdown("# Simple Text Processing App")

        # First section: Generate output
        with gr.Blocks():
            gr.Markdown("## 1. Generate Output")
            with gr.Column():
                input_text = gr.Textbox(label="Input Text", placeholder="Enter text here...")
                generate_btn = gr.Button("Generate")
            output_text = gr.Textbox(label="Generated Output", interactive=False)

        # Second section: Edit output
        with gr.Blocks():
            gr.Markdown("## 2. Edit Previous Output")
            with gr.Column():
                voice_dropdown = gr.Dropdown(
                    choices=artists,
                    value=artists[0][1] if artists else None,
                    label="Voice"
                )
                edit_btn = gr.Button("Apply Edit And Generate video")
                audio_output = gr.Audio(label="Generated Speech")
                status_message = gr.Textbox(label="Status", interactive=False)

        # Set up the button click events
        generate_btn.click(
            fn=ai_interaction,
            inputs=[input_text],
            outputs=[output_text]
        )

        edit_btn.click(
            fn=read_text_list,
            inputs=[output_text,voice_dropdown],
            outputs=[audio_output,status_message]
        )
        return demo
