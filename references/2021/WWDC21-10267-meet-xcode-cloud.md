---
framework: Xcode
title: "Meet Xcode Cloud"
session: WWDC21-10267
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

# Meet Xcode Cloud (WWDC21)

Xcode Cloud is Apple's CI/CD service integrated into Xcode and App Store Connect. It builds, tests, and distributes apps automatically on Apple silicon cloud infrastructure.

## Key APIs

- **Workflow** — a named CI/CD pipeline with a start condition, environment, actions, and post-actions
- **Start condition** — what triggers the workflow: branch push, pull request, tag, or scheduled time
- **Action** — a step in the workflow: Build, Test, Analyse, Archive
- **Post-action** — what to do after all actions pass: notify via email/Slack, deploy to TestFlight, deploy to App Store Connect

## Quick start

```
Xcode → Product → Xcode Cloud → Create Workflow

Workflow settings:
  Name: "PR Checks"
  Start Conditions:
    - Pull Request Changes → Branch: feature/**
  Environment:
    Xcode: Latest Release
    macOS: Latest Release
  Actions:
    1. Build (all platforms)
    2. Test
       - Test plan: MyApp.xctestplan
       - Devices: iPhone 15, iPad Pro
       - Parallel testing: Enabled
  Post-Actions:
    - Notify: Slack webhook
```

## Script hooks

Xcode Cloud runs shell scripts at defined points in the build; place them in `ci_scripts/`:

```
ci_scripts/
  ci_post_clone.sh      # runs after cloning, before building
  ci_pre_xcodebuild.sh  # runs before xcodebuild
  ci_post_xcodebuild.sh # runs after xcodebuild
```

```bash
#!/bin/sh
# ci_scripts/ci_post_clone.sh
# Install SwiftPM dependencies or set up environment
set -e
echo "Running post-clone script"
# Example: install a CLI tool
brew install swiftlint
```

## Test parallelization

```
In workflow Test action:
  Parallel Testing: ON
  → Xcode Cloud distributes test suites across multiple simulators
  → All simulators run concurrently; results merged
  → Test result bundles downloadable from Xcode / App Store Connect
```

## App Store Connect integration

- Workflows configured in Xcode are synced to App Store Connect
- Build artifacts and test results are visible in App Store Connect → Xcode Cloud
- Webhooks can notify external systems when a build completes

```
App Store Connect → Apps → [Your App] → Xcode Cloud
  → Builds list with status, duration, test results
  → Download .xcresult bundles
  → Webhook URL: configured per workflow for Slack, GitHub, Jira, etc.
```

## Common patterns

```
Post-Action: TestFlight Internal Testing
  → Automatically uploads archive to TestFlight
  → Distributes to internal group on successful build
  → Requires: app record in App Store Connect, provisioning profiles
```

## Environment variables

```bash
# Built-in variables available in ci_scripts/
$CI_WORKSPACE          # root of the cloned repo
$CI_DERIVED_DATA_PATH  # derived data directory
$CI_PRODUCT_PLATFORM   # e.g., "iOS"
$CI_XCODE_SCHEME       # the scheme being built
$CI_BUILD_NUMBER       # incrementing build number
$CI_BRANCH             # git branch name
$CI_PULL_REQUEST_NUMBER# PR number, if triggered by a PR
```

## Gotchas

- Xcode Cloud requires Xcode 13+ and an active Apple Developer Program membership
- Source control: supports GitHub, Bitbucket, GitLab (connected via App Store Connect)
- Build infrastructure: Apple silicon (M1) cloud machines
- Free tier included; additional compute hours available via paid plans
- Webhooks support standard HTTP POST with JSON payload; no SDK required on the receiving end
