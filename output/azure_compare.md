# Azure API Comparison

Fill in each section below (2-3 sentences each) after completing the Task 7 steps.

## Auth

<!-- Fill in here -->
Azure APIs authenticate using a Bearer token obtained via Azure Active Directory (Azure AD), while Open-Meteo is a public API that does not require authentication or tokens.


## Schema verbosity

<!-- Fill in here -->
 The Azure Resource Manager response is highly nested with multiple objects, metadata, and hierarchical structures, whereas Open-Meteo returns flat, column-oriented arrays that are easier to read and process.

## api-version in the URL

<!-- Fill in here -->
Azure requires an explicit `api-version` in the request URL to ensure backward compatibility, and omitting it would cause the request to fail because ARM APIs are versioned and strictly controlled.
