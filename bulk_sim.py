#!/usr/bin/env python3
import pandas as pd
from sim_checker import SIMChecker
import time
import sys

def bulk_check(csv_file):
    df = pd.read_csv(csv_file)
    results = []
    
    checker = SIMChecker()
    
    for index, row in df.iterrows():
        number = str(row['phone'])
        print(f"Checking {number}... ({index+1}/{len(df)})")
        
        result = checker.trace_sim(number)
        results.append(result)
        time.sleep(2)  # Rate limit
    
    result_df = pd.DataFrame(results)
    result_df.to_csv("bulk_results.csv", index=False)
    print("✅ Results saved to bulk_results.csv")

if __name__ == "__main__":
    bulk_check("phones.csv")
