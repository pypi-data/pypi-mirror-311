import asyncio
from typing import List, Dict, Tuple
from openai import AsyncOpenAI
from .base import BaseModel

class OpenAIModel(BaseModel):
    """OpenAI API model implementation."""
    
    def __init__(self, 
                 model_name: str,
                 api_key: str,
                 base_url: str = None,
                 max_tokens: int = 10,
                 concurrency_limit: int = 50):
        """
        Initialize OpenAI model.
        
        Args:
            model_name: Name of OpenAI model to use
            api_key: OpenAI API key
            base_url: Optional base URL for API (for third-party providers)
            max_tokens: Maximum tokens in response
            concurrency_limit: Maximum concurrent API calls
        """
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.semaphore = asyncio.Semaphore(concurrency_limit)
        
        # Initialize client
        if base_url:
            self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        else:
            self.client = AsyncOpenAI(api_key=api_key)
        
        self.prompt_template = """Which of the following options would you prefer?:

Option A:
{option_a}

Option B:
{option_b}

Please respond with only "A" or "B"."""

    async def _get_single_response(self, option_a: str, option_b: str) -> str:
        """Get single response from API."""
        prompt = self.prompt_template.format(
            option_a=option_a,
            option_b=option_b
        )
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        
        async with self.semaphore:
            try:
                completion = await self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    max_tokens=self.max_tokens
                )
                response = completion.choices[0].message.content.strip()
                # Clean response
                if 'A' in response:
                    return 'A'
                elif 'B' in response:
                    return 'B'
                else:
                    return None
                    
            except Exception as e:
                print(f"Error in API call: {e}")
                return None

    async def compare_pair(self, option_a: str, option_b: str, num_samples: int = 10) -> Dict[str, int]:
        """Compare single pair of options."""
        tasks = [
            self._get_single_response(option_a, option_b)
            for _ in range(num_samples)
        ]
        
        responses = await asyncio.gather(*tasks)
        
        counts = {'A': 0, 'B': 0}
        for response in responses:
            if response in counts:
                counts[response] += 1
                
        return counts

    async def batch_compare_pairs(self, 
                                pairs: List[tuple[str, str]], 
                                num_samples: int = 10) -> List[Tuple[tuple[str, str], Dict[str, int]]]:
        """
        Compare multiple pairs in batch.
        
        Returns:
            List of tuples, each containing (pair, counts) where:
            - pair is the original (option_a, option_b) tuple
            - counts is a dict with counts of 'A' and 'B' responses
        """
        all_tasks = []
        for option_a, option_b in pairs:
            pair_tasks = [
                self._get_single_response(option_a, option_b)
                for _ in range(num_samples)
            ]
            all_tasks.append(asyncio.gather(*pair_tasks))
            
        all_responses = await asyncio.gather(*all_tasks)
        
        results = []
        for (option_a, option_b), responses in zip(pairs, all_responses):
            counts = {'A': 0, 'B': 0}
            for response in responses:
                if response in counts:
                    counts[response] += 1
            results.append(((option_a, option_b), counts))
            
        return results