import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.document.chunking.document import DocumentChunking
from phi.vectordb.pgvector import PgVector
from phi.model.anthropic import Claude
from phi.embedder.openai import OpenAIEmbedder
from phi.model.openai import OpenAIChat
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
knowledge_base.load(recreate=False)  # Set to False after first run

# Create the Component Analyzer agent
analyzer = Agent(
    name="Component Analyzer",
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "1. Analyze UI requirements and break them down into component needs",
        "2. Identify suitable FlyonUI components and their HTML structure",
        "3. Suggest appropriate Tailwind CSS classes for styling and responsiveness",
        "4. Consider accessibility and best practices",
        "5. Provide a clear component architecture plan"
    ],
    show_tool_calls=True,
    read_chat_history=True,
    markdown=True
)

# Create the Code Generator agent
generator = Agent(
    name="Code Generator",
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "1. Generate semantic HTML structure using FlyonUI components",
        "2. Implement responsive layouts with Tailwind CSS utility classes",
        "3. Follow FlyonUI's component patterns and best practices",
        "4. Ensure proper integration between FlyonUI and Tailwind CSS",
        "5. Add detailed comments explaining the implementation",
        "6. Include any required JavaScript interactions",
        "7. Consider browser compatibility and performance"
    ],
    show_tool_calls=True,
    read_chat_history=True,
    markdown=True
)

multi_ai_agent = Agent(
    name="Multi Agent",
    model=OpenAIChat(id="gpt-4o"),
    team=[analyzer, generator],
    instructions=[
        "1. Component Analyzer: Break down UI requirements and plan the component architecture",
        "2. Component Analyzer: Suggest FlyonUI components and their HTML structure",
        "3. Component Analyzer: Recommend Tailwind CSS classes for styling",
        "4. Code Generator: Implement the complete solution with FlyonUI + HTML + Tailwind CSS",
        "5. Code Generator: Add necessary JavaScript interactions and ensure responsiveness",
        "6. Both agents should focus on modern UI/UX practices and performance",
    ],
    show_tool_calls=True,
    markdown=True,
)

multi_ai_agent.print_response("create a responsive navigation bar with a logo, menu items, and a user profile dropdown", stream=True)