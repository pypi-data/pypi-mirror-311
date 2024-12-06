from check11.base_test import BaseTest

class SingleFileTest(BaseTest):
	def __init__(self, gituser: str, aname: str, modname: str, mods, no_trace: bool, errors_only: bool):
		super().__init__()
		self.gitname = gituser
		self.mods = mods #  [0] = test mod, [1] = user mod
		self.aname = aname
		self.modname = modname
		self.no_trace = no_trace
		self.errors_only = errors_only
		self.set_functions(['exit_hello']) # 'bestaat_niet'])

	def test_exit(self):
		funcname = 'exit_hello'
		pars = '():'
		testname = 'for proper sys.exit message'
		self.sys_exit(
			funcname,
			pars,
			testname,
			'Hello World',
			[],
			[],
		)

