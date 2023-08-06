Struid - "Stringy UUID"
By Dale Magee
BSD 3-clause License

# What is it?

The Struid is an extension of python's UUID class which is intended to be more "pythonic" than the builtin UUID.

In particular, the struid makes it easy to compare with a string or integer value, e.g:
```
> a = Struid('deadbeef-d00f-d00f-d00f-c0ffeedecade')
> a == 'deadbeef-d00f-d00f-d00f-c0ffeedecade'
True
> a == 295990755078525382164994183696159263454
True
```

# What else can it do?

Struids also have a new shortstr() method, which allows you to compactify your string representations of UUID values down using extended unicode characters (emojis, or any characters you choose)
 
e.g:
```
> a = Struid('deadbeef-d00f-d00f-d00f-c0ffeedecade')
> a.shortstr()
'🌨🚩💵👤🚡ᚮ🕓💣🐙😝🕴🕤ᛦ'
```

And you can also instantiate a struid from a shortstr, or compare with one:
```
> Struid('🌨🚩💵👤🚡ᚮ🕓💣🐙😝🕴🕤ᛦ')
Struid('deadbeef-d00f-d00f-d00f-c0ffeedecade')
```

You can change the available characters shortstr() can use by setting SHORTSTR_DIGITS, e.g:
```
> import struid
> struid.SHORTSTR_DIGITS = "0123456789AbCdEf"
> a=Struid('deadbeef-d00f-d00f-d00f-c0ffeedecade')
> a.shortstr()
'dEAdbEEfd00fd00fd00fC0ffEEdECAdE'
```
(note that changing the available characters affects the shortstr for all guids, 
 so if you e.g save shortstrings to a file and then change character sets, 
 the shortstrings in the file will no longer match)

# What else do I need to know?

Struids are built to be case-insensitive, i.e you must not include both upper and lowercase of the same character in the SHORTSTR_DIGITS, doing so will cause breakage.

