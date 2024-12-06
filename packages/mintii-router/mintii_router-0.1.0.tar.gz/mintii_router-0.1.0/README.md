# Mintii Router

The intelligent LLM model selection and optimization library by [Mintii Labs](https://mintii.ai).

## About Mintii Router

Mintii Router is a sophisticated AI model selection system that automatically chooses the best Large Language Model (LLM) for each specific prompt, optimizing for both cost and quality. Our system evaluates over 20 different LLMs in real-time to ensure you get the best possible response while minimizing costs.

## Key Features

- 🎯 **Intelligent Model Selection**: Automatically selects the most suitable LLM for each prompt
- 💰 **Cost Optimization**: Achieve up to 80% cost reduction through smart model routing
- 🚀 **Quality Assurance**: Maintains high-quality responses through sophisticated model evaluation
- 🔄 **Adaptive Learning**: Continuously improves selection criteria based on performance data
- 📊 **Usage Analytics**: Track and optimize your LLM usage patterns

## Installation

```bash
pip install mintii-router
```

## Quick Start

```python
from mintii import Router
from dotenv import load_dotenv
import os

# Load your API keys
load_dotenv()

# Initialize the router
router = Router(api_key=os.getenv('MINTII_API_KEY'))

# Get a response
response = router.generate("Explain quantum computing in simple terms")
print(response.content)
```

## Features

- **Smart Model Selection**: Automatically chooses the best model based on:
  - Prompt complexity
  - Required capabilities
  - Cost constraints
  - Performance requirements

- **Cost Optimization**: Reduces costs by:
  - Selecting cost-effective models
  - Optimizing token usage
  - Balancing quality and cost

- **Quality Assurance**: Maintains high standards through:
  - Model capability matching
  - Response quality monitoring
  - Consistent performance tracking

## Documentation

For full documentation, visit [docs.mintii.ai](https://docs.mintii.ai)

## Support

- Email: support@mintiilabs.com
- Documentation: [docs.mintii.ai](https://docs.mintii.ai)
- Issues: [GitHub Issues](https://github.com/mintiilabs/mintii-router/issues)

## License

Proprietary. Copyright © 2024 Mintii Labs. All rights reserved.