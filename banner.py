import time

# ANSI escape codes for colors
RED = "\033[91m"
WHITE = "\033[97m"
RESET = "\033[0m"

def print_banner():
    R = RED + "█" + WHITE  # Red block character
    W = WHITE + "█" + WHITE  # White block character

    banner = f"""
{W}{W}     {W}{W}  {R}{R}{R}{R}{R}  {R}{R} {W}{W}{W}{W}{W}{W}  
{W}{W}     {W}{W} {R}{R}   {R}{R} {R}{R} {W}{W}   {W}{W} 
{W}{W}  {W}  {W}{W} {R}{R}{R}{R}{R}{R}{R} {R}{R} {W}{W}   {W}{W}  
{W}{W} {W}{W}{W} {W}{W} {R}{R}   {R}{R} {R}{R} {W}{W}   {W}{W} 
 {W}{W}{W} {W}{W}{W}  {R}{R}   {R}{R} {R}{R} {W}{W}{W}{W}{W}{W}  

What Am I Doing
AI-Powered Activity Summarizer
Version: 1.0.0 | License: MIT
{RESET}
"""
    print(banner)

if __name__ == "__main__":
    print_banner()