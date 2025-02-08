>>> from sonic.utils.genai.llm.llm import LLM
>>> llm_model = LLM(model='gpt-3.5-turbo', api_key='sk-proj-123456')
>>> llm_model.generate(messages=[{'role' : 'user', 'content' : 'what is the capital of USA?'}])
2024-11-18 09:03:33,258 - utils.logger - INFO - (llm.py:21) - Generating response using model gpt-3.5-turbo
2024-11-18 09:03:34,106 - utils.logger - WARNING - (posthog.py:50) - PostHog is not initialized. Skipping event tracking.
2024-11-18 09:03:34,106 - utils.logger - INFO - (llm.py:65) - Generated response using model gpt-3.5-turbo
ModelResponse(id='chatcmpl-AUzRtOBTmn3HGZkpJObJd1XYWSKyk', created=1731949413, model='gpt-3.5-turbo-0125', object='chat.completion', system_fingerprint=None, choices=[Choices(finish_reason='stop', index=0, message=Message(content='Washington D.C.', role='assistant', tool_calls=None, function_call=None))], usage=Usage(completion_tokens=8, prompt_tokens=14, total_tokens=22, completion_tokens_details=CompletionTokensDetailsWrapper(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0, text_tokens=None), prompt_tokens_details=PromptTokensDetailsWrapper(audio_tokens=0, cached_tokens=0, text_tokens=None, image_tokens=None)), service_tier=None)
