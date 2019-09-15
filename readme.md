# WhitePages
This has python code to screen scrape the whitepages.com.au website for Residential.

Apparently, there is an API.
http://developers.sensis.com.au/member/register

But webpage says. Registration is currently disabled.

So screen scraper it is.

### Example usage
```
$ python whitepages.py surname firstname postcode
```

The return value seems unusual cos it's meant to be read back by Amazon Lex.


## AWS
I deployed this function as a AWS Lambda (region Sydney)  and when testing it, it times out when trying to connect to whitepages.com.au

Looking at the logs, it was using this URL.
```
https://www.whitepages.com.au/residential/results?name=Chai&givenName=Ang&location=Camberwell,%20VIC,%203124
```

I tried it in my browser, it works.
I then connected to the internet via a VPN (Private Internet Access). I connected to the Melbourne POP and tried the above URL again.

I get ```Access Denied
You don't have permission to access "http://www.whitepages.com.au/residential/results?" on this server.
Reference #18.60464868.1568538276.12ff82c4```

I tried the Sydney POP, the NZ, California, Singapore POP. Same issue. The __US West__ and __Perth__ was __OK__. As soon as I disconnect from the VPN, it is __OK__ again.

I havent tried deploying to every AWS region to see if any of the regions would work, but the AWS Sydney region is timing out.
