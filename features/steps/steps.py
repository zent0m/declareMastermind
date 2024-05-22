from behave import given, when, then
from declareMastermind import *

#These are all examples from our friend at the moment. These will be changed according to the
#Gherkin specs we defined in our document. 

@given('we have a calculator')
def step_impl(context):
    pass  # This step doesn't need to do anything

@when('we add {a:d} and {b:d}')
def step_impl(context, a, b):
    context.result = add(a, b)

@then('the result should be {expected:d}')
def step_impl(context, expected):
    assert context.result == expected, f"Expected {expected}, but got {context.result}"