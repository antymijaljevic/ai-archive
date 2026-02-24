#!/bin/bash

# Quick Start Script for Claude Code Project Template
# This script helps you set up a new project from this template

set -e  # Exit on error

echo "🤖 Claude Code Project Template - Quick Start"
echo "=============================================="
echo ""

# Get project name
read -p "Enter your project name: " PROJECT_NAME

if [ -z "$PROJECT_NAME" ]; then
  echo "❌ Project name cannot be empty"
  exit 1
fi

# Get project path
read -p "Where to create project? (default: ../): " PROJECT_PATH
PROJECT_PATH=${PROJECT_PATH:-"../"}

# Full path
FULL_PATH="$PROJECT_PATH/$PROJECT_NAME"

# Check if directory exists
if [ -d "$FULL_PATH" ]; then
  echo "❌ Directory already exists: $FULL_PATH"
  exit 1
fi

echo ""
echo "📁 Creating project at: $FULL_PATH"

# Copy template
cp -r "$(dirname "$0")" "$FULL_PATH"

# Remove template-specific files
cd "$FULL_PATH"
rm -f quick-start.sh
rm -f SETUP.md

echo "✅ Template copied"

# Initialize git
echo ""
read -p "Initialize git repository? (y/n): " INIT_GIT
if [[ "$INIT_GIT" =~ ^[Yy]$ ]]; then
  git init
  git add .
  git commit -m "Initial commit with Claude Code configuration"
  echo "✅ Git initialized"
fi

# Create .env from example
if [ -f ".env.example" ]; then
  cp .env.example .env
  echo "✅ Created .env from .env.example"
fi

# Make hooks executable
chmod +x .claude/hooks/*.sh
echo "✅ Made hooks executable"

echo ""
echo "🎉 Project created successfully!"
echo ""
echo "Next steps:"
echo "  1. cd $FULL_PATH"
echo "  2. Edit CLAUDE.md with your project information"
echo "  3. Edit .env with your environment variables"
echo "  4. Customize .claude/settings.json permissions"
echo "  5. Run: claude"
echo ""
echo "📚 Read README.md for complete documentation"
echo "🔧 Read STRUCTURE.md to understand the file layout"
echo ""
echo "Happy coding with Claude! 🚀"
