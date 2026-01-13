#!/usr/bin/env python
"""
Batch process multiple subjects through structural MRI pipeline

Usage:
    python scripts/batch_process.py --n-subjects 5 --output-dir ./outputs
"""

import argparse
from pathlib import Path
import time
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.run_analysis import StructuralPipeline


def main():
    parser = argparse.ArgumentParser(
        description='Batch process structural MRI data'
    )
    parser.add_argument(
        '--n-subjects',
        type=int,
        default=5,
        help='Number of subjects to process (default: 5)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./outputs',
        help='Output directory (default: ./outputs)'
    )
    parser.add_argument(
        '--start-idx',
        type=int,
        default=0,
        help='Starting subject index (default: 0)'
    )
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = StructuralPipeline(output_dir=args.output_dir)
    
    # Process subjects
    results = {}
    total_start = time.time()
    
    print(f"\n{'='*70}")
    print(f"BATCH PROCESSING: {args.n_subjects} subjects")
    print(f"{'='*70}\n")
    
    for i in range(args.start_idx, args.start_idx + args.n_subjects):
        subject_start = time.time()
        
        try:
            print(f"\n{'='*70}")
            print(f"SUBJECT {i} ({i - args.start_idx + 1}/{args.n_subjects})")
            print(f"{'='*70}")
            
            result = pipeline.run_full_pipeline(subject_idx=i)
            
            subject_time = time.time() - subject_start
            results[i] = {
                'status': 'success',
                'time': subject_time
            }
            
            print(f"\n✓ Subject {i} completed in {subject_time:.1f}s")
            
        except Exception as e:
            subject_time = time.time() - subject_start
            results[i] = {
                'status': 'failed',
                'time': subject_time,
                'error': str(e)
            }
            print(f"\n✗ Subject {i} failed: {e}")
    
    # Summary
    total_time = time.time() - total_start
    n_success = sum(1 for r in results.values() if r['status'] == 'success')
    n_failed = len(results) - n_success
    
    print(f"\n{'='*70}")
    print("BATCH PROCESSING SUMMARY")
    print(f"{'='*70}")
    print(f"Total subjects: {len(results)}")
    print(f"Successful:     {n_success}")
    print(f"Failed:         {n_failed}")
    print(f"Total time:     {total_time:.1f}s ({total_time/60:.1f}m)")
    print(f"Average time:   {total_time/len(results):.1f}s per subject")
    print(f"{'='*70}\n")
    
    # Detailed results
    print("Detailed Results:")
    for subject_idx, result in results.items():
        status_icon = '✓' if result['status'] == 'success' else '✗'
        print(f"{status_icon} Subject {subject_idx}: {result['status']} ({result['time']:.1f}s)")
        if result['status'] == 'failed':
            print(f"    Error: {result['error']}")
    
    print()
    
    # Exit with error code if any failed
    if n_failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()