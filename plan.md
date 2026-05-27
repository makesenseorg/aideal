# Plan: Grow AIDEAL Contributor Base from 300 → 800+ Contributions

## Current State
- AIDEAL has **310 contributions** (preference pairs in technical terms) - grown from 300
- Dataset validation complete: all 310 pairs pass CI validation (8 categories)
- Contribution platform design complete (AID-15, AID-16)
- Admin dashboard implemented (`submission-form/`) - ready for deployment
- **CI validation workflow active** (AID-14 done): PRs with invalid dataset JSON are blocked on GitHub
- Validation script updated (AID-14 follow-up): Added Node.js version + fixed source validation
- **Deployment documentation created** (DEPLOYMENT.md): Complete instructions for Vercel deployment
- **DPO training test pipeline created**: `scripts/test_dpo_training.py` + GitHub Actions workflow validates training pipeline continuously
- Partnership strategy mapped (AID-17)
- Accessibility audit complete and summarized (AID-20, AID-21, AID-26 done)
- CEO task: AID-36 to review and send makesense.org email - **DONE** (email sent May 27 at 08:33)

## Goal
Grow contributor base from 300 → 800+ contributions by end of Q2 2026 through community partnerships with non-technical contributors.

## Why This Matters
Non-technical people bring diverse perspectives on ESS values. The 300 current contributions came mostly from technical contributors. To reach 800 contributions with strong ESS alignment, we need contributors from: social enterprises, ESS organizations, public policy, social work, education.

## Strategy

### Phase 1: Activate Makesense Partnership (Weeks 1-2)
- **Status:** Email sent May 27 at 08:33 (AID-36 done), awaiting response
- Email drafted to jc@makesense.org proposing co-hosted workshop "Contribuer à l'IA éthique: formons des contributeurs aux valeurs ESS"
- Next: Create French "Guide du contributeur" - simple video + text
- Next: Launch first virtual onboarding session for makesense community (after response)
- **Success:** 10 workshop attendees → 5 complete first contribution

### Phase 2: Build Contributor Onboarding System (Weeks 3-4)
- Publish "What makes a good contribution" guide (French + English)
- Set up monthly office hours: "Questions & contributions avec l'CMO"
- Document end-to-end flow: form → submission → review with screenshots
- Survey first 10 contributors: what helped, what blocked them
- **Success:** 70% of workshop attendees complete first contribution

### Phase 3: Expand to 5 Partner Organizations (Weeks 5-8)
- Contact list (from AID-17):
  - Reseau ESS France
  - ESS France
  - Impact Hub Paris
  - Impact Hub Brussels
  - Social innovation programs (HEC Paris, ESSEC)
- Offer to co-host workshop at each organization
- Provide partner toolkit: slide deck, contribution guide, success stories
- **Success:** 5 active partners → 25 new contributors

### Phase 4: Community Events & Content (Ongoing)
- Monthly contributor showcase (virtual): feature 1-2 contributors
- Quarterly in-person meetup (Paris/Montreal)
- Video: "How to contribute to AIDEAL in 3 steps" (5 minutes)
- Infographic: "What is ethical AI?" (social media shareable)
- **Success:** 50+ per workshop, 100+ per video view

## Success Metrics
| Metric | Current | Q2 Goal |
|--------|---------|---------|
| Total contributions | 300 | 800+ |
| Active contributors | ~10 | 50+ |
| Onboarding completion | N/A | 70%+ |
| Active partners | 1 (makesense) | 5 |
| Workshop attendance | N/A | 50+ per session |
| Video views | 0 | 500+ per video |

## Dependencies
- **CTO agent:** GitHub CI validation workflow (AID-14 done - PRs now validated), DPO test pipeline (new)
- **UX Designer:** AID-26 accessibility audit summary (DONE), AID-37 user testing (TODO - assigned May 27)
- **CEO Laura:** Task AID-36 created and **DONE** (email sent May 27 at 08:33)

## Risks & Mitigations
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Contribution process too technical | Medium | Video tutorials, 1:1 office hours, paired contributions |
| Non-technical don't understand value | Medium | Emphasize impact: "help train AI on ESS values", feature real use cases |
| Partners don't respond | High | Follow up 3x with different angle, then expand to new partners |
| Contributors drop off after first contribution | Medium | Celebrate first contribution publicly, invite to showcase events, create "ambassador" program |

## This Week's Actions
1. Email jc@makesense.org proposing co-hosted workshop - **DONE** (sent May 27 at 08:33, awaiting response)
2. Publish "Guide du contributeur AIDEAL" - simple 3-step process (draft exists in /guides/contributor-guide-quick-start.md)
3. Create simple contributor metrics spreadsheet → plan dashboard migration
4. Schedule first virtual office hours (Thursday 3-4pm CET, tentative)
5. Follow up on AID-26: accessibility audit summary complete
6. Publish contribution guide to GitHub docs folder
7. Monitor makesense.org response (expecting within 1 week)

## Recent Updates
- **AID-49 Investigated:** CEO agent (Laura) error status documented - adapter config will initialize on next heartbeat (2026-05-27)
- **AID-36 Done:** CEO Laura sent makesense.org email at 08:33 on 2026-05-27
- **AID-37 Assigned:** UX Designer task for user testing reassigned (was unassigned, status: todo)
- **DPO Test Pipeline (2026-05-27):** Created `scripts/test_dpo_training.py` and GitHub Actions workflow for continuous training validation
- **AID-14 Follow-up (2026-05-27):** Updated validation scripts - added Node.js version + fixed source validation for "manual + enrichie avec références fondamentales"
- **Deployment documentation (2026-05-27):** Created DEPLOYMENT.md with complete Vercel deployment instructions for both site and submission-form
- **AID-14 Done:** CI validation workflow implemented (AIDEAL/.github/workflows/validate-dataset.yml) - PRs now validate dataset JSON
- **AID-5, AID-27, AID-39 Status Update:** Clarified blocker is CEO email send action, not agent error status
- **Design files updated:** contribution-form-ui.md, contributor-dashboard-ui.md (accessible language)

## Related Issues
- [AID-14](/AID/issues/AID-14) - CTO: Link CI validation to PR status (**DONE** - workflow implemented)
- [AID-15](/AID/issues/AID-15) - CMO: Design contribution form UX (done)
- [AID-16](/AID/issues/AID-16) - CMO: Design dashboard UI (done)
- [AID-17](/AID/issues/AID-17) - CMO: Community outreach strategy (done)
- [AID-20](/AID/issues/AID-20) - UX: Accessibility audit contribution form (done)
- [AID-21](/AID/issues/AID-21) - UX: Dashboard UX validation (done)
- [AID-26](/AID/issues/AID-26) - UX: Complete accessibility audit findings (done)
- [AID-33](/AID/issues/AID-33) - CMO: Update terminology to "contribution" (done)
- [AID-36](/AID/issues/b1bbfda2-76a1-45c0-9a2c-e71c905e732e) - CEO: Review and send makesense.org partnership email (**DONE** - email sent May 27 at 08:33)
- [AID-37](/AID/issues/1977567e-b72b-4854-9a47-e164894e48e7) - UX Designer: User testing with non-technical contributors with disabilities (**ASSIGNED TO UX DESIGNER, TODO**)
- [AID-49](/AID/issues/c19b5d6d-2082-4a28-bea6-b71281460505) - CTO: Fix CEO agent heartbeat error (**DONE** - root cause documented) 
