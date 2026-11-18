import os
import tempfile
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader, PyPDFium2Loader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent

# --- 1. Streamlit Page Configuration ---
st.set_page_config(page_title="Research Assistant Agent", page_icon="🕵️‍♂️", layout="wide")

# Initialize Session State Variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# --- 2. Sidebar for API Keys & File Uploads ---
with st.sidebar:
    st.title("⚙️ Configuration")
    openrouter_api_key = st.text_input("OpenRouter API Key", type="password")
    tavily_api_key = st.text_input("Tavily API Key", type="password")
    
    st.markdown("---")
    st.subheader("📄 Local Document Upload")
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    
    if st.button("Process Document"):
        if not uploaded_file:
            st.warning("Please upload a PDF file first.")
        else:
            with st.spinner("Processing document..."):
                try:
                    # Save the uploaded file to a temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    # Load the PDF with a more robust parser
                    loader = PyPDFium2Loader(tmp_file_path)
                    docs = loader.load()
                    
                    # Ensure metadata is clean
                    for doc in docs:
                        doc.metadata["source"] = uploaded_file.name
                    
                    # Split the document into slightly larger chunks for more context
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
                    splits = text_splitter.split_documents(docs)
                    
                    # Embed and store in Chroma
                    # Using sentence-transformers model via HuggingFaceEmbeddings
                    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                    chroma_dir = tempfile.mkdtemp()
                    
                    vector_store = Chroma.from_documents(
                        documents=splits, 
                        embedding=embeddings, 
                        persist_directory=chroma_dir
                    )
                    
                    # Store vector store in session state
                    st.session_state.vector_store = vector_store
                    st.success("Document processed successfully! Local RAG ready.")
                    
                    # Cleanup temp file
                    os.unlink(tmp_file_path)
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")

# --- 3. Tool Definitions ---
@tool
def local_doc_search(query: str) -> str:
    """Use this tool to search through the user's uploaded local research documents. Input should be a specific search query. Provide distinct keywords or phrased questions."""
    if st.session_state.vector_store is None:
        return "No local document has been uploaded or processed yet. Tell the user to upload a PDF first."
    
    try:
        # Perform similarity search, retrieve more documents (k=6) to ensure higher accuracy
        docs = st.session_state.vector_store.similarity_search(query, k=6)
        if not docs:
            return "No relevant information found in the local document."
        
        # Combine the retrieved content with clear boundaries
        results = "\n\n---\n\n".join([f"Excerpt {i+1} (Page {doc.metadata.get('page', 'Unknown')}):\n{doc.page_content}" for i, doc in enumerate(docs)])
        return results
    except Exception as e:
        return f"Error searching local document: {str(e)}"

@tool
def web_search(query: str) -> str:
    """Use this tool to search the internet for current events, news, or factual information not found in the local documents."""
    # Ensure Tavily API key is available in environment variables
    if not os.environ.get("TAVILY_API_KEY"):
        return "Tavily API Key is not configured. Cannot perform web search."
    
    try:
        tavily_tool = TavilySearchResults(max_results=3)
        return tavily_tool.invoke({"query": query}) # tavily returns list of dicts, which gets casted to str implicitly
    except Exception as e:
        return f"Error executing web search: {str(e)}"

# --- 4. Agent Initialization ---
def get_agent_executor(api_key: str):
    # Initialize the LLM via OpenRouter
    llm = ChatOpenAI(
        model_name="meta-llama/llama-3-8b-instruct",
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.1
    )
    
    tools = [local_doc_search, web_search]
    
    # Bind the LLM and tools to create a LangGraph ReAct agent.
    # The LangGraph implementation handles the prompt internally and returns an executor.
    agent_executor = create_react_agent(llm, tools=tools)
    
    return agent_executor

# --- 5. Main Chat Interface ---
st.title("🕵️‍♂️ Research Assistant Agent")
st.markdown("Ask questions based on your uploaded PDF or search the web for current facts. The agent will reason and decide which tool to use.")

def display_reasoning_trace(steps):
    """Cleanly displays the intermediate steps inside an expander."""
    with st.expander("🔍 View Agent Reasoning Trace"):
        for step in steps:
            # LangGraph intermediate steps format
            if hasattr(step, "action"):
                action = step.action
                observation = step.observation
                
                log = getattr(action, "log", "")
                thought_text = log.split('Action:')[0].replace('Thought:', '').strip() if log else "Using Tool"
                
                st.markdown(f"**Thought:** {thought_text}")
                st.markdown(f"**Tool Invoked:** `{action.tool}`")
                st.markdown(f"**Action Input:** `{action.tool_input}`")
                st.markdown(f"**Observation:**\n```text\n{observation}\n```")
                st.markdown("---")

# Render existing conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "steps" in msg and msg["steps"]:
            display_reasoning_trace(msg["steps"])

# Chat Input
if prompt_text := st.chat_input("Ask a research question..."):
    # Pre-checks
    if not openrouter_api_key:
        st.error("Please provide your OpenRouter API Key in the sidebar.")
        st.stop()
        
    if tavily_api_key:
        os.environ["TAVILY_API_KEY"] = tavily_api_key
        
    # 1. Add and display user message
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
        st.markdown(prompt_text)
        
    # 2. Add and process assistant message
    with st.chat_message("assistant"):
        with st.spinner("Agent is reasoning..."):
            try:
                executor = get_agent_executor(openrouter_api_key)
                
                # Run the agent using the v2 API format
                # LangGraph agents expect messages format instead of dict
                from langchain_core.messages import HumanMessage
                
                # Fetch stream to get intermediate steps
                inputs = {"messages": [HumanMessage(content=prompt_text)]}
                
                intermediate_steps = []
                final_answer = "No response generated."
                
                # Stream gives you each event including tool calls and LLM steps
                for event in executor.stream(inputs, stream_mode="values"):
                    message = event["messages"][-1]
                    if message.type == "ai" and message.tool_calls:
                        for tool_call in message.tool_calls:
                            # In LangGraph we manually construct an observation payload for the UI
                            # Since the actual observation returns in a subsequent message
                            intermediate_steps.append({
                                "tool": tool_call["name"],
                                "tool_input": tool_call["args"],
                                "log": "Deciding to use tool" 
                            })
                    elif message.type == "tool":
                        # The tool output matches the last tool log we saved
                        if intermediate_steps:
                            intermediate_steps[-1]["observation"] = message.content
                    elif message.type == "ai" and not message.tool_calls:
                        final_answer = message.content
                
                # Render reasoning trace dynamically
                if intermediate_steps:
                    with st.expander("🔍 View Agent Reasoning Trace"):
                        for step in intermediate_steps:
                            st.markdown(f"**Thought:** {step.get('log', '')}")
                            st.markdown(f"**Tool Invoked:** `{step.get('tool', '')}`")
                            st.markdown(f"**Action Input:** `{step.get('tool_input', '')}`")
                            st.markdown(f"**Observation:**\n```text\n{step.get('observation', 'Pending...')}\n```")
                            st.markdown("---")
                    
                # Render Final Answer
                st.markdown(final_answer)
                
                # Save to session state
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_answer,
                    "steps": intermediate_steps
                })
                
            except Exception as e:
                error_msg = f"An error occurred during execution: {str(e)}"
                st.error(error_msg)
