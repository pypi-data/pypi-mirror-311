# 0.10.0
- Instead of non-breaking hyphen we are now using 
  regular hyphen surrounded with word joiner symbols

# 0.9.1
- Updated the rule for non-breaking hyphens between short words.
  Now, digits are considered part of a word.
- If either the word on the left or right of the hyphen contains up to 4 characters,
  the hyphen is automatically replaced with a non-breaking hyphen.

# 0.9.0
- Disable fractions replacement 

# 0.8.1
- Add non-breaking space after numbers up to 4 digits. (Before it was up to 3 digits)

# 0.8.0
- Prohibits line breaks if two numbers are separated by m-dash symbol.
- The rules for the m-dash (—) `\u2014` are also applied to the horizontal bar (―) `\u2015`.

# 0.2.0
- Add expression to replace positional spaces with non-breakable spaces
after certain words
