'''
Descripttion: 
version: 
Author: Gezhaoyuan
Date: 2024-04-30 20:34:34
LastEditors: Gezhaoyuan
LastEditTime: 2024-04-30 21:51:32
'''
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate


from flask import Flask, jsonify, request

# 初始化flask app
app = Flask(__name__)

prompt_translation = """
    zh-en translation of "input".
    Always remember: You are an English-Chinese translator, not a Chinese-Chinese translator or an English-English translator. 
    Your output should only contains Chinese or English!
    You should Always just do the translate part and do not change its meaning! 

    example1:
    input:"write me a poem",
    output:"帮我写一首诗"

    example2:
    input:"你好世界",
    output:"hello world"

    Now I will give you my input:
"""

# Define prompt
prompt_summarize = """Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:"""
prompt = PromptTemplate.from_template(prompt_summarize)


# 调用智谱glm-4模型翻译
def translation():
    user_content = request.json.get('user-content')
    if not user_content:
        return jsonify({'error': 'No user-content provided'}), 400

    contentPrompt = prompt_translation

    completion = client.chat.completions.create(
        model='glm-4',
        messages=[
            {"role": "system", "content": contentPrompt},
            {"role": "assistant", "content": user_content}
        ],
        max_tokens=200,
        temperature=0.1,
    )

    # 将 ChatCompletionMessage 对象转换为可序列化的格式
    response_message = completion.choices[0].message.content if completion.choices[0].message else "No response"

    return jsonify({"response": response_message})

# 调用OpenAI的gpt模型生成文本总结
def summarize(text):
    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    docs = loader.load()
    summary = stuff_chain.run(docs)
    return jsonify({"response": summary})

# 获取所有功能列表接口
@app.route('/api/functions', methods=['GET'])
def get_functions():
    functions = [
        {"name": "translation", "endpoint": "/api/translation", "method": "POST"},
        {"name": "Summarize", "endpoint": "/api/summarize", "method": "POST"}
    ]
    return jsonify(functions)

# 调用具体功能接口
# 中英互译翻接口
@app.route('/api/translation', methods=['POST'])
def translation():
    data = request.json
    text = data.get('user-content', '')
    translated_text = translation(text)
    return jsonify({"translated_text": translated_text})

# 总结接口
@app.route('/api/summarize', methods=['POST'])
def summarize_endpoint():
    data = request.json
    text = data.get('text', '')
    summarized_text = summarize(text)
    return jsonify({"summarized_text": summarized_text})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
