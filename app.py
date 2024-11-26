import streamlit as st
from transformers import AutoProcessor, AutoModelForDocumentQuestionAnswering
from PIL import Image
import torch


@st.cache_resource
def load_model():
    processor = AutoProcessor.from_pretrained("MariaK/layoutlmv2-base-uncased_finetuned_docvqa_v2")
    model_instance = AutoModelForDocumentQuestionAnswering.from_pretrained("MariaK/layoutlmv2-base-uncased_finetuned_docvqa_v2")
    return processor, model_instance

def about():
    st.sidebar.markdown("## About Project")
    with st.sidebar.expander("ℹ️ Project Information", expanded=True):
        st.markdown("""
        ### Document Question Answering System
        
        This is a Document Question Answering app powered by LayoutLMv2. 
        You can upload a document image and ask questions related to its content.
        
        #### How it works:
        - Upload a document image (JPG or PNG).
        - The image will be displayed.
        - Enter a question related to the document.
        - The model will provide an answer based on the document content.
        
        #### Important Note:
        This tool is a Demo, not the final Product.
        """)

def handle_question_answering(processor, model_instance):
    
    uploaded_image = st.file_uploader("Upload an image (JPG or PNG):", type=["jpg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image).convert("RGB")
        st.image(image, caption="Uploaded Document (Small Size)", width=300)  
        
        
        question_container = st.container()
        with question_container:
            question = st.text_input("Enter your question:")

            if question and st.button("Get Answer"):
                try:
                    
                    with torch.no_grad():
                        encoding = processor(image, question, return_tensors="pt")
                        outputs = model_instance(**encoding)
                        start_logits = outputs.start_logits
                        end_logits = outputs.end_logits
                        predicted_start_idx = start_logits.argmax(-1).item()
                        predicted_end_idx = end_logits.argmax(-1).item()
                        answer = processor.tokenizer.decode(
                            encoding.input_ids.squeeze()[predicted_start_idx : predicted_end_idx + 1]
                        )

                    st.subheader("Answer:")
                    st.write(answer)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        
        
def main():
    st.set_page_config(
        page_title="DOCuSolve App",
        page_icon="📃",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📃 DOCuSolve")
    st.markdown("""
    Welcome to DOCuSolve System. 
    This app allows you to upload a document and ask questions related to the content within the document.
    """)
    about()
    processor, model_instance = load_model()
    handle_question_answering(processor, model_instance)

if __name__ == "__main__":
    main()
