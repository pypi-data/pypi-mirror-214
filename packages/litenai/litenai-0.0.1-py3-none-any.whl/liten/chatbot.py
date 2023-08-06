from .openai import OpenAI

import panel as pn
import pandas as pd
import hvplot

import pyspark
from pyspark.sql import SparkSession

from io import StringIO
from contextlib import redirect_stdout
from contextlib import redirect_stderr

class ChatBot:
    def __init__(self, sc) -> None:
        pn.extension()
        self._spark = sc
        self._df = None
        self._openai = OpenAI()
        self._panels = [] # Collect all display
        self._width = 1000 # Default pixel width
        self._context = [ {'role':'system', 
                            'content':"""
You are a Bot, an automated service to talk to users. Your job is to analyze data files and \
answer user queries. 
"""} ]
        self._inp = pn.widgets.TextAreaInput(value="Hi", placeholder='Enter text here…', max_length=2000, height=200, width=self._width)
        # Default action is ask
        self._action_ask = 'Ask'
        self._action_codegen = 'Codegen'
        self._action_work = 'Work'
        self._action_analyze = 'Analyze'
        self._action_execute = 'Execute'
        self._action_plot = 'Plot'

        self._action = self._action_ask
        # action widget holds the current action from selection widget
        self._action_widget = pn.widgets.Select(name='Action',
                                                options=[self._action_ask, 
                                                        self._action_codegen,
                                                        self._action_work,
                                                        self._action_analyze,
                                                        self._action_execute,
                                                        self._action_plot])

        button_conversation = pn.widgets.Button(name="Chat",align='center')
        interactive_conversation = pn.bind(self._collect_messages, button_conversation)
        self._panel = pn.panel(interactive_conversation, loading_indicator=True, width=self._width, default_layout=pn.Row)

        self._row = pn.Row('Actions',
                            self._action_widget,
                            button_conversation)
        pass

    @property
    def spark(self):
        return self._spark
    
    def _ask_collect_messages(self,_):
        prompt = self._inp.value_input
        self._inp.value = ''
        self._context.append({'role':'user', 'content':f"{prompt}"})
        response = self._openai.complete_chat(self._context) 
        self._context.append({'role':'assistant', 'content':f"{response}"})
        self._panels.append(
                pn.Row('You:', pn.pane.Markdown(prompt, width=self._width)))
        self._panels.append(
                pn.Row('Bot:', pn.pane.Markdown(response, width=self._width, styles={'background-color': '#F6F6F6'})))
        pass
    
    def _codegen_collect_messages(self,_):
        prompt = self._inp.value_input
        self._inp.value = ''
        code_str = self._openai.generate_sql(prompt)
        self._context.append({'role':'user', 'content':f"Generate SQL code for {prompt}"})
        self._context.append({'role':'assistant', 'content':f"{code_str}"})
        self._panels.append(
            pn.Row('You:', pn.pane.Markdown(prompt, width=self._width)))
        self._panels.append(
            pn.Row('Bot:', pn.pane.Markdown(code_str, width=self._width, styles={'background-color': '#F6F6F6'})))
        pass
    
    def _execute_collect_messages(self,_):
        prompt = self._inp.value_input
        self._inp.value = ''
        self._panels.append(
            pn.Row('Bot:', pn.pane.Markdown(f'Executing {prompt} ...', width=self._width, styles={'background-color': '#F6F6F6'}))
        )

        exec_prompt = f"""
import liten
# Read local .env as os.environ['OPENAI_API_KEY']
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
ten = liten.Session()
spark = ten.spark
self._df=spark.sql(\"\"\"
{prompt}
\"\"\")
self._df.show(5)
"""
        fout = StringIO()
        ferr = StringIO()
        with redirect_stdout(fout), redirect_stderr(ferr):
            exec(exec_prompt)
        response = fout.getvalue()
        response += ferr.getvalue()
        self._panels.append(
            pn.Row('Bot:', pn.pane.Markdown(response, width=self._width, styles={'background-color': '#F6F6F6'})))
        pass

    def _plot_collect_messages(self,_):
        if self._df is None:
            self._panels.append(
                pn.Row('Bot:', pn.pane.Markdown('No data to plot', width=self._width, styles={'background-color': '#F6F6F6'}))
            )
        else:
            pandas_df = self._df.na.drop().toPandas()
            pandas_df['time'] = pd.to_datetime(pandas_df['time'])
            explorer_plot = hvplot.explorer(pandas_df)
            self._panels.append(explorer_plot)
        pass

    def _analyze_collect_messages(self,_):
        self._panels.append(
            pn.Row('Bot:', pn.pane.Markdown('Action Analyze not yet supported', width=self._width, styles={'background-color': '#F6F6F6'}))
        )
        pass
    
    def _work_collect_messages(self,_):
        self._panels.append(
            pn.Row('Bot:', pn.pane.Markdown('Action Work not yet supported', width=self._width, styles={'background-color': '#F6F6F6'}))
        )
        pass

    def _collect_messages(self,_):
        self._action = self._action_widget.value
        if self._action == self._action_ask:
            self._ask_collect_messages(_)
        elif self._action == self._action_codegen:
            self._codegen_collect_messages(_)
        elif self._action == self._action_analyze:
            self._analyze_collect_messages(_)
        elif self._action == self._action_work:
            self._work_collect_messages(_)
        elif self._action == self._action_execute:
            self._execute_collect_messages(_)
        elif self._action == self._action_plot:
            self._plot_collect_messages(_)
        else:
            self._panels.append(
                pn.Row('Bot:', pn.pane.Markdown(f'Unknown Action {self._action}', width=self._width, styles={'background-color': '#F6F6F6'}))
            )   
        return pn.Column(*self._panels)

    def start(self):
        """
        Return the plot for the chatbot
        """
        col_panels = pn.Column(
            self._inp,
            self._row,
            self._panel,
        )
        return col_panels