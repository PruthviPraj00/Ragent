import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.document.chunking.document import DocumentChunking
from phi.vectordb.pgvector import PgVector
from phi.model.anthropic import Claude
from phi.embedder.openai import OpenAIEmbedder
from phi.tools.firecrawl import FirecrawlTools

# Load environment variables for API keys
load_dotenv()

# Database configuration
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Initialize PgVector for storage
vector_db = PgVector(
    table_name="flyonui_docs",
    db_url=db_url,
    embedder=OpenAIEmbedder(),
)

# Initialize FirecrawlTools
firecrawl = FirecrawlTools(
    scrape=False,
    crawl=True
)

# Create knowledge base with crawling capability
knowledge_base = WebsiteKnowledgeBase(
    urls=["https://flyonui.com/"],
    vector_db=vector_db,
    chunking_strategy=DocumentChunking(),
    tools=[firecrawl]  # Add Firecrawl tool to knowledge base
)

# Load or create the knowledge base
knowledge_base.load(recreate=True)  # Set to False after first run

# Create the Component Analyzer agent
analyzer = Agent(
    name="Component Analyzer",
    model=Claude(id="claude-3-5-sonnet-20240620"),
    knowledge=knowledge_base,
    search_knowledge=True,
    system_prompt="""You are an expert UI Component Analyzer specializing in FlyonUI.
    Your role is to analyze requirements and suggest appropriate components.
    
    For each requirement:
    1. Identify the key UI elements needed
    2. Suggest specific FlyonUI components that best match the requirements
    3. Explain why each component is appropriate
    4. Provide component features and customization options
    
    Use the knowledge base to reference FlyonUI documentation.
    Format your response in clear sections with markdown.""",
    show_tool_calls=True,
    read_chat_history=True,
    markdown=True
)

# Create the Code Generator agent
generator = Agent(
    name="Code Generator",
    model=Claude(id="claude-3-5-sonnet-20240620"),
    knowledge=knowledge_base,
    search_knowledge=True,
    system_prompt="""You are an expert Frontend Developer specializing in FlyonUI.
    Your role is to generate implementation code for UI requirements.
    
    For each requirement:
    1. Generate clean, semantic HTML using FlyonUI components
    2. Implement efficient Tailwind CSS styling
    3. Include all necessary classes and attributes
    4. Add comments explaining key parts of the code
    
    Use the knowledge base to reference FlyonUI documentation.
    Always provide complete, working code snippets with explanations.""",
    show_tool_calls=True,
    read_chat_history=True,
    markdown=True
)

if __name__ == "__main__":
    pass 