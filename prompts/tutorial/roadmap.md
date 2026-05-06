# Content roadmap section page

The roadmap page should show roadmap that consist of steps.
The list of roadmap steps located in `content\roadmap\steps.json` file.
On click of step the user should be forwarded on step page with content that described in `roadmap_step.md`.
Each step should have a checkbox. When user completes the step he will press it. 
The value for checkboxes should be stored in local storage in browser with the key of `id` of step.
When the step marked as done, it goes down the list.