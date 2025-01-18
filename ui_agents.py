import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.model.anthropic import Claude
from phi.model.openai import OpenAIChat

# Load environment variables for API keys
load_dotenv()

# Database configuration
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Initialize PgVector for storage
vector_db = PgVector(
    table_name="flyonui_docs",
    db_url=db_url,
)

knowledge_base = WebsiteKnowledgeBase(
    urls=["https://flyonui.com/"],
    # Reduce max_links to ensure thorough crawling of main documentation
    max_links=100,
    # Add these parameters to improve crawling
    max_depth=3,
    follow_links_containing=["/docs/", "/components/", "/examples/"],
    ignore_links_containing=["blog", "changelog"],
    vector_db=vector_db 
)
# Force recreate to refresh the knowledge base
knowledge_base.load(recreate=True)  # Set to True for first run to rebuild index


flyon_agent = Agent(
    name="FlyonUI Agent",
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "You are a specialized FlyonUI component generator. Follow these strict guidelines:",
        "1. Output ONLY the specific component code - no full HTML files or surrounding structure",
        "2. Use ONLY components and classes from the FlyonUI knowledge base exactly as documented",
        "3. Maintain component hierarchy and functionality exactly as per FlyonUI documentation",
        "4. Include only the essential imports for the requested component",
        "5. Focus on functional correctness over styling - ensure all interactive features work",
        "6. If a component isn't directly documented, construct it using available basic FlyonUI components",
        "7. Structure must be exact - no compromises on component structure or functionality",
        "8. Keep responses focused on component code only - minimize explanatory text",
        "9. Always provide code using available components, even if the exact pattern isn't documented",
    ],
    show_tool_calls=True,
    markdown=True,
)

flyon_agent.print_response("create a responsive navigation bar with a logo, menu items, and a user profile dropdown", stream=True)

