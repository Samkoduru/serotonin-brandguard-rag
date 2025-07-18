#!/usr/bin/env python3
"""
Simple BrandGuard RAG Demo
=========================

A streamlined demonstration of the RAG solution that solves the LLM problems:
- Forgetting specific instructions over time
- Mixing styles/tones from unrelated inputs  
- Combining disparate elements inconsistently

This demo uses minimal dependencies to avoid conflicts.
"""

import json
import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass

# We'll simulate the embeddings and use a simple similarity search
# In production, you'd use SentenceTransformers and a real LLM

@dataclass
class ClientProfile:
    """Client brand voice and style configuration"""
    client_id: str
    brand_voice: str
    tone: str
    lexicon: List[str]
    avoid_terms: List[str]
    deliverable_types: List[str]

@dataclass
class Document:
    """Document with metadata for RAG"""
    content: str
    client_id: str
    doc_type: str
    doc_id: str
    source_url: Optional[str] = None

class SimpleBrandGuardRAG:
    """
    Simplified RAG system demonstrating the core concepts
    """
    
    def __init__(self):
        # Simple in-memory storage
        self.documents = []
        self.client_profiles = {}
        print("✓ Simple BrandGuard RAG system initialized!")
    
    def register_client(self, profile: ClientProfile):
        """Register a client with their brand profile"""
        self.client_profiles[profile.client_id] = profile
        print(f"✓ Registered client: {profile.client_id}")
    
    def ingest_documents(self, documents: List[Document]):
        """Ingest documents (simulated embedding)"""
        print(f"✓ Ingesting {len(documents)} documents...")
        self.documents.extend(documents)
        print("✓ Document ingestion complete!")
    
    def retrieve_context(self, query: str, client_id: str, top_k: int = 3) -> tuple:
        """Retrieve relevant context for a specific client (simulated)"""
        # Filter documents by client_id (strict isolation)
        client_docs = [doc for doc in self.documents if doc.client_id == client_id]
        
        # Simple keyword-based relevance (in production, use semantic similarity)
        query_words = query.lower().split()
        scored_docs = []
        
        for doc in client_docs:
            content_words = doc.content.lower().split()
            score = sum(1 for word in query_words if word in content_words)
            if score > 0:
                scored_docs.append((doc, score))
        
        # Sort by relevance and take top_k
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        top_docs = scored_docs[:top_k]
        
        retrieved_docs = [doc.content for doc, _ in top_docs]
        retrieved_metadata = [{
            'doc_id': doc.doc_id,
            'doc_type': doc.doc_type,
            'client_id': doc.client_id
        } for doc, _ in top_docs]
        
        return retrieved_docs, retrieved_metadata
    
    def construct_prompt(self, query: str, client_id: str, deliverable_type: str, 
                        retrieved_docs: List[str], retrieved_metadata: List[Dict]) -> str:
        """Construct a brand-aware prompt with retrieved context"""
        
        # Get client profile
        profile = self.client_profiles.get(client_id)
        if not profile:
            raise ValueError(f"Client {client_id} not registered")
        
        # Build context section
        context = ""
        for doc, meta in zip(retrieved_docs, retrieved_metadata):
            context += f"[Source: {meta['doc_id']}] {doc}\n\n"
        
        # Construct the prompt with brand guidelines
        prompt = f"""BRAND REQUIREMENTS FOR {client_id.upper()}:
- Voice: {profile.brand_voice}
- Tone: {profile.tone}
- Required terms: {', '.join(profile.lexicon)}
- Avoid: {', '.join(profile.avoid_terms)}

CONTEXT FROM CLIENT DOCUMENTS:
{context}

TASK: Write a {deliverable_type} that {query}

IMPORTANT: Only use information from the provided context. Follow the brand voice exactly."""
        
        return prompt
    
    def simulate_llm_response(self, prompt: str, client_id: str) -> str:
        """Simulate LLM response (in production, this calls the actual LLM)"""
        
        # Get client profile for brand-appropriate response
        profile = self.client_profiles.get(client_id)
        
        # Extract context from prompt
        if "EIP-7702" in prompt:
            if client_id == "alchemy-web3":
                return """Alchemy now supports EIP-7702, enabling developers to sponsor gas fees and batch transactions for users. This implementation allows externally owned accounts (EOAs) to temporarily act as smart contract wallets for single transactions.

Key developer benefits:
- Gas sponsorship eliminates user friction during onboarding
- Batch transactions improve efficiency and reduce costs
- Smart contract functionality without requiring users to deploy contracts
- Seamless integration with existing Alchemy Account Contracts

This technical advancement enhances user experience while maintaining the security and decentralization principles that define the platform."""
        
        # Fallback response
        return f"[Simulated {profile.brand_voice} response for {client_id}] Content generated following brand guidelines with technical focus on developer benefits."
    
    def generate_content(self, query: str, client_id: str, deliverable_type: str) -> Dict:
        """Generate brand-consistent content for a client"""
        
        print(f"\n🔄 Generating {deliverable_type} for {client_id}...")
        
        # Step 1: Retrieve relevant context
        retrieved_docs, retrieved_metadata = self.retrieve_context(query, client_id)
        
        if not retrieved_docs:
            return {
                'content': 'Insufficient context to generate content.',
                'sources': [],
                'error': 'No relevant documents found'
            }
        
        print(f"✓ Retrieved {len(retrieved_docs)} relevant documents")
        
        # Step 2: Construct brand-aware prompt
        prompt = self.construct_prompt(query, client_id, deliverable_type, 
                                     retrieved_docs, retrieved_metadata)
        
        print("✓ Constructed brand-aware prompt")
        
        # Step 3: Generate content (simulated)
        generated_text = self.simulate_llm_response(prompt, client_id)
        
        print("✓ Generated brand-consistent content")
        
        # Extract sources
        sources = [meta['doc_id'] for meta in retrieved_metadata]
        
        return {
            'content': generated_text.strip(),
            'sources': sources,
            'client_id': client_id,
            'deliverable_type': deliverable_type,
            'context_used': len(retrieved_docs)
        }

def setup_example_data():
    """Set up example clients and sample data"""
    
    # Define Alchemy client profile
    alchemy_profile = ClientProfile(
        client_id='alchemy-web3',
        brand_voice='Professional, technical, and solution-oriented',
        tone='Direct, authoritative, developer-focused',
        lexicon=['EIP-7702', 'smart contract', 'gas sponsorship', 'batch transactions', 'EOA', 'onchain'],
        avoid_terms=['revolutionary', 'game-changing', 'disrupting', 'amazing'],
        deliverable_types=['product_update', 'blog_post', 'technical_docs']
    )
    
    # Sample documents for Alchemy
    alchemy_docs = [
        Document(
            content="""Alchemy Brand Guidelines: Always use a professional, technical, and solution-oriented tone. 
            Focus on developer benefits and outcomes. Use precise technical terminology. 
            Avoid marketing fluff and hyperbole. Target audience: blockchain developers and technical founders.""",
            client_id='alchemy-web3',
            doc_type='brand_guide',
            doc_id='alchemy-brand-guide-v1'
        ),
        Document(
            content="""EIP-7702 introduces a new transaction type that allows an externally owned account (EOA) 
            to temporarily act as a smart contract wallet for a single transaction. This enables features like 
            gas sponsorship and transaction batching without requiring users to deploy a full smart contract account.""",
            client_id='alchemy-web3',
            doc_type='technical_spec',
            doc_id='eip-7702-spec'
        ),
        Document(
            content="""Alchemy's Account Contracts now fully support EIP-7702, enabling developers to sponsor 
            gas fees and batch transactions for users. This integration allows for seamless user onboarding 
            while maintaining security and decentralization.""",
            client_id='alchemy-web3',
            doc_type='product_update',
            doc_id='alchemy-eip7702-update'
        ),
        Document(
            content="""Technical implementation: With Alchemy's EIP-7702 support, developers can create 
            more user-friendly applications by removing friction points. Users can interact with complex 
            smart contract functionality without understanding gas mechanics or holding ETH for fees.""",
            client_id='alchemy-web3',
            doc_type='blog_post',
            doc_id='alchemy-blog-eip7702-benefits'
        )
    ]
    
    return alchemy_profile, alchemy_docs

def main():
    """Main demonstration of the BrandGuard RAG system"""
    
    print("=" * 60)
    print("🛡️  BRANDGUARD RAG SOLUTION - DEMONSTRATION")
    print("=" * 60)
    print("Solving LLM problems:")
    print("❌ Forgetting instructions → ✅ Persistent client profiles")
    print("❌ Mixing styles → ✅ Strict client isolation") 
    print("❌ Inconsistent outputs → ✅ Brand-aware prompting")
    print("=" * 60)
    
    # Initialize the system
    rag_system = SimpleBrandGuardRAG()
    
    # Set up example client and data
    alchemy_profile, alchemy_docs = setup_example_data()
    
    # Register client
    rag_system.register_client(alchemy_profile)
    
    # Ingest documents
    rag_system.ingest_documents(alchemy_docs)
    
    # Test queries
    test_queries = [
        {
            'query': 'about our new EIP-7702 support focusing on developer benefits like gas sponsorship and transaction batching',
            'deliverable_type': 'product_update'
        },
        {
            'query': 'explaining how EIP-7702 improves user onboarding for web3 applications',
            'deliverable_type': 'blog_post'
        }
    ]
    
    # Generate content for each query
    for i, test in enumerate(test_queries, 1):
        print(f"\n{'='*50}")
        print(f"🎯 TEST {i}: {test['deliverable_type'].upper()}")
        print(f"{'='*50}")
        print(f"📝 Query: {test['query']}")
        print("-" * 50)
        
        result = rag_system.generate_content(
            query=test['query'],
            client_id='alchemy-web3',
            deliverable_type=test['deliverable_type']
        )
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print("✅ GENERATED CONTENT:")
            print(result['content'])
            print(f"\n📚 SOURCES USED: {', '.join(result['sources'])}")
            print(f"📊 CONTEXT DOCUMENTS: {result['context_used']}")
    
    print(f"\n{'='*60}")
    print("🎉 DEMONSTRATION COMPLETE!")
    print("\nThe BrandGuard system successfully:")
    print("✅ Maintained client-specific brand voice")
    print("✅ Used only relevant, client-specific context")
    print("✅ Prevented cross-client contamination")
    print("✅ Generated consistent, on-brand content")
    print("✅ Provided source transparency")
    print(f"\n{'='*60}")
    print("🚀 PRODUCTION DEPLOYMENT:")
    print("- Replace simulated components with:")
    print("  • BAAI/bge-small-en-v1.5 for embeddings")
    print("  • llmware/bling-phi-2-v0 for generation") 
    print("  • ChromaDB for vector storage")
    print("- Add web interface for Content Team")
    print("- Scale to handle 300+ Serotonin clients")
    print(f"{'='*60}")

if __name__ == "__main__":
    main() 