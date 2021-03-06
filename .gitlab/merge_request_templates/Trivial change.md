## What does this MR do?
<!--
Briefly describe what this MR is about.
Examples:
 Adds new document type: MyNewDocumentType
 Fixes js error in <some functionality>
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
- [ ] Prerequisites:
    - [ ] The change is contained within *not more than three commits* which reference the ticket ID (eg. `[#12345] Implement featureX in Y`)
    - [ ] The MR contains a single minor bugfix, documentation correction or trivial feature
    - [ ] Screenshots of any UI changes have been added to the MR description
- [ ] Workflow:
    - [ ] The title of this MR contains the relevant ticket no., formatted like `[#12345]`
    - [ ] The corresponding Redmine ticket has been set to `Needs review` and assigned to the principal reviewer
    - [ ] The MR has been labelled with either ~bug (if it is a bugfix) or ~enhancement (if it is a feature)

## On Merge
- [ ] Update redmine:
    - [ ] Status (to `QA (int)` or `Done`)
    - [ ] Version (upcoming release)
    - [ ] Assignee (if relevant)
