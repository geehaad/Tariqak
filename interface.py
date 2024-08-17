import gradio as gr
from api_utils import fetch_model_tags, generate_output

def create_gradio_interface(ollama_server_url, generate_url):
    # Fetch model tags and prompts
    model_tags, model_prompts = fetch_model_tags(ollama_server_url)

    # Function to update the textbox with the corresponding prompt when a model is selected
    def update_prompt(selected_model):
        return model_prompts.get(selected_model, "")

    # Create Gradio interface using Blocks
    with gr.Blocks() as demo:
        with gr.Row():
            dropdown = gr.Dropdown(choices=model_tags, label="Select a Model", value=model_tags[0] if model_tags else None)
      
        with gr.Row():
            prompt_box = gr.Textbox(label="Enter your prompt", lines=10)
            
        with gr.Row():
            temperature_slider = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, value=0.1, label="Temperature")
            top_p_slider = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, value=0.5, label="Top p")
            top_k_slider = gr.Slider(minimum=1, maximum=100, step=1, value=70, label="Top k")
        
        with gr.Row():
            submit_btn = gr.Button("Submit")
        
        output_box = gr.Textbox(label="Output Box", lines=10)

        # Set up the interactions
        dropdown.change(fn=update_prompt, inputs=dropdown, outputs=prompt_box)
        submit_btn.click(fn=lambda model, prompt, temp, p, k: generate_output(generate_url, model, prompt, temp, p, k),
                         inputs=[dropdown, prompt_box, temperature_slider, top_p_slider, top_k_slider], outputs=output_box)

    return demo
