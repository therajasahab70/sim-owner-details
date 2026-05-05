#!/usr/bin/env python3
import requests
import phonenumbers
import json
import re
from datetime import datetime
import sys
import os

class SIMChecker:
    def __init__(self):
        self.agents = [
            'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
        ]
    
    def validate_phone(self, number):
        """Validate Indian phone number"""
        try:
            parsed = phonenumbers.parse(number, "IN")
            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except:
            pass
        return None
    
    def get_carrier_info(self, number):
        """Get carrier using Numverify API (Free tier available)"""
        api_key = "YOUR_NUMVERIFY_API_KEY"  # Get free key from numverify.com
        url = f"http://apilayer.net/api/validate?access_key={api_key}&number={number}&country_code=IN&format=1"
        
        try:
            resp = requests.get(url, timeout=10)
            data = resp.json()
            if data.get('valid'):
                return {
                    'carrier': data.get('carrier'),
                    'line_type': data.get('line_type')
                }
        except:
            pass
        return None
    
    def trace_sim(self, number):
        """Main SIM tracing function"""
        clean_num = self.validate_phone(number)
        if not clean_num:
            return {"error": "Invalid Indian number"}
        
        result = {
            "number": clean_num,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "processing"
        }
        
        # Carrier lookup
        carrier = self.get_carrier_info(clean_num)
        if carrier:
            result.update(carrier)
            result["status"] = "verified"
        
        # Mock detailed info (replace with real API)
        operators = {
            '91': {'name': 'Airtel', 'circle': 'Delhi'},
            '92': {'name': 'Jio', 'circle': 'Mumbai'},
            '93': {'name': 'Vodafone', 'circle': 'UP'},
            '94': {'name': 'BSNL', 'circle': 'Kerala'}
        }
        
        prefix = clean_num[3:5]
        if prefix in operators:
            result.update(operators[prefix])
        
        return result

def main():
    print("🔍 SIM Owner Details Checker - Termux Edition")
    print("=" * 50)
    
    while True:
        number = input("\n📱 Enter phone number (or 'q' to quit): ").strip()
        
        if number.lower() == 'q':
            print("👋 Goodbye!")
            break
            
        if not number.startswith('9') and not number.startswith('8') and not number.startswith('7'):
            print("❌ Please enter valid 10-digit Indian number")
            continue
        
        checker = SIMChecker()
        result = checker.trace_sim(number)
        
        print("\n📊 RESULTS:")
        print(json.dumps(result, indent=2))
        
        # Save to file
        with open("sim_results.json", "a") as f:
            json.dump(result, f)
            f.write("\n")

if __name__ == "__main__":
    main()
