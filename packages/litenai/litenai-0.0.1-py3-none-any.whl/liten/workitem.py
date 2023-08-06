from .openai import OpenAI
import json

class WorkItem:
    """
    A WorkItem with code snippet and _output data
    """
    def __init__(self):
        """
        Create a WorkItem
        """
        self._type=None
        self._output=[]
        self._source=[]
        self._summary=None
        self._explanation=None
        self._openai = OpenAI()

    def type(self):
        return self._type

    def set_type(self, value):
        self._type = value
    
    def source(self):
        return self._source

    def set_source(self, value):
        self._source = value

    def _output(self):
        return self._output

    def set_output(self, value):
        self._output = value

    def summary(self):
        return self._summary

    def reduce_prompt_size(self, prompt):
        """
        remove image etc to reduce prompt size
        """
        return self._openai.reduce_prompt_size(prompt, self._openai.max_input_tokens)
        
    def summarize(self):
        if self._summary:
            return self._summary
        prompt = """ Following are outputs from sql and python commands in a python notbook. The input commands follows input keyword. Input commands is printed in json from  a python array. The output result follows output keyword. Output is aldo printed in json format from a python array.
        Can you summarize what it is trying to do?

        """
        prompt += "input="
        prompt += json.dumps(self._source)
        prompt += "\n  output="
        prompt += json.dumps(self._output)
        rprompt = self.reduce_prompt_size(prompt)
        self._summary = self._openai.summarize(rprompt).strip()
        return self._summary

    def explain(self):
        if self._explanation:
            return self._explanation        
        syscontent = """ Following are outputs from sql and python commands in a python notebook. The input commands follows input keyword. Input commands are a list of string printed in json format fora python array. The output result follows output keyword. Output commands are also a list of string printed in json format from a python array.
        Can you explain what it is trying to do?
        """
        prompt += "input="
        prompt += json.dumps(self._source)
        prompt += "\noutput="
        prompt += json.dumps(self._output)
        rprompt = self.reduce_prompt_size(prompt)
        msg = [
            {"role": "system", "content" : syscontent},
            {"role": "user", "content" : rprompt}
        ]
        self._explanation = self._openai.complete_chat(msg)
        return self._explanation

    def json_dump(self):
        return json.dumps([self._type,self._source,self._output])
    
           
