from mcp.server.fastmcp import FastMCP
from pypdf import PdfReader
import os
import logging
import sys

# Setup logging to stderr so it doesn't interfere with JSON-RPC
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize server
mcp = FastMCP("Pdf Reader", "1.0")

# Get PDF path - works from any directory
pdf_path = os.path.join(os.path.dirname(__file__), "..", "profile-of-ruthran-raghavan-chief-ai-scientist-here-and-now-ai-202601272359.pdf")

logger.info(f"MCP Server starting... PDF path: {pdf_path}")

@mcp.tool()
def ask_pdf(q: str) -> str:
    """Search PDF for relevant information based on query"""
    try:
        logger.info(f"Query received: {q}")
        
        # Extract all text from PDF
        reader = PdfReader(pdf_path)
        txt = "\n".join(p.extract_text() or "" for p in reader.pages)
        logger.info(f"Extracted {len(txt)} characters from PDF")
        
        # If text is too long, return first 5000 chars
        if len(txt) > 5000:
            result = txt[:5000]
            logger.info(f"Text too long, returning first 5000 chars")
            return result
        
        # Search for relevant lines
        words = [k.lower() for k in q.split() if len(k) > 2]
        if not words:
            logger.info("No search words found")
            return txt[:5000]
            
        matches = [l for l in txt.split("\n") if any(w in l.lower() for w in words)]
        result = "\n".join(matches[:20]) if matches else txt[:5000]
        logger.info(f"Found {len(matches)} matching lines")
        return result
        
    except FileNotFoundError:
        msg = f"PDF file not found at: {pdf_path}"
        logger.error(msg)
        return msg
    except Exception as e:
        msg = f"Error reading PDF: {str(e)}"
        logger.error(msg, exc_info=True)
        return msg

if __name__ == "__main__":
    try:
        logger.info("Starting MCP server")
        mcp.run()
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)