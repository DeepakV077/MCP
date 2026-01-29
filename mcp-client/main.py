from dotenv import load_dotenv
import os
import sys
from langchain_cerebras import ChatCerebras
from mcp import StdioServerParameters as Params
import mcp.client.stdio as stdio
from mcp import ClientSession
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

async def run():
    try:
        #step 1 - file paths
        server_script = os.path.abspath("mcp-server/main.py")
        # Use correct venv path for Windows (venv/Scripts/python.exe) or Unix (venv/bin/python)
        if os.name == 'nt':  # Windows
            python_executable = os.path.abspath("venv/Scripts/python.exe")
        else:  # Unix/Linux/Mac
            python_executable = os.path.abspath("venv/bin/python")

        logger.info(f"Python: {python_executable}")
        logger.info(f"Server: {server_script}")

        #step 2 - initialize the llm
        llm = ChatCerebras(model="gpt-oss-120b")

        #step 3 - launching the parameters
        server_params = Params(
            command=python_executable,
            args=[server_script],
            env=os.environ.copy()
        )
        
        logger.info("Starting MCP server...\n")

        #step 4 - connecting to the server
        async with stdio.stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                logger.info("MCP server connected!\n")

                loop = asyncio.get_event_loop()
                
                while True:
                    user_query = await loop.run_in_executor(None, input, "Ask PDF (or exit): ")
                    if user_query.lower() in ["exit", "quit"]:
                        break

                    try:
                        logger.info(f"Querying: {user_query}")
                        mcp_response = await session.call_tool("ask_pdf", {"q": user_query})
                        
                        # Handle response
                        if hasattr(mcp_response, 'content') and mcp_response.content:
                            context_text = mcp_response.content[0].text if isinstance(mcp_response.content, list) else str(mcp_response.content[0])
                        else:
                            context_text = str(mcp_response)

                        logger.info(f"Got context: {context_text[:100]}...")

                        system_prompt = (
                            "You are an assistant to Ruthran Raghavan, Chief AI Scientist at HERE AND NOW AI. "
                            f"Use this pdf text to answer: {context_text} "
                            "Respond concisely and based on the PDF content."
                        )

                        ai_response = llm.invoke([("system", system_prompt),
                                                 ("human", user_query)])
                        
                        print(f"\nBot: {ai_response.content}\n")
                    
                    except Exception as error:
                        logger.error(f"Tool error: {error}")
                        print(f"Error: {error}\n")
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run())