# Lessons

- When adding a new section page, match the established section styling first before introducing any new visual treatment.
- Do not add extra controls or navigation actions unless the spec or the user explicitly asks for them.
- Apply the same consistency rule to section subpages too; if `vocabulary/*` mirrors `grammar/*`, match the corresponding page style unless told otherwise.
- On topic pages, do not keep or add return/navigation buttons unless the user explicitly wants them.
- Do not add extra metadata or helper copy to vocabulary topic pages unless the spec explicitly asks for it.
- For exercises pages, implement the full interaction model from the spec, not just a static render of exercise data.
- Verify actual field names in the current JSON before adding compatibility fallbacks; do not keep stale aliases like `idem_id` when the data model uses `item_id`.
- When local static serving does not send cache-control headers, force fresh fetches for JSON-driven pages after schema or data changes to avoid stale browser data.
- For “Complete” actions on drill/exercises pages, use history-based return behavior rather than a normal forward link, or the browser Back button will reopen the exercises page.
