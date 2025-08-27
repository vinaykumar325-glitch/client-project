## Importing libraries and files
# task.py
from typing import List, Optional, Any
from agents import Agent
from tools import FinancialDocumentTool

class Task:
    def __init__(self, description: str, expected_output: str, agent: Agent, tools: Optional[List[Any]] = None, async_execution: bool = False):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.tools = tools or []
        self.async_execution = async_execution

# Create tasks (clear prompts)
def create_tasks(financial_analyst: Agent, verifier: Agent):
    analyze_financial_document = Task(
        description="Analyze the uploaded document and extract trends and risks. User query: {query}",
        expected_output="Structured analysis: revenue, profit, cashflow, risks, opportunities.",
        agent=financial_analyst,
        tools=[FinancialDocumentTool.read_data_tool],
    )

    verification = Task(
        description="Verify the uploaded file is a financial document.",
        expected_output="Yes/No with brief reason.",
        agent=verifier,
        tools=[FinancialDocumentTool.read_data_tool],
    )

    return verification, analyze_financial_document
