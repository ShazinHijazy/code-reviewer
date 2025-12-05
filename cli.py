#!/usr/bin/env python3
"""
Code Reviewer CLI - Command line interface for the code reviewer
"""

import sys
import json
import argparse
from pathlib import Path
from code_reviewer import CodeReviewer

def review_file(filepath: str, output_format: str = "text") -> None:
    """Review a single file"""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)
    
    reviewer = CodeReviewer(code, filepath)
    issues = reviewer.review()
    
    if output_format == "json":
        report = reviewer.get_report()
        print(json.dumps(report, indent=2))
    else:
        reviewer.print_report()

def review_directory(dirpath: str, extension: str = ".py") -> None:
    """Review all files in a directory"""
    path = Path(dirpath)
    
    if not path.exists():
        print(f"❌ Directory not found: {dirpath}")
        sys.exit(1)
    
    files = list(path.glob(f"**/*{extension}"))
    
    if not files:
        print(f"No {extension} files found in {dirpath}")
        return
    
    total_issues = 0
    total_files = 0
    
    print(f"\n📁 Reviewing {len(files)} files in {dirpath}\n")
    print("="*70)
    
    for filepath in files:
        try:
            with open(filepath, 'r') as f:
                code = f.read()
            
            reviewer = CodeReviewer(code, str(filepath))
            issues = reviewer.review()
            
            if issues:
                total_issues += len(issues)
                total_files += 1
                
                severity_count = {}
                for issue in issues:
                    sev = issue.severity.value
                    severity_count[sev] = severity_count.get(sev, 0) + 1
                
                print(f"\n{filepath}")
                print(f"  Issues: {len(issues)} {severity_count}")
        
        except Exception as e:
            print(f"❌ Error reviewing {filepath}: {e}")
    
    print("\n" + "="*70)
    print(f"\n📊 Summary:")
    print(f"   Files with issues: {total_files}/{len(files)}")
    print(f"   Total issues: {total_issues}")

def main():
    parser = argparse.ArgumentParser(
        description="Static Code Reviewer - Review Python code without LLM APIs"
    )
    
    parser.add_argument(
        "path",
        help="File or directory to review"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "-e", "--extension",
        default=".py",
        help="File extension to review (default: .py)"
    )
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if path.is_file():
        review_file(args.path, args.format)
    elif path.is_dir():
        review_directory(args.path, args.extension)
    else:
        print(f"❌ Path is neither a file nor directory: {args.path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
