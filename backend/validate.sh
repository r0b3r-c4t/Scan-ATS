#!/bin/bash
# Scan-ATS Backend Validation Script
# Run after making changes to verify everything is working

echo "=========================================="
echo "SCAN-ATS BACKEND VALIDATION"
echo "=========================================="

cd /reps/Scan-ATS/backend

echo ""
echo "1. Testing Evaluation Logic with Real CV Data..."
echo "   Running: python test_evaluation_otilia.py"
echo ""

python test_evaluation_otilia.py

echo ""
echo "=========================================="
echo "2. Testing Skill Matching..."
echo "   Running: python debug_skills.py"  
echo ""

python debug_skills.py

echo ""
echo "=========================================="
echo "VALIDATION COMPLETE"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Start backend: python -m uvicorn app.main:app --reload"
echo "2. Start frontend: cd ../frontend && pnpm dev"
echo "3. Upload a CV at http://localhost:5173/candidates/upload"
echo "4. Verify score appears in CandidateDetail page"
echo "5. Test recalculation endpoint if needed"
echo ""
