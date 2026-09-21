# Open Humanizer

A free, open-source, local-first editorial quality checker for natural English writing.

Open Humanizer applies a public editorial rule set to English writing. It flags patterns and explains what to review. It does not generate a false certificate that text is human-written and does not promise to bypass AI detectors.

## What it checks

- promotional and inflated language;
- vague attribution;
- unsupported analytical `-ing` phrases;
- formulaic contrast structures;
- placeholders;
- internal AI or tool markers;
- assistant-to-user language;
- em dashes;
- basic evidence signals such as dates and numbers.

## Privacy

The CLI and web UI run locally. No API key is required. No text is sent to a third party.

## Run the CLI

From this repository:

```text
python -m humanizer.cli path/to/report.md
python -m humanizer.cli path/to/report.md --json
```

Or pipe text:

```text
printf "Experts say this is a groundbreaking solution." | python -m humanizer.cli
```

## Run the local web UI

```text
python -m humanizer.web
```

Open <http://127.0.0.1:8788>.

## Use the rules in another project

The rule contracts are in [`rules/writing_rules.json`](rules/writing_rules.json) and [`rules/french_writing_rules.json`](rules/french_writing_rules.json). The source checklists are in [`docs/ANTI_AI_WRITING_SIGNS.md`](docs/ANTI_AI_WRITING_SIGNS.md) and [`docs/FRENCH_WRITING_RULES.md`](docs/FRENCH_WRITING_RULES.md). For website context, see [navidaitoolbox.com](https://navidaitoolbox.com).

## Test

```text
python -m unittest discover -s tests -v
```

## License

MIT. See [`LICENSE`](LICENSE).
