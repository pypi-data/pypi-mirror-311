
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.schema import SystemMessage
from langchain.agents import initialize_agent, AgentType
from langchain.tools import BaseTool
from datetime import date
from typing import Type
import json
import pandas as pd

class HRAgent:

    def __init__(self, temperature:float = None,
                llm_ver:str = None,
                model:str = None,
                embed_batch_size:int = None,
                streaming:bool = None,
                verbose:bool = None) -> None:
        self.temperature = temperature
        self.llm_ver = llm_ver
        self.model = model
        self.embed_batch_size = embed_batch_size
        self.streaming = streaming
        self.verbose = verbose

    def get_agent(self,last_message=None, callback_handler=None,
                  name:str = None,
                  employee_name:str = None,
                  companies:list[str] = None,
                  content:str = None):
        name = name
        employee_name = employee_name
        year = date.today().year
        print(f'GET AGENT YEAR={year}')
        companies = companies
        print(f'COMPANIES={companies}')
        content=content
        # if (employee_name != None) and (len(employee_name) > 0):
        #     content +=f"\n5/ You are currently talking about the employee {employee_name}"
        if last_message:
            content +=f"\n5/ The last response you sent was: \"{last_message[1]}\""
        print(content)
        system_message = SystemMessage(content)

        tools = [
            HRRecordsTool(),
            LeavesTool(),
            EmployeeListTool(),
        ]
        agent_kwargs = {
            "system_message": system_message,
        }
        llm_ver = "gpt-4"
        if callback_handler != None:
            llm=ChatOpenAI(temperature=1.0, model_name=llm_ver, streaming=True, callbacks=callback_handler)
        else:
            llm = ChatOpenAI(temperature=0, model=llm_ver, verbose=True)
        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            agent_kwargs=agent_kwargs,
        )

        return agent

class HRRecordsInput(BaseModel):

    def __init__(self) -> None:
        pass

    """Inputs for get_content function"""
    first_name: str = Field(description="The first name of the employee to get records for.")
    last_name: str = Field(description="The last name of the employee to get records for.")
    start_date: date = Field(description="The start date of the entries that you want to query. Set to None if not specifically asked for a joining date.")
    end_date: date = Field(description="The end date of the entries that you want to query. Set to None if not specifically asked for a joining date.")



class HRRecordsTool(BaseTool):

    def __init__(self, doc, emp, path) -> None:
        self.doc = doc
        self.emp = emp
        self.path = path
        self.name = "hr_records_tool"
        self.description = "Use to get information about an employee. Whenever you see a record_url in your result, render it as a link."
        self.args_schema: Type[BaseModel] = HRRecordsInput

    def get_data(self, start_date=None, end_date=None):

        if start_date == 'None':
            start_date = None
        if end_date == 'None':
            end_date = None
        if len(first_name) > 0:
            first_name = first_name.split()[0]
        if len(last_name) > 0:
            last_name = last_name.split()[-1]
        print(f'{first_name} {last_name} {start_date} {end_date}')
        doc = self.doc
        print(doc)
        if len(doc) > 0:
            name = doc[0]['name']
            emp = self.emp
            print (type(emp))
            emp_dict = emp.__dict__
            emp_dict['record_url'] = f'/app/employee/{name}'
            print (emp_dict)
            return emp_dict
        else:
            return "Employee Not Found"

    def get_conn_string(self):
        path = f'{self.path}/site_config.json'
        with open(path) as file:
            j = json.load(file)
            print(j)
            conn_string = f'mariadb+pymysql://{j["db_name"]}:{j["db_password"]}@localhost:3306/{j["db_name"]}'
            return conn_string

    def _run(self, first_name: str, last_name: str, start_date: date, end_date : date):
        return self.get_data(first_name, last_name, start_date, end_date)

    def _arun(self,  first_name: str, last_name: str, attr: str):
        raise NotImplementedError("error here")
    

class LeavesInput(BaseModel):

    def __init__(self) -> None:
        pass
    
    """Inputs for get_content function"""
    first_name: str = Field(description="The first name of the employee to get records for.")
    last_name: str = Field(description="The last name of the employee to get records for.")
    start_date: date = Field(description="The start date of the entries that you want to query")
    end_date: date = Field(description="The end date of the entries that you want to query")


class LeavesTool(BaseTool):

    def __init__(self, doc, emp, path) -> None:
        self.doc = doc
        self.emp = emp
        self.path = path
    
    name = "leaves_tool"
    description = "Use to get information about an employee's leaves. Use only if specifically asked about leaves."
    args_schema: Type[BaseModel] = LeavesInput


    def get_data(self, first_name, last_name, start_date=None, end_date=None):
        print(f'{first_name} {last_name} {start_date} {end_date}')
        doc = self.doc
        print(doc)
        # return "doc"
        if len(doc) > 0:
            emp = self.emp
            return emp
        else:
            return "Employee Not Found"

    def get_conn_string(self):
        path = f'{self.path}/site_config.json'
        with open(path) as file:
            j = json.load(file)
            print(j)
            conn_string = f'mariadb+pymysql://{j["db_name"]}:{j["db_password"]}@localhost:3306/{j["db_name"]}'
            return conn_string

    def _run(self, first_name: str, last_name: str, start_date: date, end_date : date):
        return self.get_data(first_name, last_name, start_date, end_date)

    def _arun(self,  first_name: str, last_name: str, attr: str):
        raise NotImplementedError("error here")


class EmployeeListInput(BaseModel):

    def __init__(self) -> None:
        pass
    
    """Inputs for get_content function"""
    company: str = Field(description="The company to get records for. Set to blank to a list for all companies.")
    start_date: date = Field(description="The start date of the entries that you want to query. Set to January 1, 1970 if not specifically asked for a joining date.")
    end_date: date = Field(description="The end date of the entries that you want to query. Set to the end of the current year if not specifically asked for a joining date.")
    status: str = Field(description="The employee status to look for. Possibe values are ['Active', 'Inactive', 'Suspended', 'Left']")
    


class EmployeeListTool(BaseTool):

    def __init__(self, doc, emp, path) -> None:
        self.doc = doc
        self.emp = emp
        self.path = path
    
    name = "employee_list_tool"
    description = "Use to get a list of employees for a company, Always provide full names. When presenting a list, include the record_url rendered as a link."
    args_schema: Type[BaseModel] = EmployeeListInput


    def get_data(self, company, start_date=None, end_date=None, status='Active'):
        print(f'{company} {start_date} {end_date}')
        fields=['name', 'first_name', 'last_name', 'company', 'status', 'designation', 'date_of_joining', 'relieving_date']
        filters={'status':status,}
        if start_date and start_date != 'None':
            if status == 'Left':
                filters['relieving_date'] = ['between', [start_date, end_date]]
            else:
                filters['date_of_joining'] = ['between', [start_date, end_date]]
        if company:
            filters['company'] = company
        doc = self.doc
        print(doc)
        # if len(doc) > 100:
        #     doc = doc[:100]
        if len(doc) > 0:
            df = pd.DataFrame.from_records(doc)
            df['full_name'] = df['first_name'] +' '+df['last_name']
            df['record_url'] = df.apply(lambda x: f"/app/employee/{x['name']}", axis=1)
            df.drop(columns=['name' ,'first_name', 'last_name'], inplace=True)
            return df
        return 'No Records Found'

    def get_conn_string(self):
        path = f'{self.path}/site_config.json'
        with open(path) as file:
            j = json.load(file)
            print(j)
            conn_string = f'mariadb+pymysql://{j["db_name"]}:{j["db_password"]}@localhost:3306/{j["db_name"]}'
            return conn_string

    def _run(self, company: str, start_date: date, end_date : date, status: str):
        return self.get_data(company, start_date, end_date, status)

    def _arun(self,  company: str, attr: str):
        raise NotImplementedError("error here")