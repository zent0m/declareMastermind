from behave import given, when, then
from declareMastermind import *

@given('the codemaker sets the code "{code}"')
def stepDef(context, code):
    context.code = Pattern.parse(code)
    assert context.code is not None, f"Invalid code: {code}"

@when('the codebreaker guesses "{guess}"')
def stepDef(context, guess):
    context.guess = Pattern.parse(guess)
    context.feedback = Feedback.giveFeedback(context.code, context.guess) if context.guess else None

@then('the codebreaker should win')
def stepDef(context):
    assert context.guess == context.code, "The codebreaker won."

@then('the codemaker should win')
def stepDef(context):
    assert context.guess != context.code, "The codemaker won."

@when('the codebreaker has 10 incorrect attempts')
def stepDef(context):
    context.attempts = 10

@then('the feedback should be "{expected_feedback}"')
def stepDef(context, expected_feedback):
    feedback_str = ', '.join([str(fb) for fb in context.feedback])
    assert feedback_str == expected_feedback, f"Expected {expected_feedback}, got {feedback_str}"

@then('the guess should be invalid')
def stepDef(context):
    assert context.guess is None, "Guess was invalid."

@given('the campaign mode is started')
def stepDef(context):
    context.campaign_codes = CampaignCodes
    context.current_level = 0

@when('the codebreaker completes all levels')
def stepDef(context):
    context.won_campaign = True
    for code in context.campaign_codes:
        context.code = code
        context.guess = code
        context.won_campaign = context.won_campaign and (context.guess == context.code)

@when('the codebreaker fails a level')
def stepDef(context):
    context.code = context.campaign_codes[0]
    context.guess = Pattern.parse("bbbb")
    context.won_campaign = True if context.guess==context.code else False

@then('the codebreaker should win the campaign')
def stepDef(context):
    assert context.won_campaign, "Codebreaker won the campaign."

@then('the codebreaker should lose the campaign')
def stepDef(context):
    assert not context.won_campaign, "Codebreaker lost the campaign."