# Verification-Driven Implementation

## Core Principle
**Implementation is not complete until verification proves it works from the user's perspective.**

## Verification Framework by Work Type

### Technical Claims & References
1. Source Verification: Backed by official docs?
2. WebFetch Before Writing: Verified BEFORE stating as fact?
3. Direct Quotation: Exact source quotes?
4. Link Verification: Every hyperlink works?
5. Authority Check: Most authoritative source?

### Code Implementation
1. Compile/Parse: Runs without errors?
2. Unit Test: Tests pass?
3. Integration: Components work together?
4. User Journey: Complete intended workflow?
5. Regression: Nothing previously working broke?

### Documentation & Content
1. Deployment: Successfully deployed?
2. Link Testing: **CLICK EVERY LINK**
3. Content Rendering: Formatting correct?
4. Navigation: Users can find content?
5. Cross-Platform: Works mobile/desktop?

### Configuration/Infrastructure
1. Apply: Changes applied without errors?
2. Functionality: Intended functionality works?
3. Workflow: Users complete normal workflows?
4. Rollback: Can revert safely?
5. Integration: Other tools still work?

## Verification Methodology

### Test-Driven Verification
- Before: Define success
- During: Build verification into each step
- After: Prove success through testing

### User Perspective Testing
- Never assume: Test user's actual experience
- Click every link: Don't trust, verify
- Follow user journeys: Complete workflows end-to-end
- Test edge cases: What happens when things go wrong?

### Systematic Checklists
- Pre: What will we verify?
- During: Check progress at each step
- Post: Complete verification checklist
- Documentation: Record what/how verified

## Agent Integration

Every agent should verify:
```yaml
immediate_verification:
  - Test specific functionality just implemented
  - Verify no existing functionality broke
user_experience_verification:
  - Test from end-user perspective
  - Follow complete user workflows
integration_verification:
  - Verify system interactions
  - Check dependencies still function
```

## Common Failures

### What NOT to Do
❌ Make claims without WebFetch verification
❌ Assume library features without docs
❌ Skip manual testing ("code looks right")
❌ Trust links without clicking
❌ Skip regression testing

### What TO Do
✅ WebFetch sources BEFORE claims
✅ Quote directly from documentation
✅ Hyperlink EVERY reference
✅ Test from user perspective
✅ Document verification steps

## Verification Tools

**Automated:** Unit/integration tests, link checkers, performance monitoring, automated journey tests

**Manual:** Click-through testing, cross-browser/device, performance under realistic conditions, usability testing

## Making Verification Habitual

1. **Built into Workflow:** Required step, not optional
2. **Agent Enhancement:** Verification behaviors built-in
3. **Memory System:** Store patterns, checklists, post-mortems

---

**Key Principle:** Implementation without verification is incomplete work.
