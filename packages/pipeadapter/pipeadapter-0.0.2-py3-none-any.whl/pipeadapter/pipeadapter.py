import os
import logging
import eons
from pathlib import Path

######## START CONTENT ########
# All errors
class FittingError(Exception): pass


# Exception used for miscellaneous errors.
class OtherFittingError(FittingError): pass



#Interface method for use in other python code.
def connect(fitting, input={}, **kwargs):
	connector = Connector()
	return connector(fitting, input, **kwargs)

class Connector(eons.Executor):

	def __init__(this):
		super().__init__(name="Pipe Adapter", descriptionStr="An eons adapter for Pipedream")

		#Spoof args, since we won't be using this on the command line.
		this.args = eons.util.DotDict({
			'no_repo': False,
			'verbose': 1,
			'quiet': 0,
			'config': None
		})

		#Outputs are consolidated from Fitting.
		this.output = {}


	#Configure class defaults.
	#Override of eons.Executor method. See that class for details
	def Configure(this):
		super().Configure()
		this.defaultRepoDirectory = str(Path("/tmp/fittings").resolve())

	#Override eons.UserFunctor Call method to add arguments when called by other python functions.
	def __call__(this, fitting, input={}, **kwargs) :
		this.fittingName = fitting
		this.input = input
		super().__call__(**kwargs)
		return this.output #set in UserFunction()

	#Disable argument parsing, since this will not be called from the command line.
	def ParseArgs(this):
		pass

	#Override of eons.Executor method. See that class for details
	def Function(this):
		super().Function()
		fitting = this.GetRegistered(this.fittingName, "fitting")
		fitting(executor=this, input=this.input, **this.kwargs)
		this.output = fitting.output


class Fitting(eons.Functor):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)

		this.enableRollback = False

		# Populate this with anything you want to return.
		this.output = {}


	# Run inputs through *this fitting!
	# i.e. do work.
	# Override this or die.
	def Run(this):
		pass


	# Override this to perform whatever success checks are necessary.
	def DidRunSucceed(this):
		return True


	# API compatibility shim
	def DidFunctionSucceed(this):
		return this.DidRunSucceed()


	# Hook for any pre-run configuration
	def PreRun(this):
		pass


	# Hook for any post-run configuration
	def PostRun(this):
		pass


	# Override of eons.UserFunctor method. See that class for details.
	def ParseInitialArgs(this):
		super().ParseInitialArgs()
		this.input = this.kwargs.pop('input')


	# Override of eons.Functor method. See that class for details
	def Function(this):
		this.PreRun()

		logging.debug(f"<---- Running {this.name} ---->")
		this.Run()
		logging.debug(f">---- Done running {this.name} ----<")

		this.PostRun()

	def fetch_location_input(this, varName, default, fetchFrom, attempted):
		if (varName in this.input.keys()):
			return this.input[varName], True
		return default, False
