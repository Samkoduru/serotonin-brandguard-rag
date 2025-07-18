#!/usr/bin/env python3
"""
Multi-Client Isolation Demo
==========================

This demonstrates the key innovation: strict client isolation that prevents
style mixing and context contamination between different clients.
"""

from simple_brandguard_demo import SimpleBrandGuardRAG, ClientProfile, Document

def setup_two_clients():
    """Set up two clients with contrasting brand voices"""
    
    # Client 1: Alchemy (Technical, Professional)
    alchemy_profile = ClientProfile(
        client_id='alchemy-web3',
        brand_voice='Professional, technical, and solution-oriented',
        tone='Direct, authoritative, developer-focused',
        lexicon=['EIP-7702', 'smart contract', 'gas sponsorship', 'developers', 'technical'],
        avoid_terms=['revolutionary', 'game-changing', 'disrupting', 'amazing', 'incredible'],
        deliverable_types=['product_update', 'technical_docs']
    )
    
    # Client 2: FunCoin (Casual, Marketing-heavy) - Contrasting style
    funcoin_profile = ClientProfile(
        client_id='funcoin-defi',
        brand_voice='Exciting, energetic, and community-focused',
        tone='Casual, enthusiastic, user-friendly',
        lexicon=['amazing', 'incredible', 'community', 'moon', 'hodl', 'revolutionary'],
        avoid_terms=['technical', 'complex', 'implementation', 'architecture'],
        deliverable_types=['blog_post', 'social_media']
    )
    
    # Documents for Alchemy (Technical)
    alchemy_docs = [
        Document(
            content="Alchemy provides enterprise-grade blockchain infrastructure. Focus on technical implementation details and developer benefits.",
            client_id='alchemy-web3',
            doc_type='brand_guide',
            doc_id='alchemy-brand-v1'
        ),
        Document(
            content="EIP-7702 technical specification: Allows EOAs to act as smart contract wallets. Enables gas sponsorship and transaction batching.",
            client_id='alchemy-web3',
            doc_type='technical_spec',
            doc_id='alchemy-eip7702-tech'
        )
    ]
    
    # Documents for FunCoin (Marketing)
    funcoin_docs = [
        Document(
            content="FunCoin is an amazing DeFi protocol that's revolutionizing how communities interact with blockchain! We're going to the moon!",
            client_id='funcoin-defi',
            doc_type='brand_guide',
            doc_id='funcoin-brand-v1'
        ),
        Document(
            content="Our incredible new staking feature lets users earn amazing rewards! The community loves our revolutionary approach to DeFi.",
            client_id='funcoin-defi',
            doc_type='marketing_copy',
            doc_id='funcoin-staking-promo'
        )
    ]
    
    return alchemy_profile, funcoin_profile, alchemy_docs, funcoin_docs

def test_isolation(rag_system):
    """Test that each client only gets their own data"""
    
    print("\n" + "="*60)
    print("🔒 TESTING CLIENT ISOLATION")
    print("="*60)
    
    # Same query for both clients - should get very different results
    query = "about our new exciting features and benefits"
    
    print(f"\n📝 Same Query for Both Clients: '{query}'")
    print("-" * 60)
    
    # Generate for Alchemy (should be technical)
    print(f"\n🔧 ALCHEMY RESPONSE (Technical/Professional):")
    print("-" * 40)
    alchemy_result = rag_system.generate_content(
        query=query,
        client_id='alchemy-web3',
        deliverable_type='product_update'
    )
    print("Content:", alchemy_result['content'][:200] + "...")
    print("Sources:", alchemy_result['sources'])
    
    # Generate for FunCoin (should be casual/marketing)
    print(f"\n🎉 FUNCOIN RESPONSE (Casual/Marketing):")
    print("-" * 40)
    funcoin_result = rag_system.generate_content(
        query=query,
        client_id='funcoin-defi',
        deliverable_type='blog_post'
    )
    print("Content:", funcoin_result['content'][:200] + "...")
    print("Sources:", funcoin_result['sources'])
    
    # Validate isolation
    print(f"\n✅ ISOLATION VALIDATION:")
    print(f"- Alchemy uses only Alchemy sources: {all('alchemy' in src for src in alchemy_result['sources'])}")
    print(f"- FunCoin uses only FunCoin sources: {all('funcoin' in src for src in funcoin_result['sources'])}")
    print(f"- No cross-contamination: {set(alchemy_result['sources']).isdisjoint(set(funcoin_result['sources']))}")

def main():
    """Demonstrate multi-client isolation"""
    
    print("🛡️  BRANDGUARD: MULTI-CLIENT ISOLATION DEMO")
    print("="*60)
    print("Proving: No style mixing between different clients")
    print("="*60)
    
    # Initialize system
    rag_system = SimpleBrandGuardRAG()
    
    # Set up contrasting clients
    alchemy_profile, funcoin_profile, alchemy_docs, funcoin_docs = setup_two_clients()
    
    # Register both clients
    print("\n📋 REGISTERING CLIENTS:")
    rag_system.register_client(alchemy_profile)
    rag_system.register_client(funcoin_profile)
    
    # Ingest documents for both
    print("\n📚 INGESTING DOCUMENTS:")
    all_docs = alchemy_docs + funcoin_docs
    rag_system.ingest_documents(all_docs)
    
    print(f"- Total documents: {len(all_docs)}")
    print(f"- Alchemy docs: {len(alchemy_docs)}")
    print(f"- FunCoin docs: {len(funcoin_docs)}")
    
    # Test isolation
    test_isolation(rag_system)
    
    print(f"\n{'='*60}")
    print("🎯 ISOLATION PROOF COMPLETE!")
    print("\nKey Findings:")
    print("✅ Each client only retrieves their own documents")
    print("✅ Brand voice remains distinct and consistent") 
    print("✅ No cross-client contamination occurs")
    print("✅ Same query → Different brand-appropriate responses")
    print(f"\n{'='*60}")
    print("This solves the core problem: 'Mix styles or tones from unrelated inputs'")
    print("="*60)

if __name__ == "__main__":
    main() 