# pytrics




## Useful Tidbits

**Are cached files messing with your head, can you not see your latest changes when you run code/tests?**

    find . -name "*.pyc" -exec rm -f {} \;
