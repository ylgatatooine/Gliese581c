# 🧑‍💻 Developer Co-Pilot Prompt Playbook

> **Purpose**: Use LLMs to *enhance* your workflow, not replace it. Pair your engineering skills with generative AI to build, test, debug, and ship better software.

## 📄 Table of Contents

1. [🚦 Test-Driven Development (TDD)](#-1-test-driven-development-tdd)
2. [🪵 Observability-Driven Debugging](#-2-observability-driven-debugging)
3. [🧩 Chain-of-Thought Prompting](#-3-chain-of-thought-cot)
4. [🗃️ Git & GitHub + MCP](#-4-git--github--mcp)
5. [🧠 Meta Prompt Frameworks](#-5-meta-prompt-frameworks)
6. [🎯 Few-Shot Prompting](#-6-few-shot-prompting)
7. [⚖️ LLM as a Judge](#-7-llm-as-a-judge)
8. [🛠️ Putting It All Together](#️-putting-it-all-together)

---

## 🚦 1. Test-Driven Development (TDD)

**Why?**  
- Forces clarity on expected behavior  
- Prevents over-engineering  
- Helps you validate edge cases up front  

**Prompt Templates**  
- “Write unit tests for a function that [describe function behavior].”  
- “Suggest edge cases and boundary tests for this [describe feature].”  
- “Given these tests, what code would satisfy them?”  
- “Let’s do test-driven. I’ll give requirements, you write the tests first, then we’ll iterate.”  

**Example**  

```python
# Prompt to LLM:
"Write tests for a function that validates credit card numbers."

# LLM output:
def test_valid_visa():
    assert validate_card("4111111111111111") == True

def test_invalid_length():
    assert validate_card("1234") == False

def test_non_numeric():
    assert validate_card("abcdabcdabcdabcd") == False
````

---

## 🪵 2. Observability-Driven Debugging

**Why?**

* Many bugs are runtime-only
* Logging helps track dynamic state
* Faster root-cause analysis

**Prompt Templates**

* “Add logs to show inputs and outputs for this method.”
* “Please suggest logging to help isolate a bug in this function.”
* “Here’s the log output. What is your hypothesis now?”

**Example**

```python
logger.info(f"Fetching data from URL: {url}")
logger.debug(f"Request params: {params}")
logger.error(f"Exception while fetching data: {e}")
```

---

## 🧩 3. Chain-of-Thought (CoT)

**Why?**

* Forces the LLM to “think out loud”
* You can catch reasoning errors mid-way
* Improves transparency for tricky bugs

**Prompt Templates**

* “Think step by step before suggesting a fix.”
* “Explain each line of this code, then reason about the bug.”
* “Walk through how this algorithm works before rewriting it.”

**Example**

```plaintext
# Prompt:
"Explain why this binary search fails before fixing it."

# LLM:
1) It initializes left = 0 and right = len(arr)
2) Mid is correct
3) But right = len(arr) causes out-of-bounds
Fix: right = len(arr) - 1
```

---

## 🗃️ 4. Git & GitHub + MCP

**Why?**

* Standardizes commits
* Makes PR reviews consistent
* Works well with GitHub agents

**Prompt Templates**

* “Generate a commit message summarizing these changes.”
* “Write a PR description with testing instructions.”
* “What tests should reviewers focus on for this PR?”
* “Suggest a semantic version bump for these changes.”

**Example**

```markdown
# Prompt:
"Write a PR description for this fix."

# LLM:
Title: Fix division-by-zero error in calculate_ratio

Description:
- Adds input validation to avoid division by zero
- Includes test cases for zero denominator

Testing:
- Run `pytest test_math.py`
```

---

## 🧠 5. Meta Prompt Frameworks

**Why?**

* Provides consistent conversations
* Easier to scale prompts across a team
* Reduces “hallucinations”

**Reusable Template**

```plaintext
[You are a senior software assistant. Please follow this framework:]
1) Identify the user’s task
2) Break it into subproblems
3) Clarify any missing details
4) Solve one subproblem at a time
5) Summarize progress and next steps
```

**Example**

```plaintext
# Prompt:
"Use the meta framework to help design a payment gateway."

# LLM:
1) Task: Build a payment gateway API
2) Subproblems:
   - authentication
   - transaction handling
   - currency support
3) Missing details: Supported currencies? Auth methods?
...
```

---

## 🎯 6. Few-Shot Prompting

**Why?**

* Shows the LLM your style
* Anchors behavior to consistent examples
* Prevents random answers

**Prompt Templates**

* “Here are 3 correct patterns and 1 incorrect. Explain why the incorrect one is wrong.”
* “Use these examples to generate the next function.”
* “Rate these implementations from best to worst and explain why.”

**Example**

```plaintext
# Prompt:
"Given these working patterns, generate a new test."

Examples:
input: [2,4,6] => output: even numbers
input: [1,3,5] => output: empty
input: [0,-2] => output: even numbers

# LLM:
input: [7,8,9] => output: [8]
```

---

## ⚖️ 7. LLM as a Judge

**Why?**

* Consistent code reviews
* Surfaces best practices
* Gives objective-style feedback

**Prompt Templates**

* “Act as a senior reviewer and rate this code on clarity, performance, and maintainability.”
* “Which of these two code samples is better, and why?”
* “What best practices are violated here?”

**Example**

```plaintext
# Prompt:
"Review this function for maintainability."

# LLM:
Rating: 6/10

Issues:
- Variable names unclear
- Deeply nested logic
- Missing input validation

Suggestions:
- Rename variables for clarity
- Use guard clauses
```

---

# 🛠️ Putting It All Together

✅ **Write tests first (TDD)**
✅ **Generate code to pass the tests**
✅ **Add logs to improve observability**
✅ **Use chain-of-thought to reason about bugs**
✅ **Employ GitHub workflows to track changes**
✅ **Leverage meta prompt frameworks for repeatable consistency**
✅ **Ask the LLM to judge and review your code**

**Example Combo Prompt**

```plaintext
"Let's write tests for this function, then write code to pass them, then add logs, then review the code with chain-of-thought reasoning. I’ll feed you logs if it fails, and finally help me write the PR and do a review."
```

---
