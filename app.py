import streamlit as st
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import random
from load_css import local_css
local_css("style.css")
#from PIL import Image


st.set_page_config(layout="wide")
st.title('Cloze test generator')

#@st.cache
def tokenization(paragraph):
    sents = nltk.sent_tokenize(paragraph)
    words = [nltk.word_tokenize(sent) for sent in sents]
    return sents, words

def clozeGeneration(text):   
    sents, words = tokenization(text)
    posWords = [nltk.pos_tag(word) for word in words]

    punctuation = '[-()\'"#/@;:<>{}`+=~|.,!?i.e.e.g.ieeg]'

    fillSents = sents
    answers = []

    i = 0
    number = 1
    
    random_num = random.randint(3, 13) 
    for posWord in posWords:
        for x in enumerate(posWord):
            if x[0] == random_num:
                if x[1][0] not in punctuation and x[1][1] != "CD" and len(x[1][0]) > 1:
                    fillSents[i] = fillSents[i].replace(" " + x[1][0], ' (' + str(number) + ') __________', 1) 
                    answers.append('(' + str(number) + ') ' + str(x[1][0]))
                    number += 1
                else:
                    pass
        i += 1
        

    finalSents = ' '.join(fillSents)
    answers = ' '.join(answers)
    return finalSents, answers



tabs_font_css = """
<style>
div[class*="stTextArea"] label {
  font-size: 26px;
  font-weight: bold;
  height: 800;
}
"""
st.write(tabs_font_css, unsafe_allow_html=True)

with st.empty():  
    text = st.text_area('Text', 'Input text here.', key="inputted_text")

col1, col2, col3 = st.columns(3)
with col2 : 
    generation = st.button('Generate a Cloze test')



with st.empty(): 
    st.markdown('##')
with st.empty(): 
    st.subheader('Cloze test')

container_cloze = st.empty()



with st.empty(): 
    st.markdown('##')
with st.empty(): 
    st.markdown("""<h1 style="height:2px;border:none;color:#e5e4e2;background-color:#e5e4e2;" /> """, unsafe_allow_html=True)

if 'count' not in st.session_state:
    st.session_state.count = 0

if generation:
    st.session_state.count += 1

    clozeTest = clozeGeneration(text)
    container_cloze.markdown(f'<h5 style="color:#000000; background-color: #FFFFFF; padding: 10px; border-radius: 10px; font-size: 16px; font-weight: 400;">{clozeTest[0]} </h5>', unsafe_allow_html=True)

    st.subheader('Answers')
    with st.expander("See answers"):
        st.markdown(f'<h5 style="color:#000000; background-color: #FFFFFF; padding: 10px; border-radius: 10px; font-size: 16px;"> {clozeTest[1]} </h5>', unsafe_allow_html=True)

    st.legacy_caching.clear_cache()

