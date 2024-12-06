def chatCompletion(llm, sampling_params, messages, response_format=None):
    query = '<|begin_of_text|>'
    for message in messages[:-1]:
        query += f'<|start_header_id|>{message["role"]}<|end_header_id|>{message["content"]}<|eot_id|>\n'
    if response_format:
        query += f'<|start_header_id|>{messages[-1]["role"]}<|end_header_id|>{messages[-1]["content"]}\nRespond in this format with no additional output, text, or formatting: {response_format}\n<|eot_id|>\n'
    else:
        query += f'<|start_header_id|>{messages[-1]["role"]}<|end_header_id|>{message[-1]["content"]}<|eot_id|>\n'
    query += '<|start_header_id|>assistant<|end_header_id|>\n'

    output = llm.generate([query], sampling_params)[0]
    return output