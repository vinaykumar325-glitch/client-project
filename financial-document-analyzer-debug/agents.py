# agents.py
from typing import Any, Dict, List, Optional
from .tools import FinancialDocumentTool, LocalLLM

# Use the LocalLLM by default (safe fallback).
LLM_IMPL = LocalLLM()

class Agent:
    def __init__(
        self,
        role: str = "Agent",
        goal: str = "",
        verbose: bool = False,
        memory: bool = False,
        backstory: str = "",
        tools: Optional[List[Any]] = None,
        llm: Optional[Any] = None,
        max_iter: int = 1,
        max_rpm: int = 10,
        allow_delegation: bool = False,
        **kwargs,
    ):
        self.role = role
        self.goal = goal
        self.verbose = verbose
        self.memory = memory
        self.backstory = backstory
        self.tools = tools or []
        self.llm = llm or LLM_IMPL
        self.max_iter = max_iter
        self.max_rpm = max_rpm
        self.allow_delegation = allow_delegation

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run a minimal analysis and return a structured dict.

        Safety: never slices None. Handles non-string document_text values.
        """
        prompt_parts: List[str] = [f"Role: {self.role}", f"Goal: {self.goal}"]
        query_val = inputs.get("query")
        if isinstance(query_val, str) and query_val:
            prompt_parts.append(f"User query: {query_val}")

        doc_text = inputs.get("document_text")
        if isinstance(doc_text, str) and doc_text:
            excerpt = doc_text[:2000] + ("..." if len(doc_text) > 2000 else "")
            prompt_parts.append("Document excerpt:\n" + excerpt)

        prompt = "\n\n".join(prompt_parts)

        # LLM generate if supported
        if hasattr(self.llm, "generate"):
            try:
                summary = self.llm.generate(prompt)
            except Exception as e:
                summary = f"(llm.generate raised an exception: {e})"
        else:
            summary = str(self.llm)

        # Safe raw_inputs preview: don't slice None
        raw_inputs = {}
        for k, v in inputs.items():
            if k == "document_text":
                if v is None:
                    raw_inputs[k] = None
                elif isinstance(v, str):
                    raw_inputs[k] = v[:200] + ("..." if len(v) > 200 else "") if v else ""
                else:
                    try:
                        s = str(v)
                        raw_inputs[k] = s[:200] + ("..." if len(s) > 200 else "")
                    except Exception:
                        raw_inputs[k] = "(unrepresentable)"
            else:
                raw_inputs[k] = v

        return {"role": self.role, "summary": summary, "raw_inputs": raw_inputs}
