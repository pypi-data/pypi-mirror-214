"""
The StrUID class
By Dale Magee
BSD 3-clause
"""

from uuid import UUID as UUID_Real, uuid4 as uuid4_real


"""
This is the list of characters allowed in our short strings, lowest-to-highest
 value.
 
You *must not* include both upper and lowercase of the same character!
"""
SHORTSTR_DIGITS="" #"-_=.+*"

#SHORTSTR_DIGITS="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#SHORTSTR_DIGITS+="-_=(){}[]:;."

unicode_ranges = [	# list of tuples of start, stop for unicode values to include in the charset
	#(5792, 5880), 	# runes
	#(128512,128591),# emojis
	(127744,128725), # lots-o-symbols (includes emojis)
	#(8704,8959), # math operators
	#(9728,9983), # misc symbols
	#(10241,10495), # braille
	#(77824,78894), # heiroglyphs
	
]

# populate digits with unicode characters
for start, end in unicode_ranges:
	for i in range(start,end+1):		# emojis start at 128512 - 128591
		SHORTSTR_DIGITS += chr(i)

def set_digits(new_digits:str):
	global SHORTSTR_DIGITS
	SHORTSTR_DIGITS = new_digits

def arb_base(num:int, base:int) -> list:
	# convert number n to arbitrary base
	# from https://stackoverflow.com/a/28666223
	if num == 0:
		return [0]
	digits = []
	while num:
		digits.append(int(num % base))
		num //= base
	return digits[::-1]

def from_arb_base(digit: str, digits:str=None) -> int:
	"""
	convert an arbitrary-base digit into an integer
	digits must be a string containing allowed digits, lowest-highest value
	"""
	if digits is None: digits = SHORTSTR_DIGITS
	ret = max(str(digits).find(str(digit)),0)
	return ret
	

class Struid(UUID_Real):
	"""
	The Struid, or string-like GUID, is an extended GUID class with a few 
	 extra helpers.
	 
	The primary motivation for creating the struid is to make comparison with 
	 UUIDs more pythonic, i.e:
	 Struid('deadbeef-d00f-d00f-d00f-c0ffeedecade') == 'deadbeef-d00f-d00f-d00f-c0ffeedecade'
	You can also compare a struid with an integer or shortstr value.
	
	"""
	def __init__(self,val=None):
		
		intval = val
		if intval is None:
			intval = uuid4_real().int
			
		elif type(val) is not int:
			try:
				# try to convert to uuid
				uuidval = UUID_Real(val)
				intval = uuidval.int
			except Exception as ex:
				pass
				
			if type(intval) is not int:
				intval=None
			
			if intval is None and type(val) is str:
				# try a short string
				shortstrval = Struid.from_shortstr(val)
				intval = shortstrval.int

		if type(intval) is int:
			if not 0 <= intval < 1<<128:
				raise ValueError('int is out of range (need a 128-bit value)')
		else:
			raise ValueError(f"Could not create guid from {intval.__class__.__name__} value '{intval}'")
		
		object.__setattr__(self, 'int', intval)
		
	
	def __eq__(self,other):
		"""
		A Struid is much more tolerant with equality matching than a UUID
		Where a UUID can only be compared with another UUID, a Struid can easily
		 be compared with:
		 * a UUID
		 * an integer
		 * a string
		"""
		if isinstance(other,int):
			return self.int == int(other)
		elif isinstance(other,UUID_Real):
			return self.int == other.int
		elif isinstance(other,str):
			# try to turn strings into uuid. this might throw an exception
			try:
				uuidval = Struid(other)
				return self.int == uuidval.int
			except Exception as ex:
				print(f"could not uuidify: {ex}")
				return False # not a valid uuid	
		else:
			# don't know how to compare
			return False
				
	
	def shortstr(self,digits:str=None):
		"""
		Encode the uuid value into a short string format
		"""
		if digits is None: digits = SHORTSTR_DIGITS
		base = len(digits)
		vals = arb_base(self.int,base)
		#print("vals1",vals)
		return "".join(digits[n] for n in vals)
		
		
	@classmethod
	def from_shortstr(cls, val: str,digits:str=None) -> "Struid":
		"""
		Instantiates a new Struid from a shortstr
		"""
		if digits is None: digits = SHORTSTR_DIGITS
		frombase = len(digits)
		intval=0
		val=str(val)
		exponent=len(str(val))-1
		totval=0
		for character in val:
			charval = from_arb_base(character.lower(),digits.lower()) * ((frombase) ** exponent )
			#print(exponent,charval)
			totval += charval
			exponent -= 1
		return cls(totval)
		
		
class StrUUID(Struid):
	# alias
	pass
	
class UUID(Struid):
	# you can just import UUID from the struid package and get a struid :)
	pass
	
def uuid4():
	return UUID(uuid4_real().int)



def testit():
	print("Welcome to the Struid Library!")
	
	print(f"\nshortstr charset:\n{SHORTSTR_DIGITS}\n(base {len(SHORTSTR_DIGITS)})\n\nDoing some tests...")
	
	strval = str('deadbeef-d00f-d00f-d00f-c0ffeedecade')
	a=UUID(strval)
	print("A:",a)
	short = a.shortstr()
	print("shortstr:",short,", len",len(a.shortstr()))
	b = UUID.from_shortstr(a.shortstr())
	print("B:",b)
	
	# struids are always case-insensitive:
	c = UUID.from_shortstr(a.shortstr().lower())
	print("C:",c)
	
	print("int:",int(a))
	print("type:",type(a))
	
	assert (b == a) is True
	assert (c == a) is True
	# and the struid can be compared with a string
	assert (a == strval) is True
	# and you don't even need the hyphens
	assert a == 'deadbeefd00fd00fd00fc0ffeedecade'
	# but not just any string
	assert (a != 'beadd00f-beef-beef-beeff-c0ffeedecade') is True
	
	# and the struid can be compared with an int
	assert (a == 295990755078525382164994183696159263454) is True
	# but not just any int
	assert (a != 42) is True
	
	# and we can instantiate a new struid from the shortstr
	z = UUID(short)
	print("z:",z)
	assert (z == a) is True
	
	# and you can compare a struid with a shortstr
	assert (z == short) is True
	assert UUID('deadbeef-d00f-d00f-d00f-c0ffeedecade') == str(short)
	
	# Randomised shortstr testing
	num_tests=20 #0000
	print(f"\nDoing {num_tests} random tests:")
	for i in range(1,num_tests+1):
		v = uuid4()
		v2 = UUID(v.int)
		v3 = UUID.from_shortstr(v2.shortstr())
		print(f"{i}:",v," -> ",v2.shortstr(),f"({len(v2.shortstr())}) -> ",v3)
		#print(v,v2,v3)
		assert v3 == v == v2
		
	
	print("\nOK!")
	
if __name__ == "__main__":
	testit()