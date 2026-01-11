#!/bin/bash
echo "Reverting Phase 2: Local Reorganization..."

# Reverse moves for agents-hq
mv ~/Projects/agents-hq/ai-customer-service-agent-google-adk ~/Projects/ 2>/dev/null
mv ~/Projects/agents-hq/claude-on-whatsapp ~/Projects/ 2>/dev/null
mv ~/Projects/agents-hq/elevenlabs-conversational ~/Projects/ 2>/dev/null
mv ~/Projects/agents-hq/geometrik-ai-home-customer-support ~/Projects/ 2>/dev/null
mv ~/Projects/agents-hq/smart-gaming-industry-research-agent ~/Projects/ 2>/dev/null
mv ~/Projects/agents-hq/livekit-google-ads-agent ~/Projects/ 2>/dev/null

# Reverse moves for courses-hq
mv ~/Projects/courses-hq/geometrik-ai-course ~/Projects/ 2>/dev/null

# Reverse moves for labs
mv ~/Projects/labs/GhostType ~/Projects/ 2>/dev/null
mv ~/Projects/labs/csv_llm_processor ~/Projects/ 2>/dev/null
mv ~/Projects/labs/gemini-cli ~/Projects/ 2>/dev/null
mv ~/Projects/labs/object_oriented_agentic_approach ~/Projects/ 2>/dev/null
mv ~/Projects/labs/claude-agents-public-repo ~/Projects/ 2>/dev/null

# Reverse moves for creative-hq
mv ~/Projects/creative-hq/ai-pitch-decks ~/Projects/ 2>/dev/null
mv ~/Projects/creative-hq/superU ~/Projects/ 2>/dev/null
mv ~/Projects/creative-hq/superu-pluto ~/Projects/ 2>/dev/null
mv ~/Projects/creative-hq/videos-hq ~/Projects/ 2>/dev/null

# Reverse moves for personal-hq
mv ~/Projects/personal-hq/blog_local_archive ~/Projects/stablo-astro-blog 2>/dev/null
mv ~/Projects/personal-hq/docs ~/Projects/sharad_docs 2>/dev/null

# Reverse moves for archives/local-old
for dir in ~/Projects/archives/local-old/*; do
    mv "$dir" ~/Projects/ 2>/dev/null
done

echo "Phase 2 rollback complete."

# Reverse Phase 3: iCloud Cleanup
mv ~/Projects/personal-hq/resume "/Users/sharad/Library/Mobile Documents/com~apple~CloudDocs/github/resume.sharadjain" 2>/dev/null
# Note: Deleted items (Bungeetech, chatbot-ui-hosted, etc.) cannot be easily rolled back via script if rm -rf is used.
echo "Phase 3 rollback (resume move) updated."
