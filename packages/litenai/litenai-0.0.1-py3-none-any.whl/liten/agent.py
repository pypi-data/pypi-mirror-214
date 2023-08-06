from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, TimestampType
from .openai import OpenAI
from .workitem import WorkItem
from . import utils
from pyspark.sql.functions import *

import json

class Agent:
    """
    Liten agent is a collection of work units in Liten. AI uses it for fine tuning the model.
    """
    def __init__(self, name, spark):
        """
        Initialize workitem array
        """
        self._openai = OpenAI()
        self._workitems = []
        self._name = name
        self._spark = spark
        pass

    def _add_workitem(self, workitem):
        self._workitems.append(workitem)

    def load(self, nbname):
        """
        Read python notebook using a json reader
        """
        # This is the cell layout in json
        """
        {
         cells [
          cell_type : 'code'|'markdown',
          execution_count : integer,
          id : '',
          metadata : { },
          source : [
           'commands'
          ],
          outputs : [
            name : 'stdout'|'stderr',
            output_type: 'stream'|'execute_result'|'display_data'
            text: [
             'output_lines'
            ],
          ]
        }
        """
        #
        # All cells are dicts with at least these three values 
        #   type(code or markdown), user (user prompt), assistant (response prompt)
        #   for now only collect code type and their results
        #
        with open(nbname) as datafile:
            data = json.load(datafile)
            for c in data['cells']:
                workitem = WorkItem()
                if 'code' == c['cell_type']:
                    workitem.set_type('code')
                    if 'source' in c.keys():
                        workitem.set_source(c['source'])
                    if 'outputs' in c.keys():
                        for out_vals in c['outputs']:
                            if 'output_type' in out_vals and 'text' in out_vals:
                                if (out_vals['output_type'] == 'stream'):
                                    workitem.set_output(out_vals['text'])
                    self._add_workitem(workitem)
                    
    def json_dump(self):
        workitem_dumps = []
        for workitem in self._workitems:
            workitem_dumps.append(workitem.json_dump())
        return json.dumps(workitem_dumps)

    def num_workitems(self):
        return len(self._workitems)

    def get_workitem(self, item):
        if item < 0 or item >= len(self._workitems):
            print(f"Work {item}: does not exist")
            return None
        return self._workitems[item]

    def reduce_prompt_size(self, prompt):
        """
        remove image etc to reduce prompt size
        """
        return self._openai.reduce_prompt_size(prompt, self._openai.max_input_tokens)

    def summarize_item(self, item):
        workitem = self.get_workitem(item)
        if workitem is None:
            return  
        workitem.summarize()
        print(f"Workitem {item}: {workitem.summary()}\n")
    
    def summarize(self):
        for workitem in self._workitems:
            workitem.summarize()
            print(f"Workitem {workitem.item()}: {workitem.summary()}\n")
        
    def replay(self, item):
        """
        Replay the queries of a work
        """
        workitem = self.get_workitem(item)
        if workitem is None:
            return
        utils.create_new_cell(workitem.source())
        return

    def explain(self, item):
        """
        Explain a work id
        """
        workitem = self.get_workitem(item)
        if workitem is None:
            return
        s = workitem.explain()
        print(f"Work {id}: {s.strip()}\n")
        return
    
    def find_similar(self, prompt):
        syscontent = "Find a list of works below. Each work starts with work keyword followed by a number. It is followed by a short summary.\n"
        for workitem in self._workitems:
            syscontent += f"Work {workitem.item()} = {workitem.summarize()}\n"
        rsyscontent = self.reduce_prompt_size(syscontent)
        chatprompt = "List the work closest to the following work summary.\n"
        chatprompt += prompt
        rchatprompt = self.reduce_prompt_size(chatprompt)
        msg = [
            {"role": "system", "content" : rsyscontent},
            {"role": "user", "content" : rchatprompt}
        ]        
        answer = self._openai.complete_chat(msg).strip()
        print(answer)
        return
        
    def complete_chat(self, prompt):
        return self._openai.complete_chat(prompt)

    def generate_sql(self, prompt):
        return self._openai.generate_sql(prompt)
    
    def complete_data_chat(self, df, prompt):
        completed_chat = False
        if 'syslog' == self._name:
            try:
                self.complete_syslog_data_chat(df, prompt)
                completed_chat = True
            except:
                print("Agent was syslog but data does not have syslog schema. Will use general schema.")
        if not completed_chat:
            usercontent = f"""Find a log data file below. This starts with a triple quote like ``` and ends with triple quote ``` again. Each line is a single row of data. All fields in that row are separated by comma. Read this data and respond to the following prompt.
{prompt}
```
            """
            num_cols = len(df.columns)
            for d in df.collect():
                for i in range(0 , num_cols):
                    usercontent += f"{d[i]},"
                usercontent += '\n'
            rusercontent = self.reduce_prompt_size(usercontent)
            rusercontent += """```"""
            msg = [
                {"role": "user", "content" : rusercontent}
            ]
            answer = self._openai.complete_chat(msg).strip()
            print(answer)
        return
        
    def complete_syslog_data_chat(self, df, prompt):    
        usercontent = f"""Find a log data generated by Linux system log file. This starts with a triple quote like ``` and ends with triple quote ``` again. Read this data and respond to the following prompt.
{prompt}
```
        """
        #  Jun 14 15:16:01 combo sshd(pam_unix)[19939]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4                
        for r in df.collect():
            timestr = ""
            if r['timestamp']:
                timestr = to_date(r['timestamp'],'MMM DD HH:mm:ss')           
            usercontent += f"""{timestr} {r['hostname']} {r['process']}({r['pid']}); {r['message']}\n"""

        rusercontent = self.reduce_prompt_size(usercontent)
        rusercontent += """```"""
        msg = [
            {"role": "user", "content" : rusercontent}
        ]        
        answer = self._openai.complete_chat(msg).strip()
        print(answer)
        return

    def analyze(self, df, prompt):
        """
        Analyze the given dataframe based on the prompt
        df: dataframe to analyze
        prompt: prompt to analyze the dataframe
        """
        self.complete_data_chat(df, prompt)
        return
