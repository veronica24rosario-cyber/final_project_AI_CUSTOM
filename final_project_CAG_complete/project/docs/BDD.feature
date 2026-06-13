Feature: Context Augmented Generation

  Scenario: Remember user name
    Given a user starts a conversation
    When the user says "My name is Julio"
    And later asks "What is my name?"
    Then the system should answer "Your name is Julio"

  Scenario: Remember preferred technology
    Given a user says "I work with Python"
    When the user later asks "What technology do I use?"
    Then the system should answer "Python"

  Scenario: Save and retrieve context via API
    Given a user "ana" exists in the system
    When a POST /api/context is sent with key "preferred_style" and value "explicaciones con analogias"
    Then the response status should be 201
    And the response body should contain saved: true

  Scenario: Context influences answer
    Given user "luis" has context audience = "explicar como principiante"
    When a POST /api/ask is sent with question "Que es CAG?"
    Then the response body answer should contain "principiante"
    And the response body context_used should contain "audience"
