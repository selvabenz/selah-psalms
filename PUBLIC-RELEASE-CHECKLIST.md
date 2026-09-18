# Public-release checklist

Complete every item before changing this repository or its GitHub Pages site to public.

- [ ] Obtain publication permission for the complete ESV text, or remove the English text and every derived English token span from `site/data/`.
- [ ] Confirm that the proposed use complies with TTESV's CC BY-NC terms, including the intended hosting and funding model.
- [ ] Confirm the IRV Tamil redistribution license and required attribution, or remove the Tamil text and every derived Tamil token span from `site/data/`.
- [ ] Review TAHOT attribution and include any additional notices required by the distributed source snapshot.
- [ ] Confirm that no supplied scholarship article, MHTML file, screenshot, PDF, prompt archive, or raw private source file has entered the repository.
- [ ] Decide and add a license for the project-specific code, interface, documentation, and original analysis.
- [ ] Have a qualified reviewer assess the AI-proposed literary judgments and record the state of scholarly review prominently.
- [ ] Run `python scripts/validate_bundle.py` and require a passing result on the exact commit to be published.
- [ ] Confirm the visibility of the GitHub Pages deployment under the account or organization's current GitHub plan.
- [ ] Review the rendered site from the deployed URL on desktop and mobile.

The included Pages workflow requires a manual run so that a push alone cannot publish the bundled Scripture text.
