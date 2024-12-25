import streamlit as st
from langchain_openai import ChatOpenAI
from openai import OpenAIError
import os

# 필요한 함수 임시 구현
def view_sourcecode(file_name):
    st.write(f"Source code of {file_name} will be displayed here.")

def modelName():
    return "gpt-3.5-turbo"

# 체인 생성 함수
def createChain(llm, output_parser):
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a caring teacher who answers students' questions."),
        ("user", "{input}")
    ])
    if output_parser:
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
    else:
        chain = prompt | llm
    return chain

# OpenAI API와 상호작용하는 함수
def generate_text(api_key, input_text, whatToAsk, language):
    try:
        model_name = modelName()
        llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name)

        if whatToAsk == 'Basic':
            st.write("- *기본적인 LLM 사용 방식입니다.*")
            generated_text = llm.invoke(f"Please answer this question in {language}. {input_text}")
        elif whatToAsk == 'ChatPromptTemplate':
            chain = createChain(llm, output_parser=False)
            st.write("- *ChatPromptTemplate을 사용한 프롬프트 구조화.*")
            generated_text = chain.invoke({"input": f"Please answer this question in {language}. {input_text}"})
        else:
            chain = createChain(llm, output_parser=True)
            st.write("- *출력 파서를 사용한 체인 응답 구조화.*")
            generated_text = chain.invoke({"input": f"Please answer this question in {language}. {input_text}"})

        return generated_text
    except OpenAIError as e:
        st.warning("OpenAI API에서 에러가 발생했습니다.")
        st.warning(e)

# 메인 함수
def main():
    st.title('LangChain Quickstart')

    # 사용자 입력 받기
    api_key = st.text_input("OpenAI API 키를 입력하세요:", type="password")
    input_text = st.text_input("질문을 입력하세요:")
    st.write(f"입력된 질문: {input_text}")

    whatToAsk = st.radio(
        "LLM 질문 방식 선택:",
        ["Basic", "ChatPromptTemplate", "StrOutputParser"]
    )

    languages = ["English", "Korean", "Spanish", "French", "German", "Chinese", "Japanese"]
    selected_language = st.selectbox("언어를 선택하세요:", languages)

    if st.button("제출"):
        if api_key:
            with st.spinner("응답을 생성 중입니다..."):
                response = generate_text(api_key, input_text, whatToAsk, selected_language)
                st.write(response)
        else:
            st.warning("OpenAI API 키를 입력하세요.")

    # 현재 소스 코드 보기
    current_file_name = os.path.basename(__file__)
    view_sourcecode(current_file_name)

if __name__ == "__main__":
    main()
