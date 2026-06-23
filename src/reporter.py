# src/reporter
from colorama import init, Fore, Style
import os
import json

init(autoreset=True)

class ConsoleReporter:
    @staticmethod

    def report(issues:list):
        if not issues:
            print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ No issues found. Code is clean!")            
            return
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}=== STATIC ANALYSIS REPORT ===")
        print("-" * 50)
        

        for issue in issues:
            file_path = os.path.basename(issue.get('file_path','unknown'))
            line = issue.get('line','?')
            column = issue.get('column','?')
            message = issue.get('message','')
            severity = issue.get('severity','WARNING').upper()
            if severity=='ERROR':
                severity_str=f"{Fore.RED}{Style.BRIGHT}[ERROR]{Style.RESET_ALL}"
            elif severity == 'WARNING':
                severity_str = f"{Fore.YELLOW}{Style.BRIGHT}[WARNING]{Style.RESET_ALL}"
            else:
                severity_str = f"{Fore.BLUE}[INFO]{Style.RESET_ALL}"
            print(f"{severity_str} {file_path}:{line}:{column} - {message}")

        print("-" * 50)
        print(f"{Fore.CYAN}Total issues found: {len(issues)}")

    def report_as_json(issues:list):
        json_output_list = []
        for issue in issues:
            clean_issue ={
                'file_path': issue.get('file_path', 'unknown'),
                'line': issue.get('line', '?'),
                'column': issue.get('column', '?'),
                'message': issue.get('message', ''),
                'type': issue.get('severity', 'WARNING')  # کلید severity را به type نگاشت می‌کنیم
            
            }
            json_output_list.append(clean_issue)
        json_string = json.dumps(json_output_list,indent=2)
        print(json_string)
        
