# Prompts

## Session — 2026-06-08

### commit: 5e9b446 Initial prompt v2
```
@_vibe/initial-prompt-v2.md
```

### commit: b30378b Add plan v2 and issue files for Steerer
```
Consider @_vibe/initial-prompt-v2.md but start from scratch and ignore any existing plan and memory files.
```

```
commit
```

### commit: 75ebd60 Implement Issue 1: project scaffolding and development environment
```
implement issue 1
```

### commit: (this commit)
```
From now on, save every prompt to @_vibe/prompts.md and commit along with any changes.
```

### commit: (this commit)
```
Change the health check endpoint to return current date and time
```

### commit: (this commit)
```
I don't see changes in the source code when I run the steerer service in docker compose. Make the docker container use current source code without the need to rebuild.
```

### commit: (this commit)
```
Let's improve makefile. Create a command to perform lint, typecheck and test at once. Don't change current existing commands.
```

### commit: (this commit)
```
Commands format and lint must also check tests directory
```

### commit: 5716902 Tell Claude to ask for permission before committing
```
I've updated CLAUDE.md, here's the new content: @CLAUDE.md . Consider it from now on.
```

### commit: (amend 5716902)
```
I've already commited CLAUDE.md for you. But, please, amend the commit adding the prompts file.
```

### commit: (this commit)
```
Let's get rid of `__pycache__` directories. Change the makefile to avoid their creation.
```

```
Before commiting, remove current `__pycache__` directories.
```

```
commit
```

### commit: (this commit)
```
Let's consider issue 1 completed. Update it with current date and time.
```

```
Don't change its title. Add the completion statement in another paragraph.
```

```
commit
```

### commit: (this commit)
```
/init
```

```
yes
```

### commit: (this commit)
```
Change precommit hook to run only lint and typecheck.
```

```
Also fix any documentation related to this.
```

```
commit
```

### commit: (this commit)
```
Implement issue 2
```

### commit: (this commit)
```
Use explicit Python utcnow() instead of _utcnow() in @src/steerer/routers/routes.py
```

```
Not yet. Use datetime.utcnow
```

```
Do the same to the health check endpoint
```

```
commit
```

### commit: (this commit)
```
Let tests for slugify separate from anything else
```

```
commit
```

### commit: (this commit)
```
I got ModuleNotFoundError: No module named 'piccolo_conf' when trying it from the command line. Please check and fix it.
```

```
commit
```

### commit: (this commit)
```
I sent invalid expiration to POST /routes/ and got status code 422 with this body: {"detail":[{"type":"datetime_from_date_parsing","loc":["body","expiration"],"msg":"Input should be a valid datetime or date, invalid character in year","input":"invalid entry","ctx":{"error":"invalid character in year"}}]}. Change to handle this error returning a friendly error following the pattern for other errors.
```

```
Well done. commit
```

### commit: (this commit)
```
Is there a way to move this validation away from the route?
```

```
yes, go ahead
```

```
commit
```

### commit: (this commit)
```
make name required in POST /routes/. Return error with reason "name is required" when missing.
```

```
commit
```

### commit: (this commit)
```
Remove leading and remaining spaces from name in POST /routes/. Consider empty name as missing. Create tests to assert that.
```

```
commit
```

### commit: (this commit)
```
Consider name always being str in the validator
```

```
commit
```

### commit: (this commit)
```
Add tests to slugify to assert input with only special characters result in empty string
```

```
Add another one to assert a result with valida characters inside, has dashes in both ends stripped
```

```
commit
```

### commit: (this commit)
```
Let's refactor tests for POST /routes/ and remove those related to invalid names because we're already covering it through tests on slugify. Keep only one to illustrate the case and assert the response.
```

```
Good. Also remove test_create_route_strips_name_whitespace
```

```
commit
```

### commit: (this commit)
```
Is it possible to have a computed field in a Pydantic model? If it is, create the field alias in CreateRouteRequest. Handle it as of in create_route.
```

```
Cool. commit
```

### commit: (this commit)
```
Is it possible to move the empty alias validation to CreateRouteRequest? I want the same response.
```

```
Great! commit
```

### commit: (this commit)
```
Now, let's improve validation for destination url. It must follow the same rules as for name.
```

```
commit
```

### commit: (this commit)
```
Remove field alias from error response and log. keep in case of happy path.
```

```
commit
```

### commit: (this commit)
```
Refactor log_action to make error_code with default value of 0. Don't send the error_code in happy path.
```

```
Do not ommit error_code from JSON when it's zero.
```

```
commit
```

### commit: (this commit)
```
Guarantee that an alias has at least one valid character other than a dash in POST /routes/. Otherwise, return error reason "Invalid name".
```

```
Almost there, but not yet. You cannot accept an empty alias or an alias with only a dash.
```

```
Sorry, you were correct. The function to slugify already strips dashes from the result. Reject only empty alias again.
```

```
commit
```
