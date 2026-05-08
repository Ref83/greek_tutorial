# Content reading tests page

The page should consist of 2 panels.
The top panel should show the statistic how many tests user done and how many of it was with error.
On the top panel should be the button complete that leads to the previous page.
The main panel should show the current exercise.
The source of exercises is JSON files with names like `content/reading/{id}/reading_<N>.json`
The page should show one exercise in a time.
When user completed exercise it should be able to go to the next by clicking the button "Next"
The type of exercise should be mentioned in the panel

## Type of tests
Tests could be the following types.

### True/False

**View:**
- the type of the exercise should be shown
- There should be 2 buttons `True` and `False`.
- When user click the button the app should chack it with `answer` field

```json
{
  "type": "true_false",
  "statement": "...",
  "answer": "true"
}
```

### Matching

**View:**
- the type of the exercise should be shown
- There should be 2 columns with `beginnings` and `endings` User have to match them.
- The system should check matchings of the user with `answers` 

```json
{
  "type": "matching",
  "beginnings": [
    { "text": "..." }
  ],
  "endings": [
    { "text": "..." },
    { "text": "..." }
  ],
  "answers": { "0": 3, "1": 7 }
}
```

### Multiple Choice

**View:**
- the type of the exercise should be shown
- `question` should be shown on the panel 
- `options` should be in the panel
- When user check some options the script should check it with `answer` 

```json
{
  "type": "multiple_choice",
  "question": "...",
  "options": { "a": "...", "b": "...", "c": "..." },
  "answer": "b"
}
```