#!/usr/bin/env python3
import os
import subprocess
import argparse
import sys
import time

def main():
    parser = argparse.ArgumentParser(description="Run QA cycle to detect and auto-repair German remnants in translated files.")
    parser.add_argument('-l', '--lang', required=True, help="Target language code (e.g. en)")
    args = parser.parse_args()

    max_passes = 3
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    qa_script = os.path.join(base_dir, 'scripts', 'qa_german_remnants.py')
    translate_script = os.path.join(base_dir, 'scripts', 'lan_translate.py')

    print(f"=== Starting QA Cycle for language: {args.lang} ===")

    for pass_num in range(1, max_passes + 1):
        print(f"\n--- QA Pass {pass_num}/{max_passes} ---")
        
        # 1. Run QA Script to flag German remnants
        result = subprocess.run(['python3', qa_script, '-l', args.lang], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode == 0:
            print(f"✅ QA Passed! No German remnants found in '{args.lang}'.")
            sys.exit(0)
        elif result.returncode == 1:
            print(f"⚠️ German remnants found and flagged. Triggering surgical repair...")
            # 2. Run lan_translate in surgical fallback mode
            # Since lan_translate processes all files and skips up-to-date ones, we can just run it for the language.
            # It will automatically find the files with Fallback tags and surgically repair them!
            repair_cmd = ['python3', translate_script, '-l', args.lang, 'all']
            print(f"Running: {' '.join(repair_cmd)}")
            
            repair_result = subprocess.run(repair_cmd)
            if repair_result.returncode != 0:
                print(f"❌ Repair script failed with exit code {repair_result.returncode}.")
                sys.exit(repair_result.returncode)
                
            print("Repair cycle complete. Cooling down for 5 seconds before next pass...")
            time.sleep(5)
        else:
            print(f"❌ QA script failed unexpectedly with exit code {result.returncode}.")
            sys.exit(result.returncode)

    print(f"\n❌ QA Cycle finished {max_passes} passes, but German remnants still exist.")
    print("Please check the files manually.")
    sys.exit(1)

if __name__ == '__main__':
    main()
