# Voidstrap Vulnerability Testing 

This was a single day project I did to test and help improve security of the extremely popular Roblox Bootstraper "VoidStrap" (See: https://voidstrapp.pages.dev & https://github.com/KloBraticc/Voidstrap)

I specifically targeted the website's "gameboard" feature, while allowed users to vote on Roblox games, which would then be featured on the website.

## Findings
- Voidstraps website uses a lenient captcha on signup, allowing malicious actors to easily create hundreds of accounts automatically, without so much as having to pay for captcha bypassing software
- Voidstrap's only ratelimits account signups in any impactful capacity.

Using this repo, I was able to create many Voidstrap accounts, and bring games to the front page.

# These issues have been now been fixed. Thus this repo has been publicized 
Reported: 7/18/2026
Fixed: 8/18/2026
