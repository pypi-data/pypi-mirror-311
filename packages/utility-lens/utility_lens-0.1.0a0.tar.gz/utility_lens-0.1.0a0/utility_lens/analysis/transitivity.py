import asyncio
from typing import List, Dict, Any
import itertools
import random
from tqdm import tqdm
import math
from ..models.base import BaseModel

class TransitivityAnalyzer:
    """Analyzer for measuring preference transitivity. Provides both sync and async interfaces."""
    
    def __init__(self,
                 model: 'BaseModel',
                 items: List[str],
                 n_trial: int = 10,
                 n_triad: int = 200,
                 seed: int = 42,
                 save_directory: str = None):
        random.seed(seed)
        self.model = model
        self.items = items
        self.n_trial = n_trial
        self.n_triad = n_triad
        self.save_directory = save_directory

        # Add stats computations
        self.total_possible_triads = math.comb(len(items), 3)  # Total possible unique triads from n items
        self.triads_to_sample = min(n_triad, self.total_possible_triads)  # Actual number of triads we'll analyze
        self.total_comparisons = self.triads_to_sample * 6  # Each triad needs 6 comparisons (3 pairs × 2 directions)

        print(f"> Processing {len(items)} items")
        print(f"> Sampling {self.triads_to_sample} (triads) out of {self.total_possible_triads} (triads) possible")
        print(f"> A total of {self.triads_to_sample} (triads) x 3 (pairs per triad) x 2 (order shuffle) = {self.total_comparisons} pairwise comparisons are needed")
        print(f"> A total of {self.total_comparisons} (pairs) x {self.n_trial} (trials per pair) = {self.n_trial * self.total_comparisons} API calls will be made")
        
    def _generate_triads(self) -> List[tuple[int, int, int]]:
        """Generate triads for comparison."""
        all_triads = list(itertools.combinations(range(len(self.items)), 3))
        
        if self.n_triad == -1:
            return all_triads
        else:
            return random.sample(all_triads, min(self.n_triad, len(all_triads)))
            
    def _get_pairs_from_triad(self, triad: tuple[int, int, int]) -> List[tuple[str, str]]:
        """Get all pairs to compare from a triad."""
        a, b, c = triad
        pairs = []
        for i, j in [(a,b), (b,c), (a,c)]:
            pairs.append((self.items[i], self.items[j]))
            pairs.append((self.items[j], self.items[i]))  # Also do reverse
        return pairs
    
    def run(self) -> Dict[str, Any]:
        """
        Synchronous interface for running transitivity analysis.
        
        Returns:
            Dictionary containing transitivity results
        """
        return asyncio.run(self._analyze_async())

    async def run_async(self) -> Dict[str, Any]:
        """
        Asynchronous interface for running transitivity analysis.
        
        Returns:
            Dictionary containing transitivity results
        """
        return await self._analyze_async()

    async def _analyze_async(self) -> Dict[str, Any]:
        """
        Run transitivity analysis.
        
        Returns:
            Dictionary containing:
            - triad_results: List of results for each triad
            - transitivity_score: Overall transitivity score
            - cycles: List of discovered preference cycles
        """
        # 1. Generate triads
        # [(3, 14, 24), (...), ...]
        triads = self._generate_triads()
        
        # 2. Generate all comparison info
        # [{'key': 't0_Tiger_Kangaroo', 'triad_idx': 0, 'triad_indices': (3, 14, 24), 'triad_items': ['Tiger', 'Kangaroo', 'Horse'], 'pair': ('Tiger', 'Kangaroo')}, {...}, ...]
        comparison_info = []

        with tqdm(total=len(triads), desc="Generating pairs", unit="triad") as pbar:
            for triad_idx, triad in enumerate(triads):
                triad_items = [self.items[i] for i in triad]
                pairs = self._get_pairs_from_triad(triad)
                
                for i, pair in enumerate(pairs):
                    item1, item2 = pair
                    key = f"t{triad_idx}_{item1}_{item2}"
                    
                    comparison_info.append({
                        'key': key,
                        'triad_idx': triad_idx,
                        'triad_indices': triad,
                        'triad_items': triad_items,
                        'pair': pair,
                    })
                pbar.update(1)

        # 3. Get model's responses
        # [{'key': 't0_Tiger_Kangaroo', 'triad_idx': 0, 'triad_indices': (3, 14, 24), 'triad_items': ['Tiger', 'Kangaroo', 'Horse'], 'pair': ('Tiger', 'Kangaroo'), 'counts': {'A': 7, 'B': 13}}, {...}, ...]
        with tqdm(total=len(comparison_info), desc="Comparing pairs", unit="pair") as pbar:
            pairs_to_compare = [info['pair'] for info in comparison_info]
            model_results = await self.model.batch_compare_pairs(pairs_to_compare, self.n_trial)
            
            # Add results back to comparison_info
            for info, (pair, counts) in zip(comparison_info, model_results):
                if info['pair'] != pair:
                    print(f"Warning: Pair mismatch detected: {info['pair']} != {pair}")
                    continue
                info['counts'] = counts
                pbar.update(1)

        # 4. Process results by triad
        triad_results = []
        all_cycles = []  # Store all cycles for sorting later
        total_transitivity = 0

        # First calculate all strengths (strength of preferring first item over the second)
        # {'t0_Tiger_Kangaroo': 0.675, 't0_Kangaroo_Tiger': 0.325, 't0_Kangaroo_Horse': 0.6, 't0_Horse_Kangaroo': 0.4, 't0_Tiger_Horse': 0.725, 't0_Horse_Tiger': 0.275, ...}
        strengths = {}

        # Group comparisons by triad
        for triad_idx in range(len(triads)):
            triad_comparisons = [info for info in comparison_info if info['triad_idx'] == triad_idx]
            items = triad_comparisons[0]['triad_items']
            
            # Process each pair in the triad
            pairs = [(items[0], items[1]), (items[1], items[2]), (items[0], items[2])]
            for item1, item2 in pairs:
                # Find the two comparisons for this pair
                key1 = f"t{triad_idx}_{item1}_{item2}"
                key2 = f"t{triad_idx}_{item2}_{item1}"
                
                comp1 = next(comp for comp in triad_comparisons if comp['key'] == key1)
                comp2 = next(comp for comp in triad_comparisons if comp['key'] == key2)
                
                # Get total responses
                total_responses = sum(comp1['counts'].values()) + sum(comp2['counts'].values())
                
                if total_responses > 0:
                    # Calculate how many times item1 was preferred:
                    # Times chosen when presented as A in first comparison
                    # Plus times chosen as B in second comparison
                    count_item1_preferred = comp1['counts']['A'] + comp2['counts']['B']
                    count_item2_preferred = comp1['counts']['B'] + comp2['counts']['A']
                    
                    # Calculate probabilities
                    p_first_over_second = count_item1_preferred / total_responses
                    p_second_over_first = count_item2_preferred / total_responses

                    if not p_first_over_second + p_second_over_first == 1:
                        raise ValueError("p_first_over_second and p_second_over_first don't sum up to 1")

                    # Store both directions
                    strengths[key1] = p_first_over_second
                    strengths[key2] = p_second_over_first

        with tqdm(total=len(triads), desc="Processing results", unit="triad") as pbar:
            for triad_idx in range(len(triads)):
                # Get this triad's comparisons
                triad_comparisons = [info for info in comparison_info if info['triad_idx'] == triad_idx]
                items = triad_comparisons[0]['triad_items'] # ['Tiger', 'Kangaroo', 'Horse']

                # Get triad's strength keys
                triad_strengths = {
                    key: value for key, value in strengths.items() 
                    if key.startswith(f"t{triad_idx}")
                } # {'t0_Tiger_Kangaroo': 0.675, 't0_Kangaroo_Tiger': 0.325, 't0_Kangaroo_Horse': 0.6, 't0_Horse_Kangaroo': 0.4, 't0_Tiger_Horse': 0.725, 't0_Horse_Tiger': 0.275}

                # Check for cycles
                # For items [A,B,C], check:
                # 1. A over B, B over C, C over A
                # 2. A over C, C over B, B over A
                possible_cycles = [
                    [f"t{triad_idx}_{items[0]}_{items[1]}",
                    f"t{triad_idx}_{items[1]}_{items[2]}",
                    f"t{triad_idx}_{items[2]}_{items[0]}"],
                    
                    [f"t{triad_idx}_{items[0]}_{items[2]}",
                    f"t{triad_idx}_{items[2]}_{items[1]}",
                    f"t{triad_idx}_{items[1]}_{items[0]}"]
                ]
                
                cycle_prob = 0
                for cycle in possible_cycles:
                    cycle_preferences = []
                    all_exist = True
                    
                    for key in cycle:
                        if key not in triad_strengths:
                            all_exist = False
                            break
                        cycle_preferences.append(triad_strengths[key])
                    
                    if all_exist:
                        prob = cycle_preferences[0] * cycle_preferences[1] * cycle_preferences[2]
                        cycle_prob += prob
                        
                        if prob > 0:
                            # Parse items from keys
                            cycle_items = []
                            for key in cycle:
                                item1, item2 = key.split('_')[1:3]
                                cycle_items.append(item1)
                            
                            all_cycles.append({
                                'probability': prob,
                                'cycle_path': (
                                    f"{cycle_items[0]} picked over {cycle_items[1]}, "
                                    f"{cycle_items[1]} picked over {cycle_items[2]}, "
                                    f"{cycle_items[2]} picked over {cycle_items[0]} å"
                                ),
                                'triaåd': items
                            })
                
                transitivity_score = 1 - cycle_prob
                total_transitivity += transitivity_score
                
                triad_results.append({
                    'triad': items,
                    'strengths': triad_strengths,
                    'transitivity_score': transitivity_score,
                    'comparisons': triad_comparisons
                })
                
                pbar.update(1)

        # Sort cycles by probability_of_cycle (highest prob = least transitive)
        sorted_cycles = sorted(all_cycles, key=lambda x: x['probability'], reverse=True)

        results = {
            'triad_results': triad_results,
            'transitivity_score': total_transitivity / len(triads),
            'possible_cycles': sorted_cycles,
            'raw_data': comparison_info
        }

        # Save if directory was specified
        self.save_results(results)

        return results

    
    def save_results(self, results: Dict[str, Any]):
        """Save analysis results to specified directory."""
        if self.save_directory is None:
            return
            
        import os
        import json
        from datetime import datetime

        # Generate timestamp for this run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create directory if it doesn't exist
        os.makedirs(self.save_directory, exist_ok=True)
        
        # Add metadata to results
        metadata = {
            "timestamp": timestamp,
            "n_items": len(self.items),
            "n_trial": self.n_trial,
            "n_triad": self.n_triad,
            "total_possible_triads": self.total_possible_triads,
            "triads_sampled": self.triads_to_sample,
            "total_comparisons": self.total_comparisons,
            "total_api_calls": self.n_trial * self.total_comparisons
        }
        
        output_data = {
            "metadata": metadata,
            "transitivity_score": results["transitivity_score"],
            "possible_cycles": results["possible_cycles"],
            "triad_results": results["triad_results"],
        }
        
        # Save to file
        filename = f"transitivity_analysis_{timestamp}.json"
        output_path = os.path.join(self.save_directory, filename)
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)