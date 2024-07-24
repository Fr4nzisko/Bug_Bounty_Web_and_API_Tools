# Fuzzing API Wordlist 

A wordlist of API names used for fuzzing web application APIs.

## Contents

- API_seen_in_wild.txt - Contains API function names that I have seen in the wild.
- Actions.txt - All API function name verbs.
- Objects-lowercase.txt - All API function names.
- Actions-uppercase.txt - API function name verbs with uppercase as the initial character.
- Objects-uppercase.txt - Contains the above, but adding versions and a longer list of possible endponits.
- Actions-lowercase.txt - API function name verbs with lowercase left.
- objects-uppercase.txt - API function naming verbs nouns with uppercase on the left.
- objects-lowercase.txt - API function for naming nouns with lowercase on the left.

## Usage

1.  In Burp Suite, send an API request you want to fuzz to Intruder.
2.  Remove the existing API function call, and replace it with two § characters for each text file you want to use.
3.  On the "Positions" tab, set Attack type to "Cluster Bomb".
4.  On the "Payloads" tab, select 1 for the first Payload set drop-down, then select a Payload type of "Runtime file" and navigate to the directory you downloaded these text files to. Select "actions.txt".
5.  Repeat step 4 by setting Payload set 2 to "objects.txt".
6.  (optional step - add more payload sets and set them to "objects.txt" to test for multi-part objects like "UserAccount").
7.  Start attack!

## Comments

If you use this and it's helpful, I'd love to hear about it! (https://x.com/Fr4nzisko1). If you think I've missed any obvious word choices, I'd love to hear about that as well, or feel free to add them.
