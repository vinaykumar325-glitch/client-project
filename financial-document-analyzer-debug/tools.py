## Importing libraries and files

import os
from typing import List, Any

# LocalLLM and PDFLoader are defined here for re-use across modules.
class LocalLLM:
    def __init__(self, model: str = "local-llm", temperature: float = 0.0):
        self.model = model
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        if not prompt:
            return "(no content)"
        lower = prompt.lower()
        keywords = [
            "revenue", "net income", "profit", "loss", "ebitda", "cash",
            "assets", "liabilities", "earnings", "guidance", "margin", "debt",
        ]
        snippets: List[str] = []
        for kw in keywords:
            idx = lower.find(kw)
            if idx != -1:
                start = max(0, idx - 80)
                end = min(len(prompt), idx + 240)
                snippets.append(prompt[start:end].strip())
        if snippets:
            return "\n---\n".join(snippets)
        return prompt[:400] + ("..." if len(prompt) > 400 else "")

class PDFLoader:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> List[Any]:
        class Page:
            def __init__(self, page_content: str):
                self.page_content = page_content

        if not os.path.exists(self.path):
            return [Page(f"(file not found: {self.path})")]

        fname = self.path.lower()
        try:
            import PyPDF2  # type: ignore
            pages = []
            with open(self.path, "rb") as fh:
                reader = PyPDF2.PdfReader(fh)
                for p in reader.pages:
                    try:
                        text = p.extract_text() or ""
                    except Exception:
                        text = ""
                    pages.append(text)
            return [Page(p) for p in pages if p.strip()]
        except Exception:
            # fallback to text reading
            try:
                if fname.endswith(".txt") or fname.endswith(".md"):
                    with open(self.path, "r", encoding="utf-8", errors="ignore") as fh:
                        txt = fh.read()
                    return [Page(txt)]
            except Exception:
                pass
            return [Page(f"(PDF/text reading not available for file: {self.path})")]

class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(file_path: str) -> str:
        try:
            loader = PDFLoader(file_path)
            pages = loader.load()
            content = "\n\n".join(getattr(p, "page_content", str(p)) for p in pages)
            return content
        except Exception as e:
            return f"(error reading file: {e})"
