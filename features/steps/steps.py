from behave import given, when, then
from declareMastermind import *

@given('the codemaker sets the code "{code}"')
def step_impl(context, code):
    context.code = Pattern.parse(code)
    assert context.code is not None, f"Invalid code: {code}"

@when('the codebreaker guesses "{guess}"')
def step_impl(context, guess):
    context.guess = Pattern.parse(guess)
    context.feedback = Feedback.giveFeedback(context.code, context.guess) if context.guess else None

@then('the codebreaker should win')
def step_impl(context):
    assert context.guess == context.code, "Codebreaker did not win."

@then('the codemaker should win')
def step_impl(context):
    assert context.guess != context.code, "Codemaker did not win."

@when('the codebreaker has 10 incorrect attempts')
def step_impl(context):
    context.attempts = 10

@then('the feedback should be "{expected_feedback}"')
def step_impl(context, expected_feedback):
    feedback_str = ', '.join([str(fb) for fb in context.feedback])
    assert feedback_str == expected_feedback, f"Expected {expected_feedback}, but got {feedback_str}"

@then('the guess should be invalid')
def step_impl(context):
    assert context.guess is None, "Guess was expected to be invalid, but it was valid."

@given('the campaign mode is started')
def step_impl(context):
    context.campaign_codes = CampaignCodes
    context.current_level = 0

@when('the codebreaker completes all levels')
def step_impl(context):
    context.won_campaign = True
    for code in context.campaign_codes:
        context.code = code
        context.guess = code  # Simulate correct guesses
        context.won_campaign = context.won_campaign and (context.guess == context.code)

@when('the codebreaker fails a level')
def step_impl(context):
    context.won_campaign = False
    context.code = context.campaign_codes[0]
    context.guess = Pattern.parse("bbbb")  # Simulate incorrect guess

@then('the codebreaker should win the campaign')
def step_impl(context):
    assert context.won_campaign, "Codebreaker did not win the campaign."

@then('the codemaker should win the campaign')
def step_impl(context):
    assert not context.won_campaign, "Codemaker did not win the campaign."