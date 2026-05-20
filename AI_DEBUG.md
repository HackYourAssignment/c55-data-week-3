# AI Debugging Report

While building your pipeline you will run into at least one bug.
Document the debugging session below. If everything worked first try, introduce a bug intentionally and debug it.

---

## The Error

<!-- Paste the full Python traceback here. Include the error type, message, and the lines that caused it. -->

Traceback (most recent call last):
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\knack/cli.py", line 233, in invoke
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\azure/cli/core/commands/__init__.py", line 677, in execute
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\azure/cli/core/commands/__init__.py", line 820, in _run_jobs_serially
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\azure/cli/core/commands/__init__.py", line 789, in _run_job
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\azure/cli/core/commands/__init__.py", line 335, in __call__
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\azure/cli/core/commands/command_operation.py", line 120, in handler
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\azure/cli/command_modules/profile/custom.py", line 215, in login
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\azure/cli/core/_profile.py", line 177, in login
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\azure/cli/core/auth/identity.py", line 175, in login_with_device_code
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\azure/cli/core/auth/identity.py", line 125, in _msal_app
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\msal/application.py", line 2090, in __init__
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\msal/application.py", line 649, in __init__
  File "D:\a\_work\1\s\build_scripts\windows\artifacts\cli\Lib\site-packages\msal/authority.py", line 115, in __init__
ValueError: Unable to get authority configuration for https://login.microsoftonline.com/07a14c4e-d88f-42f7-83b3-13af7e57ff3d. Authority would typically be in a format of https://login.microsoftonline.com/your_tenant or https://tenant_name.ciamlogin.com or https://tenant_name.b2clogin.com/tenant.onmicrosoft.com/policy.  Also please double check your tenant name or GUID is correct.
To check existing issues, please visit: https://github.com/Azure/azure-cli/issues
Please run 'az login' to setup account.
Please run 'az login' to setup account.


## The Prompt

<!-- Paste the exact message you sent to the LLM (ChatGPT, Claude, etc.).
     Include: the error, the relevant code snippet, and what you asked the AI to help with. -->

     How to solve this?

## The Solution

<!-- What did the AI suggest?
     Did you apply the suggestion as-is, or did you need to adapt it? Explain what changed. -->

     The error says the tenant ID is wrong. There is a typo in it!

## Reflection

<!-- Did you understand *why* the code was broken before you got the AI's answer?
     After the fix: do you understand why it works now?
     What would you do differently next time you hit this type of error? -->




     I have two accounts under my email and they seem to cause conflict when i try to login
