## What does this MR do?
<!--
Describe what this MR is about AND how to test it.
Include any points that reviewers should pay special attention to.
-->

/assign me <!-- sets current user as assignee -->

<!-- Other recommended quick actions:
/request_review @af @danni
/label ~bug
/label ~enhancement
-->

## Author's checklist
<!--
MRs must be marked as WIP until all checkboxes have been filled.
Checkboxes can be pre-filled before submitting the MR by replacing
[ ] with [x],
-->
- [ ] Workflow:
    - [ ] The title of this MR contains the relevant ticket no., formatted like `[#12345]`
    - [ ] The corresponding Redmine ticket has been set to `Needs review` and assigned to the principal reviewer
    - [ ] The MR has been labelled with either ~bug (if it is a bugfix) or ~enhancement (if it is a feature)
- [ ] Maintainability:
    - [ ] I have rebased/squashed the code into a minimal amount of atomic commits that reference the ticket ID (eg. `[#12345] Implement featureX in Y`)
    - [ ] I have ensured the MR does not introduce indentation or charset issues
    - [ ] I have added or updated documentation where relevant
    - [ ] I have added unit tests or made a conscious decision not to
- [ ] UI (if relevant):
    - [ ] I have added screenshots of the most significant UI changes to the MR description
    - [ ] I have tested all UI changes in:
        - [ ] Firefox
        - [ ] Chrome
        - [ ] Internet Explorer 11
- [ ] QA:
    - [ ] I have tested the feature/bugfix manually
    - [ ] I have added/updated and verified translations where relevant
    - [ ] I have run any new migrations on a non-empty database

## Review checklist

- [ ] The code is understandable, well-structured and sufficiently documented
- [ ] I would be able to test this feature and verify that it's working without further input from the author
- [ ] I have either checked out the code and tested it locally or thoroughly vetted it

## On Merge
- [ ] Update redmine:
    - [ ] Status (to `QA (int)`)
    - [ ] Version (upcoming release)
    - [ ] Assignee (if relevant)