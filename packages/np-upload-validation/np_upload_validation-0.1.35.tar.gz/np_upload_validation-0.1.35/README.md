# np-upload-validation

AWS upload validation

[![PyPI](https://img.shields.io/pypi/v/np-upload-validation.svg?label=PyPI&color=blue)](https://pypi.org/project/np-upload-validation/)
[![Python version](https://img.shields.io/pypi/pyversions/np-upload-validation)](https://pypi.org/project/np-upload-validation/)

[![Coverage](https://img.shields.io/codecov/c/github/AllenInstitute/np-upload-validation?logo=codecov)](https://app.codecov.io/github/AllenInstitute/np-upload-validation)
[![CI/CD](https://img.shields.io/github/actions/workflow/status/AllenInstitute/np-upload-validation/publish.yml?label=CI/CD&logo=github)](https://github.com/AllenInstitute/np-upload-validation/actions/workflows/publish.yml)
[![GitHub issues](https://img.shields.io/github/issues/AllenInstitute/np-upload-validation?logo=github)](https://github.com/AllenInstitute/np-upload-validation/issues)

# Usage

## Install

```bash
pip install np-upload-validation
```

## Python
```python
import np_upload_validation
```

## Command-line

```bash
np-upload-validation --help
```

# Deployment

Due to limitations on user accounts for the onprem HPC, this package needs to be installed into a singularity container that is then used by a "Job" submitted to the onprem HPC. A docker container would have been preferable but required more permissions than were available at the time of writing this document (11-20-24).

## Deploying to hpc

Requires the following environment variables to be present:

- `HPC_SIF_LOCATION`
- `HPC_JOBS_DIR`
- `HPC_JOB_LOGS_DIR`
- `OUTPUT_DIR`

From the build machine.

```bash
make deploy-hpc
```

If host and build machines are configured you also do it remotely (ssh)

```bash
make remote-deploy-hpc
```

## Deploying to windows task scheduler

Automated deployment to windows task scheduler (may require admin access).
- create a directory at: `NP_UPLOAD_VALIDATION_WORKING_DIR`
- create a directory at: `NP_UPLOAD_VALIDATION_OUTPUT_DIR` for validation outputs and logs
- validates against directory: `NP_UPLOAD_VALIDATION_TARGET_DIR`

Default values are

- `NP_UPLOAD_VALIDATION_WORKING_DIR`: "%USERPROFILE%\Desktop\np-upload-validation"
- `NP_UPLOAD_VALIDATION_OUTPUT_DIR`: "//allen/programs/mindscope/workgroups/dynamicrouting/PilotEphys/np-upload-validation/"
- `NP_UPLOAD_VALIDATION_TARGET_DIR`: "//allen/programs/mindscope/workgroups/dynamicrouting/PilotEphys/Task 2 pilot/"

Requires the following variables used by npc-lims, npc-sessions to be present in a .env file in `NP_UPLOAD_VALIDATION_WORKING_DIR`

- CODE_OCEAN_API_TOKEN
- CODE_OCEAN_DOMAIN (https://codeocean.allenneuraldynamics.org)
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION (us-west-2)

```bash
init && init-scheduled
```

# Testing

## Unit tests

```bash
make test
```

## Onprem integration tests

```bash
make test-onprem
```

# Development
See instructions in https://github.com/AllenInstitute/np-upload-validation/CONTRIBUTING.md and the original template: https://github.com/AllenInstitute/copier-pdm-npc/blob/main/README.md

## Debugging version divergences

```bash
pdm bumpver
```