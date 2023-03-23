import requests
import streamlit as st

prompt_examples = {
    "Fact": "Question: Where were the 2004 Olympics held?\nAnswer: Athens, Greece\r\n\r\nQuestion: What is the longest river on the earth?\r\nAnswer:",
    "Chatbot": "A chat between a curious human and the Statue of Liberty.\n\r\nHuman: What is your name?\r\nStatue: I am the Statue of Liberty.\r\nHuman: Where do you live?\r\nStatue: New York City.\r\nHuman: How long have you lived there?",
    "Airport Code": "Extract the airport codes from this text.\n\r\nText: \"I want a flight from New York to San Francisco.\"\r\nAirport codes: JFK, SFO.\r\n\r\nText: \"I want you to book a flight from Phoenix to Las Vegas.\"\r\nAirport codes:",
    "Translation": "English: I want to go home.\nChinese: 我想回家。\r\n\r\nEnglish: I don't know.\r\nChinese: 我不知道。\r\n\r\nEnglish: I am hungry.\r\nChinese:",
    "Cryptocurrency": "Every year, cryptocurrency experts prepare forecasts for the price of Dogecoin. In 2025, it is estimated that DOGE will",
    "Code": "def fib(k):\n    \"\"\"Returns the k-th Fibonacci number. Check the corner cases.\"\"\"",
    "Math": "Question: If x is 2 and y is 5, what is x + 2y?\nAnswer: x + 2y = 2 + 2(5) = 2 + 10 = 12\r\n\r\nQuestion: If x is 8 and y is 9, what is 3x + y?\r\nAnswer: 3x + y = 3(8) + 9 = 24 + 9 = 33\r\n\r\nQuestion: If x is 7 and y is 6, what is x + 4y?\r\nAnswer:",
}

def page_config():
    st.set_page_config(
        page_title="Llama",
        layout="wide"
    )
    st.title("LLM Whitespace")
    st.write("")
    st.markdown(
        "###### Powered by BLOOMZ")
    st.markdown(
        "###### Please input non-classified data only to prevent potential data breaches.")
    st.markdown(
        "###### Warning: This model might generate something offensive. No safety measures are in place.")
    st.write("")
    st.write("")

    if "prompt" not in st.session_state:
        st.session_state["prompt"] = prompt_examples["Fact"]

    # best effort spacing guesses since underlying implementation is a flexbox
    # ref: https://discuss.streamlit.io/t/regarding-layout-of-streamlit-web-app/9602/5
    for k, col in zip(prompt_examples, st.columns([.07, .09, .12, .11, .13, .07, .9])):
        if col.button(k):
            st.session_state["prompt"] = prompt_examples[k]

    prompt = st.text_area("Type the prompts here", height=200, key="prompt")
    length = st.slider("Response Length:", 0, 256, 64)
    temperature = st.slider("Temperature:", 0.0, 1.0, 0.7)
    top_p = st.slider("Top-p:", 0.0, 1.0, 0.7)
 
    return prompt, length, temperature, top_p

def main():
    prompt = ""
    prompt, length, temperature, top_p = page_config()
    if st.button("Generate"):
        if len(prompt)>0 :
            col1, = st.columns(1)
            with col1:
                st.success("Answer from BLOOMZ")

            with col1:
                with st.spinner("⌛ Getting result from BLOOMZ"):
                    pload = {
                        "model": "default",
                        "prompt": prompt,
                        "max_tokens": length,
                        "temperature": temperature,
                        "top_p": top_p,
                    }
                    resp = requests.post(url="https://llama.govtext.gov.sg:20001/completions", json=pload).json()
                    st.text_area("Response", prompt + resp["choices"][0]["text"], height=200, label_visibility="hidden")

        else:
            st.warning("Please give me a prompt")

        


if __name__ == "__main__":
    main()
