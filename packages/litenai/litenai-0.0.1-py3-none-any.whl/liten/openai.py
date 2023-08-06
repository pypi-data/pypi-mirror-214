import random
import time
import os
import openai
import tiktoken
from . import utils
from .config import Config
from .utils import Suite

def retry_with_exponential_backoff(
        func,
        initial_delay: float = 1,
        exponential_base: float = 2,
        jitter: bool = True,
        max_retries: int = 4,
        errors: tuple = (openai.error.RateLimitError,),
):
    """Retry a function with exponential backoff with delay with retry multiplies like
      delay *= exponential_base * (1 + jitter * random.random())
    func -- wrapper function
    initial_delay -- in secs (default=1)
    exponential_base -- in sec (default=2)
    jitter -- True/False for varying delay
    max_retries -- Number of retries (default=4)
    errors -- Rate limit error for backoff
    """
 
    def wrapper(*args, **kwargs):
        # Initialize variables
        num_retries = 0
        delay = initial_delay
 
        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)
 
            # Retry on specific errors
            except errors as e:
                # Increment retries
                num_retries += 1
 
                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )
 
                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())
 
                # Sleep for the delay
                time.sleep(delay)
 
            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e
 
    return wrapper
    
@retry_with_exponential_backoff
def chat_completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

# GPT3.5 models https://platform.openai.com/docs/models/gpt-3-5
class GPT35Model:
    gpt_3_5_turbo = 'gpt-3.5-turbo'
    text_davinci_003 = 'text-davinci-003'
    text_davinci_002 = 'text-davinci-002'
    code_davinci_002 = 'code-davinci-002'

class OpenAI:
    """
    Liten openai interface - setup model and prompt
    """
    # timeout secs - wait before the call timeouts
    timeout_secs_=30    
    def __init__(self):
        """
        Initialize openai variables
        """
        self._config = Config()
        openai.api_key= self._config.openai_api_key
        # max tokens must be < 4096, this is number of input tokens TBD move to yml configs
        self._max_tokens=4096
        self._max_output_tokens=1024
        self._max_input_tokens=2*1024
        # Temperature - higher temperature means more variations
        self._temp=0.5
        # n = number of answers to generate
        self._n=1
        # stop 
        self._stop=None
        # model name is like models_.data{id:"modelname"}
        # self.models_=openai.Model.list()
        self._model = GPT35Model.gpt_3_5_turbo
        #self.encoding = tiktoken.get_encoding('cl100k_base')
        self._encoding = tiktoken.encoding_for_model(self._model)
        pass

    @property
    def max_tokens(self):
        """
         Max tokens
        """
        return self._max_tokens;

    @property
    def max_input_tokens(self):
        """
        Max input tokens
        """
        return self._max_input_tokens;

    @property
    def max_output_tokens(self):
        """
        Max output tokens
        """
        return self._max_output_tokens;

    def reduce_prompt_size(self, prompt, num_tokens):
        """
        Reduce prompt size to num_tokens by removing tokens from the end as well as stuff like images etc.
        prompt - prompt to reduce
        num_tokens - number of tokens to reduce to
        """
        tokens=self._encoding.encode(prompt)
        reduced_prompt=prompt
        if (len(tokens) > num_tokens):
            reduced_prompt = self._encoding.decode(tokens[:num_tokens-1])
        return reduced_prompt
    
    def complete_chat(self, messages):
        """
        Complete chat with given messages
        messages - list of messages
        """
        response = chat_completions_with_backoff(
            model=self._model,
            messages=messages,
            max_tokens=self._max_output_tokens, # Max tokens to generate in output
            n=self._n,  # Number of responses
            stop=self._stop,
            temperature=self._temp,
        )
        content = ""
        try:
            content = response['choices'][0]['message']['content']
        except:
            raise Exception('Could not get content from OpenAI response')
        return content

    # Generate SQL prompt from given prompt
    
    def summarize(self,prompt):
        """
        Summarize the given text
        prompt - prompt to summarize
        """
        msg = [
            {"role": "system", "content" : "Summarize the given text"},
            {"role": "user", "content" : prompt}
        ]
        summary = self.complete_chat(msg)
        return summary

    def generate_sql(self,prompt):
        """
        Generate sql from the given prompt
        prompt - prompt to generate sql
        """
        msg = [
            {"role": "system", "content" : "You are a SQL coder. You only generate correct SQL code that does not have any non-SQL statements.The SQL code generated by you can be run without any modifications."},
            {"role": "user", "content": "Generate SQL code for the given description below. the description starts with a triple quote like ``` and ends with another triple quote\n```\n" +
                                        prompt + "\n```\n"}
        ]
        sql = self.complete_chat(msg)
        return sql
    
    def generate_python(self,prompt):
        """
        Generate python code from the given prompt
        prompt - prompt to generate python code
        """
        msg = [
            {"role": "system", "content" : "You are python coder. You only generate correct python code and do not have non-python statements.The python code generated by you can be compiled without any modifications."},
            {"role": "user", "content": "Generate python code for the given description below. the description starts with a triple quote like ``` and ends with another triple quote\n```\n" +
                                        prompt + "\n```\n"}
        ]
        sql = self.complete_chat(msg)
        return sql

    def complete_prompt_chat(self, prompt):
        """
        Complete the given prompt
        prompt - prompt to complete
        """
        msg = [
            {"role": "system", "content" : "Complete the given prompt and its directives"},
            {"role": "user", "content" : prompt}
        ]
        resp = self.complete_chat(msg)
        return resp

    def generate_java_code(self, prompt, class_name):
        """
        Generate java code from the prompt
        """
        msg = [
            {"role": "system", "content" : "Generate java code with a class that performs the given task. The class name must be " + class_name},
            {"role": "user", "content": prompt}
        ]
        java_code = self.complete_chat(msg)
        return java_code

    def generate_junit_code(self, java_code, desc):
        """
        Generate junit code for the given java code
        """
        content_prompt = "Generate java junit test for the given java code. The test code class name should be name of the class with Test appended to the name. "
        if (desc):
            content_prompt = content_prompt+ "This code performs the following operations." + desc
        content_prompt = content_prompt + " This is the actual java code for which you have to generate junit code." + java_code
        msg = [
            {"role": "system", "content" : "Generate java unit junit code with a class that tests the given code."},
            {"role": "user", "content" : content_prompt}
        ]
        junit_code = self.complete_chat(msg)
        return junit_code

