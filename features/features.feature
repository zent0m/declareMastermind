Feature: Mastermind

  Scenario: Codebreaker wins
    Given the codemaker sets the code "rgby"
    When the codebreaker guesses "rgby"
    Then the codebreaker should win

  Scenario: Codebreaker loses
    Given the codemaker sets the code "rgby"
    When the codebreaker guesses "bbbb"
    And the codebreaker has 10 incorrect attempts
    Then the codemaker should win

  Scenario: Provide feedback with correct positions
    Given the codemaker sets the code "rgby"
    When the codebreaker guesses "rgby"
    Then the feedback should be "Black, Black, Black, Black"

  Scenario: Provide feedback with incorrect positions
    Given the codemaker sets the code "rgby"
    When the codebreaker guesses "yrgb"
    Then the feedback should be "White, White, White, White"

  Scenario: Provide feedback with no correct colors
    Given the codemaker sets the code "rgby"
    When the codebreaker guesses "oooo"
    Then the feedback should be "Null, Null, Null, Null"

  Scenario: Provide mixed feedback
    Given the codemaker sets the code "rgby"
    When the codebreaker guesses "rbgo"
    Then the feedback should be "Black, White, White, Null"

  Scenario: Handle invalid input length
    Given the codemaker sets the code "rgby"
    When the codebreaker guesses "rg"
    Then the guess should be invalid

  Scenario: Handle invalid input characters
    Given the codemaker sets the code "rgby"
    When the codebreaker guesses "abcd"
    Then the guess should be invalid

  Scenario: Campaign mode progression
    Given the campaign mode is started
    When the codebreaker completes all levels
    Then the codebreaker should win the campaign

  Scenario: Campaign mode failure
    Given the campaign mode is started
    When the codebreaker fails a level
    Then the codebreaker should lose the campaign