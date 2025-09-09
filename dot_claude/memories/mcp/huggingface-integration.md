# Hugging Face MCP Integration

## Overview
Hugging Face MCP server provides access to the Hugging Face Hub ecosystem including models, datasets, spaces, papers, and documentation through the Model Context Protocol.

## Installation

### Standard Installation with Authentication
```bash
# Install Hugging Face MCP server with Bearer token authentication
claude mcp add hf-mcp-server -t http "https://huggingface.co/mcp" \
  -H "Authorization:Bearer $(op read 'op://Private/huggingface-token/credential')"

# Verify installation
claude mcp list
# Should show: hf-mcp-server: ✓ Connected (https://huggingface.co/mcp)
```

### Authentication Setup
```bash
# Create Hugging Face token (if not exists)
# 1. Go to https://huggingface.co/settings/tokens
# 2. Create token with appropriate permissions
# 3. Store in 1Password:
op item create --category="API Credential" \
  --title="huggingface-token" \
  credential="hf_your_token_here"

# Test authentication
mcp__hf-mcp-server__hf_whoami
# Should return your Hugging Face username and profile info
```

### Token Permissions
Recommended Hugging Face token scopes:
- **Read access** - Browse public models, datasets, spaces
- **Write access** - Upload models, create datasets (if needed)
- **Inference access** - Use inference endpoints (if needed)

## Core Functionality

### Model Discovery and Analysis
```bash
# Search for models
mcp__hf-mcp-server__model_search --query "text generation" --limit 10
mcp__hf-mcp-server__model_search --author "openai" --task "text-generation"
mcp__hf-mcp-server__model_search --library "transformers" --sort "downloads"

# Get trending models
mcp__hf-mcp-server__model_search --sort "trendingScore" --limit 20

# Get model details
mcp__hf-mcp-server__model_details --model_id "microsoft/DialoGPT-large"
mcp__hf-mcp-server__model_details --model_id "meta-llama/Llama-2-7b-chat-hf"

# Search by specific criteria
mcp__hf-mcp-server__model_search --query "coding" --task "text-generation"
mcp__hf-mcp-server__model_search --query "image classification" --library "timm"
```

### Dataset Discovery and Research
```bash
# Search datasets
mcp__hf-mcp-server__dataset_search --query "natural language processing"
mcp__hf-mcp-server__dataset_search --author "google" --limit 15
mcp__hf-mcp-server__dataset_search --tags "['language:en', 'size_categories:1M<n<10M']"

# Get trending datasets
mcp__hf-mcp-server__dataset_search --sort "trendingScore" --limit 10

# Get dataset details
mcp__hf-mcp-server__dataset_details --dataset_id "squad"
mcp__hf-mcp-server__dataset_details --dataset_id "glue"

# Search for specific data types
mcp__hf-mcp-server__dataset_search --query "conversation" --tags "['task_categories:conversational']"
mcp__hf-mcp-server__dataset_search --query "code" --tags "['language:en', 'task_categories:text-generation']"
```

### Academic Research and Papers
```bash
# Search research papers
mcp__hf-mcp-server__paper_search --query "transformer architecture"
mcp__hf-mcp-server__paper_search --query "large language models" --results_limit 15

# Focused research queries
mcp__hf-mcp-server__paper_search --query "retrieval augmented generation"
mcp__hf-mcp-server__paper_search --query "multimodal learning" --concise_only true

# Recent developments
mcp__hf-mcp-server__paper_search --query "2024 llm improvements"
mcp__hf-mcp-server__paper_search --query "efficient attention mechanisms"
```

### Spaces and Applications
```bash
# Search Spaces (interactive demos)
mcp__hf-mcp-server__space_search --query "text to image" --limit 10
mcp__hf-mcp-server__space_search --query "chatbot" --mcp false

# Find MCP-enabled Spaces
mcp__hf-mcp-server__space_search --query "api" --mcp true

# Discover new applications
mcp__hf-mcp-server__space_search --query "gradio demo"
mcp__hf-mcp-server__space_search --query "streamlit app"
```

### Documentation and Learning
```bash
# Search Hugging Face documentation
mcp__hf-mcp-server__hf_doc_search --query "fine-tuning transformers"
mcp__hf-mcp-server__hf_doc_search --query "pipeline usage" --product "transformers"

# Product-specific documentation
mcp__hf-mcp-server__hf_doc_search --query "dataset loading" --product "datasets"
mcp__hf-mcp-server__hf_doc_search --query "gradio interface" --product "gradio"
mcp__hf-mcp-server__hf_doc_search --query "inference endpoints" --product "hub"
```

## Research and Development Workflows

### Model Selection Process
```bash
# Research workflow for choosing models
# 1. Define requirements
task="text-generation"
use_case="code completion"

# 2. Search relevant models
mcp__hf-mcp-server__model_search --query "$use_case" --task "$task" --limit 20

# 3. Sort by performance metrics
mcp__hf-mcp-server__model_search --query "$use_case" --sort "downloads" --limit 10
mcp__hf-mcp-server__model_search --query "$use_case" --sort "likes" --limit 10

# 4. Get detailed analysis of top candidates
mcp__hf-mcp-server__model_details --model_id "codellama/CodeLlama-7b-Python-hf"
mcp__hf-mcp-server__model_details --model_id "WizardLM/WizardCoder-Python-7B-V1.0"

# 5. Compare model characteristics
# - Model size and compute requirements
# - License compatibility
# - Performance benchmarks
# - Community adoption (downloads, likes)
```

### Dataset Research Pipeline
```bash
# Dataset discovery for training/fine-tuning
# 1. Define data requirements
domain="programming"
language="python"
size_range="10K<n<100K"

# 2. Search relevant datasets
mcp__hf-mcp-server__dataset_search --query "$domain" --tags "['language:en']"

# 3. Filter by characteristics
mcp__hf-mcp-server__dataset_search --query "$domain $language" \
  --tags "['size_categories:$size_range', 'task_categories:text-generation']"

# 4. Analyze dataset details
mcp__hf-mcp-server__dataset_details --dataset_id "codeparrot/github-code"
mcp__hf-mcp-server__dataset_details --dataset_id "bigcode/the-stack"

# 5. Review data quality and licensing
# - Data format and structure
# - License terms
# - Data quality indicators
# - Preprocessing requirements
```

### Literature Review Automation
```bash
# Academic research support
# 1. Initial topic exploration
research_topic="efficient transformer architectures"
mcp__hf-mcp-server__paper_search --query "$research_topic" --results_limit 20

# 2. Focused subtopic research
mcp__hf-mcp-server__paper_search --query "sparse attention mechanisms"
mcp__hf-mcp-server__paper_search --query "linear attention transformers"

# 3. Recent developments tracking
mcp__hf-mcp-server__paper_search --query "$research_topic 2024"
mcp__hf-mcp-server__paper_search --query "state space models transformer"

# 4. Comparative analysis
mcp__hf-mcp-server__paper_search --query "transformer vs mamba comparison"
mcp__hf-mcp-server__paper_search --query "benchmark efficient attention"
```

## Development Integration Patterns

### Model Evaluation Pipeline
```bash
# Systematic model evaluation
# 1. Identify candidate models
candidates=("microsoft/DialoGPT-medium" "facebook/blenderbot-400M-distill")

# 2. Get detailed information for each
for model in "${candidates[@]}"; do
  echo "Analyzing: $model"
  mcp__hf-mcp-server__model_details --model_id "$model"
done

# 3. Compare key metrics
# - Model size and memory requirements
# - Inference speed benchmarks
# - Task-specific performance scores
# - License compatibility

# 4. Test with representative examples
# - Download and test locally
# - Measure performance on test data
# - Evaluate output quality
```

### Dataset Preprocessing Research
```bash
# Data preparation workflow
# 1. Find preprocessing examples
mcp__hf-mcp-server__hf_doc_search --query "dataset preprocessing transformers"
mcp__hf-mcp-server__hf_doc_search --query "tokenization best practices"

# 2. Find similar dataset implementations
mcp__hf-mcp-server__dataset_search --query "preprocessed text classification"
mcp__hf-mcp-server__dataset_search --query "tokenized conversation data"

# 3. Review preprocessing papers
mcp__hf-mcp-server__paper_search --query "data preprocessing language models"
mcp__hf-mcp-server__paper_search --query "tokenization impact performance"
```

### Technology Stack Research
```bash
# Framework and library research
# 1. Find implementation examples
mcp__hf-mcp-server__space_search --query "pytorch implementation"
mcp__hf-mcp-server__space_search --query "transformers pipeline"

# 2. Documentation deep dive
mcp__hf-mcp-server__hf_doc_search --query "custom model architecture" --product "transformers"
mcp__hf-mcp-server__hf_doc_search --query "training loop implementation"

# 3. Community best practices
mcp__hf-mcp-server__paper_search --query "hugging face transformers tutorial"
mcp__hf-mcp-server__model_search --query "custom architecture" --library "transformers"
```

## Integration with Development Workflow

### Project Initialization
```bash
# Starting new ML project
# 1. Research state-of-the-art for task
project_task="sentiment analysis"
mcp__hf-mcp-server__model_search --query "$project_task" --sort "trendingScore"

# 2. Find baseline datasets
mcp__hf-mcp-server__dataset_search --query "$project_task" --sort "downloads"

# 3. Review recent papers for insights
mcp__hf-mcp-server__paper_search --query "$project_task recent improvements"

# 4. Document findings in project CLAUDE.md
# - Selected baseline models
# - Relevant datasets
# - Key papers and insights
```

### Continuous Learning
```bash
# Weekly research routine
# 1. Check trending models in your domain
mcp__hf-mcp-server__model_search --sort "trendingScore" --limit 10

# 2. Review new papers
mcp__hf-mcp-server__paper_search --query "machine learning" --results_limit 5

# 3. Explore new spaces and demos
mcp__hf-mcp-server__space_search --query "recent demo" --limit 5

# 4. Check documentation updates
mcp__hf-mcp-server__hf_doc_search --query "new features" --product "transformers"
```

## Image Generation Integration

### Flux 1 Schnell Usage
```bash
# Generate images using Hugging Face Spaces
mcp__hf-mcp-server__gr1_flux1_schnell_infer \
  --prompt "A serene mountain landscape at sunset with a lake reflecting the sky" \
  --width 1024 \
  --height 1024 \
  --num_inference_steps 4

# Style transfer with EasyGhibli
# First generate/find source image, then apply style
mcp__hf-mcp-server__gr2_0_abidlabs_easyghiblis_ndition_generate_image \
  --spatial_img "https://example.com/source-image.jpg"
```

## Advanced Research Techniques

### Cross-Reference Research
```bash
# Multi-modal research approach
# 1. Start with model research
base_model="llama-2-7b"
mcp__hf-mcp-server__model_details --model_id "meta-llama/Llama-2-7b-hf"

# 2. Find related fine-tuned versions
mcp__hf-mcp-server__model_search --query "llama-2 fine-tuned"

# 3. Research training datasets
mcp__hf-mcp-server__dataset_search --query "llama training data"

# 4. Review evaluation papers
mcp__hf-mcp-server__paper_search --query "llama-2 evaluation benchmark"

# 5. Find implementation examples
mcp__hf-mcp-server__space_search --query "llama-2 demo"
```

### Competitive Analysis
```bash
# Compare similar solutions
# 1. Define comparison criteria
criteria=("model size" "inference speed" "accuracy" "license")

# 2. Gather competitor information
competitors=("gpt-3.5" "claude" "llama-2" "mistral")

# 3. Research each systematically
for competitor in "${competitors[@]}"; do
  mcp__hf-mcp-server__model_search --query "$competitor"
  mcp__hf-mcp-server__paper_search --query "$competitor evaluation"
done

# 4. Create comparison matrix
# Document findings in structured format for decision making
```

## Error Handling and Optimization

### Rate Limiting Management
```bash
# Handle API rate limits gracefully
# 1. Monitor usage patterns
# 2. Implement caching for repeated queries
# 3. Batch related requests when possible
# 4. Use pagination for large result sets

# Example: Efficient model discovery
mcp__hf-mcp-server__model_search --query "specific-task" --limit 50
# vs multiple small queries
```

### Result Quality Optimization
```bash
# Improve search relevance
# 1. Use specific, descriptive queries
mcp__hf-mcp-server__model_search --query "conversational AI customer service" 
# vs generic "chatbot"

# 2. Combine multiple search criteria
mcp__hf-mcp-server__model_search --query "medical AI" --author "microsoft" --task "text-classification"

# 3. Use concise mode for broad searches
mcp__hf-mcp-server__paper_search --query "deep learning" --concise_only true --results_limit 20
```

This module provides comprehensive patterns for leveraging Hugging Face's ecosystem through MCP integration for AI research and development workflows.