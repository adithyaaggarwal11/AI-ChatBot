from knowledge_engine import get_similarity, GoalMap


c1 = ["Verify the customer’s current billing address",
      "Verify the customer’s current mailing address",
      "Verify that the customer is requesting a change to their billing address only or also their mailing address",
      "Update their billing address",
      "If the customer would like to update their mailing address as well, update their mailing address",
      "Confirm the customer’s new billing address and, if applicable, their mailing address after the change"]

test_sentences = ["This is my billing address",
                  "I do not need to change my mailing address"
                  ]

g = GoalMap(c1)
for x in test_sentences:
    print(g.check(x))
