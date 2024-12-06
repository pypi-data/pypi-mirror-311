from typing import List, Dict, Any
import asyncio
from .base import BaseModel
import json
import requests

class LocalModel(BaseModel):
    """Implementation for local or self-hosted models."""
    
    def __init__(self, 
                 model_type: str = "api",
                 endpoint_url: str = None,
                 model_path: str = None,
                 device: str = "cuda",
                 batch_size: int = 4,
                 max_concurrent: int = 4):
        """
        Initialize local model.
        
        Args:
            model_type: "api" or "hf" (HuggingFace)
            endpoint_url: URL for API endpoint if using API mode
            model_path: Path/name of model if using HuggingFace mode
            device: Device to run model on ("cuda" or "cpu")
            batch_size: Batch size for processing
            max_concurrent: Maximum concurrent requests/batches
        """
        self.model_type = model_type
        self.endpoint_url = endpoint_url
        self.model_path = model_path
        self.device = device
        self.batch_size = batch_size
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        # Initialize model based on type
        if model_type == "hf":
            try:
                from transformers import AutoModelForCausalLM, AutoTokenizer
                self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path
                ).to(device)
            except ImportError:
                raise ImportError("Please install transformers: pip install transformers torch")
        
        self.prompt_template = """Which of the following options would you prefer?:

Option A:
{option_a}

Option B:
{option_b}

Please respond with only "A" or "B"."""

    async def _get_response_api(self, prompt: str) -> str:
        """Get response from API endpoint."""
        try:
            response = requests.post(
                self.endpoint_url,
                json={
                    "prompt": prompt,
                    "max_tokens": 10,
                }
            )
            if response.status_code == 200:
                result = response.json()
                return result.get("text", "").strip()
        except Exception as e:
            print(f"API call error: {e}")
        return None

    async def _get_response_hf(self, prompt: str) -> str:
        """Get response from HuggingFace model."""
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=10,
                temperature=0.7,
                do_sample=True
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response.replace(prompt, "").strip()
            
            # Extract A or B from response
            if 'A' in response:
                return 'A'
            elif 'B' in response:
                return 'B'
        except Exception as e:
            print(f"Model inference error: {e}")
        return None

    async def _get_single_response(self, option_a: str, option_b: str) -> str:
        """Get single response from model."""
        prompt = self.prompt_template.format(
            option_a=option_a,
            option_b=option_b
        )
        
        async with self.semaphore:
            if self.model_type == "api":
                return await self._get_response_api(prompt)
            else:
                return await self._get_response_hf(prompt)

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
                                num_samples: int = 10) -> List[Dict[str, int]]:
        """Compare multiple pairs in batch."""
        all_tasks = []
        for option_a, option_b in pairs:
            pair_tasks = [
                self._get_single_response(option_a, option_b)
                for _ in range(num_samples)
            ]
            all_tasks.append(asyncio.gather(*pair_tasks))
            
        all_responses = await asyncio.gather(*all_tasks)
        
        results = []
        for responses in all_responses:
            counts = {'A': 0, 'B': 0}
            for response in responses:
                if response in counts:
                    counts[response] += 1
            results.append(counts)
            
        return results