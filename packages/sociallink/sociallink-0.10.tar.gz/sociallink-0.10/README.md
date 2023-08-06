# Encodes and decodes a URL using a specified symbol to prevent spam detection on platforms like Facebook and YouTube

### pip install sociallink

```python
	site_decode_encode(url, symb="Ç"):
        Encodes and decodes a URL using a specified symbol to prevent spam detection on platforms like Facebook and YouTube.


        I have a YouTube channel about Python https://www.youtube.com/channel/UC3DeX0cPlJaLSD254T7fpdA, and YouTube makes it hard for my subscribers to post links in the comments.
        This is a module than encodes/decodes urls in a way that everybody can still understand that the encoded string
        is a url.

        Args:
            url (str): The URL to be encoded or decoded.
            symb (str, optional): The symbol used for encoding and decoding. Defaults to 'Ç'.

        Returns:
            str: The encoded or decoded URL.

        Examples:
    import random
    urls = ['https://gh.io/navigation-update',
    'https://github.blog/',
    'https://docs.github.com/site-policy/github-terms/github-terms-of-service',
    'https://docs.github.com/site-policy/privacy-policies/github-privacy-statement',
    'https://www.githubstatus.com/',
    'https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax',
    'https://gist.github.com/',
    'https://gist.github.com/mine',
    'https://docs.github.com/',
    'https://support.github.com/',
    'https://github.dev/',
    'https://docs.github.com/articles/which-remote-url-should-i-use',
    'https://cli.github.com/',
    'x-github-client://openRepo/https://github.com/hansalemaos/Tutorial_cpp_in_python',
    'git-client://clone?repo=https%3A%2F%2Fgithub.com%2Fhansalemaos%2FTutorial_cpp_in_python',
    'https://desktop.github.com/',
    'https://developer.apple.com/xcode/',
    'https://www.youtube.com/watch?v=ChZ9753o690',
    'https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&cid=2030&workload=dotnet-dotnetwebcloud&passive=false#dotnet',
    'https://support.github.com/?tags=dotcom-footer',
    'https://services.github.com/', ]

    for url1 in urls:
        symb = random.choice(['Ç', '#', '@'])
        en1 = site_decode_encode(url=url1, symb=symb)
        de1 = site_decode_encode(url=en1, symb=symb)
        print(f'encoded: {en1}, decoded: {de1}')

    # encoded: hÇtÇtÇpÇsÇ:Ç/Ç/ÇgÇhÇ.ÇiÇoÇ/ÇnÇaÇvÇiÇgÇaÇtÇiÇoÇnÇ-ÇuÇpÇdÇaÇtÇe, decoded: https://gh.io/navigation-update
    # encoded: h@t@t@p@s@:@/@/@g@i@t@h@u@b@.@b@l@o@g@/, decoded: https://github.blog/
    # encoded: h@t@t@p@s@:@/@/@d@o@c@s@.@g@i@t@h@u@b@.@c@o@m@/@s@i@t@e@-@p@o@l@i@c@y@/@g@i@t@h@u@b@-@t@e@r@m@s@/@g@i@t@h@u@b@-@t@e@r@m@s@-@o@f@-@s@e@r@v@i@c@e, decoded: https://docs.github.com/site-policy/github-terms/github-terms-of-service
    # encoded: h#t#t#p#s#:#/#/#d#o#c#s#.#g#i#t#h#u#b#.#c#o#m#/#s#i#t#e#-#p#o#l#i#c#y#/#p#r#i#v#a#c#y#-#p#o#l#i#c#i#e#s#/#g#i#t#h#u#b#-#p#r#i#v#a#c#y#-#s#t#a#t#e#m#e#n#t, decoded: https://docs.github.com/site-policy/privacy-policies/github-privacy-statement
    # encoded: h@t@t@p@s@:@/@/@w@w@w@.@g@i@t@h@u@b@s@t@a@t@u@s@.@c@o@m@/, decoded: https://www.githubstatus.com/
    # encoded: h#t#t#p#s#:#/#/#d#o#c#s#.#g#i#t#h#u#b#.#c#o#m#/#e#n#/#s#e#a#r#c#h#-#g#i#t#h#u#b#/#g#i#t#h#u#b#-#c#o#d#e#-#s#e#a#r#c#h#/#u#n#d#e#r#s#t#a#n#d#i#n#g#-#g#i#t#h#u#b#-#c#o#d#e#-#s#e#a#r#c#h#-#s#y#n#t#a#x, decoded: https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax
    # encoded: h@t@t@p@s@:@/@/@g@i@s@t@.@g@i@t@h@u@b@.@c@o@m@/, decoded: https://gist.github.com/
    # encoded: h@t@t@p@s@:@/@/@g@i@s@t@.@g@i@t@h@u@b@.@c@o@m@/@m@i@n@e, decoded: https://gist.github.com/mine
    # encoded: h@t@t@p@s@:@/@/@d@o@c@s@.@g@i@t@h@u@b@.@c@o@m@/, decoded: https://docs.github.com/
    # encoded: hÇtÇtÇpÇsÇ:Ç/Ç/ÇsÇuÇpÇpÇoÇrÇtÇ.ÇgÇiÇtÇhÇuÇbÇ.ÇcÇoÇmÇ/, decoded: https://support.github.com/
    # encoded: h@t@t@p@s@:@/@/@g@i@t@h@u@b@.@d@e@v@/, decoded: https://github.dev/
    # encoded: h#t#t#p#s#:#/#/#d#o#c#s#.#g#i#t#h#u#b#.#c#o#m#/#a#r#t#i#c#l#e#s#/#w#h#i#c#h#-#r#e#m#o#t#e#-#u#r#l#-#s#h#o#u#l#d#-#i#-#u#s#e, decoded: https://docs.github.com/articles/which-remote-url-should-i-use
    # encoded: h#t#t#p#s#:#/#/#c#l#i#.#g#i#t#h#u#b#.#c#o#m#/, decoded: https://cli.github.com/
    # encoded: x#-#g#i#t#h#u#b#-#c#l#i#e#n#t#:#/#/#o#p#e#n#R#e#p#o#/#h#t#t#p#s#:#/#/#g#i#t#h#u#b#.#c#o#m#/#h#a#n#s#a#l#e#m#a#o#s#/#T#u#t#o#r#i#a#l#_#c#p#p#_#i#n#_#p#y#t#h#o#n, decoded: x-github-client://openRepo/https://github.com/hansalemaos/Tutorial_cpp_in_python
    # encoded: g@i@t@-@c@l@i@e@n@t@:@/@/@c@l@o@n@e@?@r@e@p@o@=@h@t@t@p@s@%@3@A@%@2@F@%@2@F@g@i@t@h@u@b@.@c@o@m@%@2@F@h@a@n@s@a@l@e@m@a@o@s@%@2@F@T@u@t@o@r@i@a@l@_@c@p@p@_@i@n@_@p@y@t@h@o@n, decoded: git-client://clone?repo=https%3A%2F%2Fgithub.com%2Fhansalemaos%2FTutorial_cpp_in_python
    # encoded: h@t@t@p@s@:@/@/@d@e@s@k@t@o@p@.@g@i@t@h@u@b@.@c@o@m@/, decoded: https://desktop.github.com/
    # encoded: hÇtÇtÇpÇsÇ:Ç/Ç/ÇdÇeÇvÇeÇlÇoÇpÇeÇrÇ.ÇaÇpÇpÇlÇeÇ.ÇcÇoÇmÇ/ÇxÇcÇoÇdÇeÇ/, decoded: https://developer.apple.com/xcode/
    # encoded: h@t@t@p@s@:@/@/@w@w@w@.@y@o@u@t@u@b@e@.@c@o@m@/@w@a@t@c@h@?@v@=@C@h@Z@9@7@5@3@o@6@9@0, decoded: https://www.youtube.com/watch?v=ChZ9753o690
    # encoded: h@t@t@p@s@:@/@/@v@i@s@u@a@l@s@t@u@d@i@o@.@m@i@c@r@o@s@o@f@t@.@c@o@m@/@t@h@a@n@k@-@y@o@u@-@d@o@w@n@l@o@a@d@i@n@g@-@v@i@s@u@a@l@-@s@t@u@d@i@o@/@?@s@k@u@=@C@o@m@m@u@n@i@t@y@&@c@h@a@n@n@e@l@=@R@e@l@e@a@s@e@&@v@e@r@s@i@o@n@=@V@S@2@0@2@2@&@s@o@u@r@c@e@=@V@S@L@a@n@d@i@n@g@P@a@g@e@&@c@i@d@=@2@0@3@0@&@w@o@r@k@l@o@a@d@=@d@o@t@n@e@t@-@d@o@t@n@e@t@w@e@b@c@l@o@u@d@&@p@a@s@s@i@v@e@=@f@a@l@s@e@#@d@o@t@n@e@t, decoded: https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&cid=2030&workload=dotnet-dotnetwebcloud&passive=false#dotnet
    # encoded: h#t#t#p#s#:#/#/#s#u#p#p#o#r#t#.#g#i#t#h#u#b#.#c#o#m#/#?#t#a#g#s#=#d#o#t#c#o#m#-#f#o#o#t#e#r, decoded: https://support.github.com/?tags=dotcom-footer
    # encoded: hÇtÇtÇpÇsÇ:Ç/Ç/ÇsÇeÇrÇvÇiÇcÇeÇsÇ.ÇgÇiÇtÇhÇuÇbÇ.ÇcÇoÇmÇ/, decoded: https://services.github.com/
```	