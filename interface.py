import gradio as gr
from api_utils import fetch_model_tags, generate_output

def create_gradio_interface(ollama_server_url, generate_url):
    # Fetch model tags and prompts
    model_tags, model_prompts = fetch_model_tags(ollama_server_url)

    # Function to update the textbox with the corresponding prompt when a model is selected
    def update_prompt(selected_model):
        return model_prompts.get(selected_model, "")

    # Custom CSS for a fancy and cute look
    custom_css = """
    .container {
        margin: auto;
        background-color: #fef6e4;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    }
    h1, h2 {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #ff7b72;
        text-align: center;
    }
    .gr-button {
        background-color: #ffcccb;
        color: #fff;
        font-weight: bold;
        border-radius: 10px;
    }
    .gr-button:hover {
        background-color: #ffb6b9;
    }
    .gr-textbox, .gr-slider {
        border-color: #ffd3b6;
        width: 100%; 

    }
    .title {
        font-size: 3em; 
        margin-top: 20px;
        margin-bottom: 20px;
    }
    """

    # Create Gradio interface using Blocks
    with gr.Blocks(css=custom_css) as demo:
        # Add a title and description with the app name
        gr.Markdown(f"""
        <h1 class="title">Tariqak 🛣️</h1>
        <class="description"><p> <b>Welcome!</b> Select a model, adjust the parameters, and generate something magical!  
        Enjoy the sweet and playful interface we crafted just for you! 🍬✨</p>
        """)

        with gr.Column():
            # Input Section at the top
            with gr.Row():
                dropdown = gr.Dropdown(choices=model_tags, label="Select a Model", value=model_tags[0] if model_tags else None)
              
            with gr.Row():
                prompt_box = gr.Textbox(label="Enter your prompt", lines=10, placeholder="Type something amazing...")
                
            # Button Section
            with gr.Row():
                submit_btn = gr.Button("✨ Generate ✨")
            
            # Parameter Sliders
            with gr.Row():
                temperature_slider = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, value=0.1, label="Temperature")
                top_p_slider = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, value=0.5, label="Top p")
                top_k_slider = gr.Slider(minimum=1, maximum=100, step=1, value=70, label="Top k")
            
            # Output Section at the bottom
            output_box = gr.Textbox(label="Your Magical Output", lines=10)

        # Set up the interactions
        dropdown.change(fn=update_prompt, inputs=dropdown, outputs=prompt_box)
        submit_btn.click(fn=lambda model, prompt, temp, p, k: generate_output(generate_url, model, prompt, temp, p, k),
                         inputs=[dropdown, prompt_box, temperature_slider, top_p_slider, top_k_slider], outputs=output_box)

    return demo
