
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import PyPDF2
import io
import openai
import docx2txt
import pyperclip


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_hello = "https://lottie.host/0d49d388-9acb-492c-92c2-8dad820db057/R3WmiFyHXU.json"

lottie_hello = load_lottieurl(lottie_url_hello)


st_lottie(lottie_hello)

st.header('Welcome to the Document Reader App')

openai.api_key =  st.sidebar.text_input("Please enter your openai api key", type='password')



def extract_text_from_pdf(file):
    pdf_file_obj = io.BytesIO(file.read())
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = ""
    
    for page_num in range(len(pdf_reader.pages)):
        page =pdf_reader.pages[page_num]
        text += page.extract_text()
     
    return text    


def extract_text_from_docx(file):
    docx_file_obj = io.BytesIO(file.read())
    text = docx2txt.process(docx_file_obj)
    return text


def extract_text_from_txt(file):
    text = file.read().decode('utf-8')
    return text



def extract_text_from_file(file):
    if file.type == "application/pdf":
        text = extract_text_from_pdf(file)
    elif file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        text =extract_text_from_docx(file)
    elif file.type == 'text/plain':
        text = extract_text_from_txt(file)
    else:
        st.error('Unsupported file type')
        text = None
    return text                

def get_questions_from_gpt(text):
    prompt = text[:4096]
    response =openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0.5, max_tokens=30)
    return response.choices[0].text.strip()


def get_answers_from_gpt(text, question):
    prompt = text[:4096] + "\nQuestion: " + question + "\nAnswer:"
    
    response =openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0.6, max_tokens=2000)
    return response.choices[0].text.strip()
    

def main():
    st.header('Please Uploaded a File')
    
    uploaded_file = st.file_uploader('Choose a file', type=['pdf','docx','txt'])
    
    if uploaded_file is not None:
        
        text = extract_text_from_file(uploaded_file)
        
        if text is not None:
            
            question = get_questions_from_gpt(text)
            
            st.write('Question: ' + question)
            
            user_question = st.text_input('Ask a question about the document')
            
            st.write("---")
            
            
            if user_question:
                
                    answer = get_answers_from_gpt(text, user_question)
                
                    st.write('Answer: ' + answer)
                
                    lottie_url_hello = "https://lottie.host/60153775-c4db-4464-8715-1cdd7cfb6a1f/w7hXrezh1Y.json"

                    lottie_hello = load_lottieurl(lottie_url_hello)

                    st_lottie(lottie_hello)
                
                    st.write('Thank you for using the app, I hope you find this useful and got your answers. If you want to copy the answer, Please click ont the ***Copy Answer Text*** button.')
                
            if st.button('Copy Answer Text'):
                    pyperclip.copy(answer)
                    st.success('Answer text copied to clipboard')
 
if __name__ == "__main__":
    main()
             
