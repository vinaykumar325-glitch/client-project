# main.py
import os
import uuid
from typing import Optional, Dict, Any
from agents import Agent
from tools import FinancialDocumentTool, LocalLLM
from task import create_tasks, Task
from enum import Enum

# Minimal Crew implementation (keeps behavior deterministic and simple)
class Process(Enum):
    sequential = 1
    parallel = 2

class Crew:
    def __init__(self, agents, tasks, process=Process.sequential):
        self.agents = agents
        self.tasks = tasks
        self.process = process

    def kickoff(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        file_path = inputs.get("file_path")
        query = inputs.get("query", "")
        document_text = None
        for idx, task in enumerate(self.tasks):
            if task.tools and file_path:
                for tool in task.tools:
                    try:
                        if callable(tool):
                            document_text = tool(file_path)
                        else:
                            if hasattr(tool, "read"):
                                document_text = tool.read(file_path)
                            elif hasattr(tool, "read_data_tool"):
                                document_text = tool.read_data_tool(file_path)
                            else:
                                document_text = str(tool)
                    except Exception as e:
                        document_text = f"(tool call failed: {e})"
            inputs_for_agent = {"query": query, "document_text": document_text, "file_path": file_path}
            try:
                result = task.agent.run(inputs_for_agent)
            except Exception as e:
                result = {"error": f"agent.run failed: {e}", "raw_inputs": inputs_for_agent}
            results[f"task_{idx}_{getattr(task.agent, 'role', str(task.agent))}"] = result
        return results

# Build agents and tasks
LLM_IMPL = LocalLLM()
financial_analyst = Agent(role="Senior Financial Analyst", goal="Extract key financial metrics and provide concise insights.", tools=[FinancialDocumentTool.read_data_tool], llm=LLM_IMPL)
verifier = Agent(role="Financial Document Verifier", goal="Check whether document resembles a financial report.", llm=LLM_IMPL)
verification_task, analyze_task = create_tasks(financial_analyst, verifier)

def run_crew(query: str, file_path: Optional[str] = None):
    crew = Crew(agents=[financial_analyst], tasks=[verification_task, analyze_task], process=Process.sequential)
    return crew.kickoff({"query": query, "file_path": file_path})

# Test harness (keeps original tests and adds more)
def _write_sample_text_file(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(
            "Tesla Inc. Q2 2025 Update\n"
            "Revenue grew 18% year-over-year to $25,000M. Net income improved to $1,200M.\n"
            "Cash and cash equivalents: $10,500M. Long term debt: $5,200M.\n"
        )

def run_local_tests():
    print("--- Test 1: Text file result ---")
    sample_path = os.path.join("data", "sample.txt")
    _write_sample_text_file(sample_path)
    print(run_crew(query="Summarize Tesla's revenue and risks", file_path=sample_path))

    print("--- Test 2: No file provided ---")
    print(run_crew(query="What are the top-level risks?"))

    test_agent = Agent(role="TestAgent", llm=LocalLLM())

    print("--- Test 3: Agent.run with document_text=None ---")
    print(test_agent.run({"query": "Check behavior", "document_text": None}))

    print("--- Test 4: Agent.run with empty document_text ('') ---")
    print(test_agent.run({"query": "Check empty", "document_text": ""}))

    print("--- Additional tests ---")
    print(test_agent.run({"query": "Number as doc", "document_text": 12345}))
    print(test_agent.run({"query": "Dict as doc", "document_text": {"a": 1}}))
    print("Local tests completed.")

if __name__ == "__main__":
    run_local_tests()
