from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

code = '''class MyClass:
	"This is my second class"
	a = 10
	def func(self):
		print('Hello')

# create a new MyClass
ob = MyClass()

# Output: <function MyClass.func at 0x000000000335B0D0>
print(MyClass.func)

# Output: <bound method MyClass.func of <__main__.MyClass object at 0x000000000332DEF0>>
print(ob.func)

# Calling function func()
# Output: Hello
ob.func()'''
print(highlight(code, PythonLexer(), HtmlFormatter()))
print(highlight(code, PythonLexer(), HtmlFormatter()))
print(list(PythonLexer().get_tokens(code)))
