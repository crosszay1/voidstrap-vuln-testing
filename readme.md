# Voidstrap Vulnerability Testing 

This was a single day project I did to test and help improve security of the extremely popular Roblox Bootstraper "VoidStrap" (See: https://voidstrapp.pages.dev & https://github.com/KloBraticc/Voidstrap)

I specifically targeted the website's "gameboard" feature, while allowed users to vote on Roblox games, which would then be featured on the website.

## Findings
- Voidstraps website uses a lenient captcha on signup, allowing malicious actors to easily create hundreds of accounts automatically, without so much as having to pay for captcha bypassing software
- Voidstrap's only ratelimits account signups in any impactful capacity.

Using this repo, I was able to create many voidstrap accounts, and bring games to the front page.

Voidstrap's owner and lead developer thanking me
<img width="598" height="80" alt="image" src="https://github.com/user-attachments/assets/5a4b4e0c-ecc2-4d73-8777-14b54d25e02e" />

# This repo will stay private until the vulnerabilities have been fixed.
- As of 8/18/2026 when I am writing this, they have not been patched
