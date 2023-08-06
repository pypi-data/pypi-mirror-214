# youtbe

Developed by vardxg aka Fhivo (c) 2023

## Examples of How To Use (Alpha Version)

How To Start

```python
from youtbe import videoStats
from zeus import banner # When u want Print The Banner, before response.
from vardxg import Center, Colors, Write # For Color, Style etc

# Supported link formats are: https://www.youtube.com/watch?v=kffacxfA7G4, and Mobile Links
#Only links like this please! because my api automatically pulls the videoid from the link.

odin = banner() # Define the Banner as logo

Write.Print(Center.XCenter(odin), Colors.red, interval=0) # Prints the Banner Centered, cuz the Fuctions Provided

result = videoStats(input("\n Link >>> "))
print(result)

```
if u have Questions, contact me on Telegram: https://t.me/Fhivo