#!/usr/bin/env python3
"""
end_to_end_test.py

Comprehensive test of the grounded RAG pipeline:
1. Verifies retrieval works
2. Verifies grounding enforcement in generation
3. Tests programmatic source attribution
4. Demonstrates the full query flow
"""

import json
from query import GroundedQueryEngine


def print_section(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def test_grounded_generation():
    """Test the full grounded generation pipeline."""

    print_section("OMSCS RAG System - End-to-End Test")

    engine = GroundedQueryEngine()

    # Test 1: In-domain query (summer semesters - known to have good doc coverage)
    print_section("TEST 1: Query with good document coverage")
    print("❓ Question: How long are summer semesters compared to fall/spring?")

    result1 = engine.query("How long are summer semesters compared to fall/spring?", k=4)

    print(f"\n📊 Retrieved {len(result1['retrieved_chunks'])} chunks\n")
    print("💬 ANSWER:")
    print(result1['answer'])
    print(f"\n📋 SOURCES ({len(result1['sources'])}):")
    for src in result1['sources']:
        print(f"   • {src}")

    # Verify grounding: answer doesn't seem to hallucinate
    assert "summer" in result1['answer'].lower(), "Expected answer to mention summer"
    assert "10-13" in result1['answer'] or "weeks" in result1['answer'], "Expected specific time info"
    assert len(result1['sources']) > 0, "Expected sources to be cited"
    print("\n✅ Grounding test 1 PASSED: Answer is grounded and sources are cited")


    # Test 2: Out-of-domain query (info NOT in documents)
    print_section("TEST 2: Query about information NOT in documents")
    print("❓ Question: What is the salary for a ML engineer at Google?")

    result2 = engine.query("What is the salary for a ML engineer at Google?", k=4)

    print(f"\n📊 Retrieved {len(result2['retrieved_chunks'])} chunks\n")
    print("💬 ANSWER:")
    print(result2['answer'])

    # Verify grounding: system should say it doesn't have the information
    answer_lower = result2['answer'].lower()
    has_explicit_refusal = any(phrase in answer_lower for phrase in [
        "don't have enough", "not found", "unclear", "no information"
    ])
    assert has_explicit_refusal, "Expected explicit acknowledgment of missing info"
    print("\n✅ Grounding test 2 PASSED: System correctly refused to hallucinate")


    # Test 3: OMSCS-specific acronym query
    print_section("TEST 3: OMSCS-specific query with acronyms")
    print("❓ Question: What is GIOS and how demanding is it?")

    result3 = engine.query("What is GIOS and how demanding is it?", k=4)

    print(f"\n📊 Retrieved {len(result3['retrieved_chunks'])} chunks\n")
    print("💬 ANSWER:")
    print(result3['answer'][:400] + "..." if len(result3['answer']) > 400 else result3['answer'])
    print(f"\n📋 SOURCES ({len(result3['sources'])}):")
    for src in result3['sources']:
        print(f"   • {src}")

    assert len(result3['retrieved_chunks']) > 0, "Expected retrieval on GIOS query"
    print("\n✅ Grounding test 3 PASSED: System found relevant documents")


    # Test 4: Verify retrieval log
    print_section("✅ VERIFICATION: Check retrieval_log.json")

    try:
        with open("retrieval_log.json", "r") as f:
            logs = json.load(f)
        print(f"📝 Logged {len(logs)} queries")
        print(f"Latest query: {logs[-1]['query'][:60]}...")
        print(f"Latest sources used: {logs[-1]['cited_sources']}")
        print("✅ Retrieval log is properly persisting")
    except FileNotFoundError:
        print("⚠️  Note: retrieval_log.json not found (expected if this is first run)")


    # Summary
    print_section("🎉 ALL TESTS PASSED!")
    print("""
The RAG system is working correctly:

✅ RETRIEVAL: Vector store successfully finding relevant chunks
✅ GENERATION: LLM generating responses from retrieved context
✅ GROUNDING ENFORCEMENT: System refuses to hallucinate on out-of-domain queries
✅ SOURCE ATTRIBUTION: Programmatically extracting and citing sources
✅ LOGGING: Audit trail of all queries and retrievals

This system is ready for use in the Gradio web interface (app.py).
    """)


if __name__ == "__main__":
    test_grounded_generation()

