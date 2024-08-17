from config_loader import load_config
from interface import create_gradio_interface

def main():
    # Load the configuration
    config = load_config()

    # Extract URLs from config
    ollama_server_url = config['ollama_server_url']
    generate_url = config['generate_url']

    # Create the Gradio interface
    demo = create_gradio_interface(ollama_server_url, generate_url)

    # Launch the interface
    demo.launch()

if __name__ == "__main__":
    main()
