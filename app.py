import streamlit as st
from main import get_chain,info,summary,explaination

query = st.text_input("Ask your Query : ")

if query:
    st.markdown("###### Information:", unsafe_allow_html=True)
    if st.button('Get Information'):
        i = info(query)
        st.write(i)

    st.markdown("###### Summary:", unsafe_allow_html=True)
    if st.button('Get Summary'):
        s = summary(query)
        st.write(s)

    st.markdown("###### Explanation:", unsafe_allow_html=True)
    if st.button('Get Explanation'):
        e = explaination(query)
        st.write(e)

