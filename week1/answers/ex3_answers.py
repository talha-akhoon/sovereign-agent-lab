"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking                                                                                               
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                 
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                        
2026-04-15 21:48:46 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user is confirming a booking, and the current flow is confirm_booking. The AI has already asked for the number of guests, which the user provided as 160. Then the AI asked about vegan meals, and the user says "about 50 need vegan".

First, I need to check the available flows and slots. The confirm_booking flow has slots for guest_count, vegan_count, and deposit_amount_gbp. The user is providing the vegan_count here. The value mentioned is "about 50". The slot expects a float, so I should convert "about 50" to a numerical value. Since it\'s approximate, maybe 50.0? But the user said "about 50", so maybe it\'s better to take it as 50.0 unless there\'s a need to handle approximations differently. The instructions say to extract text exactly as provided, but the slot type is float. Hmm. Wait, the example shows "160 guests" was set as 160.0. So even if the user says "about 50", the exact value to set is 50.0? Or should it be "about 50"? The slot\'s value is supposed to be a float, so probably 50.0. But the user might mean approximately, but the system might need an exact number. However, the user provided "about 50", so maybe the exact value is 50. The instruction says to extract text exactly as the user provided it, but for numerical slots, we need to convert to the correct type. So "about 50" would be parsed as 50.0? Or is there a conflict here?

Wait, the general instructions say: "Extract text exactly as the user provided it." But the slot\'s type is float. So perhaps the value should be 50.0, even if the user said "about 50". Because the slot expects a numerical value. The example given in the slot extraction shows that "send money to John" sets the recipient as John, and "set up a recurrent payment" sets transfer_type and transfer_timing_type. So for numerical values, even if approximate, we take the number. So "about 50" would be 50.0. Therefore, set slot vegan_count to 50.0.

So the action would be set slot vegan_count 50.0' message='No commands were parsed from the LLM actions.'
2026-04-15 21:48:46 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  about 50                                                                                                                   
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                               
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->                       
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking                                                                                               

How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                 

And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                        

2026-04-15 22:18:48 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user said, "about 50 need vegan." The current flow is confirm_booking, and the current step is asking for vegan_count. The guest_count is already set to 160. So the user is providing the number of vegan guests here.

First, I need to set the vegan_count slot. The user mentioned "about 50," so I should take that as the value. The slot expects a float, so even though it\'s "about," the value should be 50.0. So the action would be set slot vegan_count 50.0.

Next, after setting the slot, I need to check if there are more steps in the confirm_booking flow. The slots that are part of this flow are guest_count, vegan_count, and deposit_amount_gbp. The user hasn\'t mentioned the deposit amount yet. So the next step would be to ask for deposit_amount_gbp. Therefore, the AI should prompt the user for the deposit amount. But according to the available actions, the next action here is to start the flow or set the slot. Wait, no—the AI\'s job here is to generate the action list based on the user\'s input. Since the user provided the vegan_count, the AI should set that slot and then proceed to the next required slot in the flow, which is deposit_amount_gbp. However, the current step in the flow is already requesting vegan_count, so after setting that, the next step would be to ask for the deposit amount. But the available actions don\'t include asking a question directly. Instead, the AI would trigger the next step in the flow by setting the slot. Since the flow is handled by the system, once the vegan_count is set, the system would automatically move to the next required slot, which is deposit_amount_gbp. Therefore, the action here is to set the vegan_count slot. There\'s no need to start another flow because the confirm_booking flow is already active. So the only action needed here is setting the vegan_count to 50.0. Wait, but the example in the slot extraction shows that when a user provides a value, you set the slot and start the flow if necessary. In this case, the flow is already started (confirm_booking is active), so the only action is setting the slot. The next step would be for the system to prompt for the deposit amount. So the correct action here is to set the vegan_count to 50.0.' message='No commands were parsed from the LLM actions.'
2026-04-15 22:18:48 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  about 50                                                                                                                   

What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit        

I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->                                                                                                                             
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £500 exceeds the organiser's authorised limit of £300"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking                                                                                               

How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                 

And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?                                                                                  
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->                  
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
The agent correctly handled the out of scope request by informing the user that it can only help with confirming tonight's venue booking and suggested they contact the event organiser directly.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Rasa CALM handled the out-of-scope request with a fixed, predefined response and
then tried to return the conversation to the booking flow. LangGraph was more
flexible and conversational: it explained that train times were outside its
available tools and suggested other sources. CALM felt safer and more controlled,
while LangGraph felt more generally helpful.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I tested the cutoff guard by temporarily making the condition always True:
```python
if True:
    return escalate("it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline")
```
Then I ran a conversation and verified that the agent escalated as expected.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
CALM simplifies the assistant because the LLM now handles flow triggering and slot extraction from natural language, which old Rasa needed intent examples, rules, and regex-based form validation to do. The trade-off is that extraction is less deterministic, so the old approach can feel more predictable. Python still needs to enforce business rules, because limits like deposit caps and escalation conditions should be checked deterministically, not left to model judgment.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
The extra setup buys a much more controlled assistant. CALM cannot improvise arbitrary multi-step tool use like the LangGraph agent, and it cannot call tools outside the flows and actions you explicitly define. For the booking confirmation use case, that is mostly a feature rather than a limitation, because the goal is consistency, auditability, and safe enforcement of business rules, not open-ended problem solving. LangGraph was more flexible, but CALM is better suited to a narrow, high-stakes workflow.
"""
