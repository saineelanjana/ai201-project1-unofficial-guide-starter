#!/usr/bin/env bash
# QUICK START GUIDE - OMSCS RAG System

echo "
╔════════════════════════════════════════════════════════════════════════════╗
║              OMSCS RAG System - Generation Layer Quick Start                ║
╚════════════════════════════════════════════════════════════════════════════╝
"

# Check 1: Python & venv
echo "✅ Checking environment..."
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 not installed"
    exit 1
fi

# Check 2: Dependencies
echo "✅ Installing dependencies..."
pip install -q -r requirements.txt

# Check 3: Check GROQ_API_KEY
echo "✅ Checking GROQ_API_KEY..."
if [ -z "$GROQ_API_KEY" ] && ! grep -q "GROQ_API_KEY" .env 2>/dev/null; then
    echo ""
    echo "⚠️  GROQ_API_KEY not found!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Get a free Groq API key:"
    echo "  1. Visit: https://console.groq.com/keys"
    echo "  2. Copy your API key"
    echo "  3. Create/update .env file:"
    echo ""
    echo "     echo 'GROQ_API_KEY=your_key_here' > .env"
    echo ""
    echo "Or set it in your shell:"
    echo "     export GROQ_API_KEY=your_key_here"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 1
fi

echo "✅ GROQ_API_KEY configured"
echo ""

# Check 4: Vector store
echo "✅ Checking vector store..."
if [ ! -d "chromadb" ] || [ -z "$(ls -A chromadb 2>/dev/null)" ]; then
    echo "   Building ChromaDB vector store (this takes ~1 minute)..."
    python3 -c "
from vector_store import VectorStore
store = VectorStore()
store.build(force=True, batch_size=64)
print('   ✅ Vector store built with 916 chunks')
"
else
    echo "   ✅ Vector store already exists"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 QUICK START OPTIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Option 1: Run End-to-End Tests"
echo "   Command: python3 end_to_end_test.py"
echo "   Tests:   • Grounding enforcement"
echo "            • Source attribution"
echo "            • Retrieval logging"
echo "            • Out-of-domain queries"
echo ""

echo "Option 2: Run CLI Query Tool"
echo "   Command: python3 query.py"
echo "   Tests grounding on 3 queries (interactive)"
echo ""

echo "Option 3: Launch Gradio Web Interface"
echo "   Command: python3 app.py"
echo "   Access:  http://localhost:7860"
echo "   Features:"
echo "            • Web UI for asking questions"
echo "            • Source attribution display"
echo "            • Retrieved context preview"
echo ""

echo "Option 4: Manual Query"
echo "   python3 -c \""
echo "from query import ask"
echo "result = ask('What is GIOS and how demanding is it?')"
echo "print(result['answer'])"
echo "print('Sources:', result['sources'])"
echo "   \""
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📖 For detailed documentation, see: GENERATION_GUIDE.md"
echo ""

