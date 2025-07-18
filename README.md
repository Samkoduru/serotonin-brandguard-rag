# BrandGuard RAG Solution

A comprehensive Retrieval-Augmented Generation (RAG) system that solves the core LLM problems identified in the problem statement:

- ✅ **Eliminates instruction forgetting** - Uses external knowledge base instead of relying on context window
- ✅ **Prevents style mixing** - Strict client data isolation via metadata filtering  
- ✅ **Ensures consistent outputs** - Brand-aware prompt engineering with client-specific personas

## 🎯 Problem Solved

The Content Team at Serotonin faces these issues when using LLMs:
- **Losing/forgetting specific instructions over time** → Solved with persistent client profiles and brand guidelines in vector DB
- **Mixing styles/tones from unrelated inputs** → Solved with strict metadata filtering ensuring only client-specific context
- **Combining disparate elements inconsistently** → Solved with structured prompt templates and brand voice enforcement

## 🏗️ Architecture

### Tech Stack (All Free & Local)
- **Embeddings**: `BAAI/bge-small-en-v1.5` (384-dim, fast, accurate)
- **LLM**: `llmware/bling-phi-2-v0` (2B params, RAG-optimized, no hallucinations)
- **Vector DB**: ChromaDB (local, in-memory, metadata filtering)
- **Hardware**: CPU-only (no GPU required)

### Core Components

1. **ClientProfile**: Defines brand voice, tone, lexicon, and forbidden terms
2. **Document**: Client content with metadata for isolation
3. **BrandGuardRAG**: Main orchestrator for the entire workflow

### Workflow

```
User Request → Embed Query → Retrieve Client Docs → Construct Brand Prompt → Generate → Return with Sources
```

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the demonstration
python brandguard_rag_solution.py
```

### Basic Usage

```python
from brandguard_rag_solution import BrandGuardRAG, ClientProfile, Document

# Initialize system
rag = BrandGuardRAG(device='cpu')

# Register a client
profile = ClientProfile(
    client_id='your-client',
    brand_voice='Professional and technical',
    tone='Direct and authoritative',
    lexicon=['technical', 'solution', 'platform'],
    avoid_terms=['amazing', 'revolutionary'],
    deliverable_types=['blog_post', 'product_update']
)
rag.register_client(profile)

# Add client documents
docs = [
    Document(
        content="Your client's brand guidelines...",
        client_id='your-client',
        doc_type='brand_guide',
        doc_id='brand-guide-v1'
    )
]
rag.ingest_documents(docs)

# Generate content
result = rag.generate_content(
    query="Write a product update about our new feature",
    client_id='your-client',
    deliverable_type='product_update'
)

print(result['content'])
print(f"Sources: {result['sources']}")
```

## 🔧 Key Features

### 1. **Strict Client Isolation**
- Metadata filtering ensures Client A's data never contaminates Client B's generation
- Each query only retrieves documents tagged with the specific client_id

### 2. **Brand Voice Enforcement**
- Client profiles define exact tone, voice, required/forbidden terms
- Prompt templates inject brand requirements directly into generation context

### 3. **Source Transparency**
- Every generated piece cites its source documents
- Full traceability for fact-checking and verification

### 4. **Hallucination Prevention**
- Uses BLING model specifically trained for factual, grounded generation
- Content is only generated from provided context, not model's training data

### 5. **Scalable Multi-Tenancy**
- Single vector DB serves multiple clients efficiently
- Easy to add new clients without affecting existing ones

## 📋 Example: Alchemy Client

The demo includes a full example with Serotonin's client Alchemy:

**Client Profile:**
- Voice: Professional, technical, solution-oriented
- Tone: Direct, authoritative, developer-focused  
- Lexicon: EIP-7702, smart contract, gas sponsorship, batch transactions
- Avoid: revolutionary, game-changing, disrupting

**Sample Output:**
```
Query: "Draft a product update about our new EIP-7702 support"

Generated: "Alchemy now supports EIP-7702, enabling developers to sponsor 
gas fees and batch transactions. This implementation allows externally 
owned accounts to act as smart contract wallets for single transactions, 
improving user onboarding while maintaining security..."

Sources: alchemy-eip7702-update, eip-7702-spec
```

## 🎛️ Configuration

### Client Profile Setup
```python
ClientProfile(
    client_id='unique-identifier',
    brand_voice='Describe the overall voice',
    tone='Specific tone attributes', 
    lexicon=['required', 'terms', 'to', 'use'],
    avoid_terms=['terms', 'to', 'avoid'],
    deliverable_types=['supported', 'content', 'types']
)
```

### Generation Parameters
- `max_tokens`: Control output length (default: 300)
- `temperature`: Control creativity (default: 0.3 for consistency)
- `top_k`: Number of context documents to retrieve (default: 3)

## 🚀 Production Deployment

For production use with Serotonin's 300+ clients:

1. **Scale Vector DB**: Use Pinecone or Weaviate for production workloads
2. **Model Serving**: Deploy with vLLM or text-generation-inference
3. **Web Interface**: Add Flask/FastAPI for Content Team UI
4. **Document Pipeline**: Integrate with Google Drive, Notion, or CMS
5. **Monitoring**: Add logging, metrics, and performance tracking

## 🔍 Validation

The system demonstrates successful resolution of the original problems:

1. ✅ **No instruction forgetting** - Brand guidelines persist in vector DB
2. ✅ **No style mixing** - Client isolation prevents contamination  
3. ✅ **Consistent outputs** - Structured prompts enforce brand compliance
4. ✅ **Factual accuracy** - All content grounded in client-specific sources
5. ✅ **Scalable** - Multi-tenant architecture serves multiple clients

## 📈 Next Steps

- **Hybrid Fine-tuning**: For high-value clients, fine-tune models on their specific style
- **Content Evaluation**: Implement LLM-as-judge for automatic quality scoring
- **Feedback Loop**: Collect user ratings to improve retrieval and generation
- **Advanced Chunking**: Implement semantic chunking for better context

---

**Built for Serotonin's Content Team to solve real LLM challenges with practical, production-ready RAG architecture.** 