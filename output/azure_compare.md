# Azure API Comparison

Fill in each section below (2-3 sentences each) after completing the Task 7 steps.

## Auth

Azure uses Bearer token authentication. I had to log in with Azure CLI and send an access token in the `Authorization` header.  I can call the Open-Meteo API directly without an API key or Bearer token.

## Schema verbosity

The Azure response is more verbose and nested than the Open-Meteo response. Azure returns resource groups with fields such as `id`, `name`, `type`, `location`, and `properties`.
Open-Meteo returns weather data in a flatter columnar structure under the `hourly` key. For example, it gives separate arrays for `time`, `temperature_2m`, and `relative_humidity_2m`.

## api-version in the URL

Azure requires the `api-version` parameter in the URL to specify which version of the API should be used. This makes the API contract explicit and helps Azure keep compatibility between different API versions.
If the `api-version` parameter is missing, Azure may reject the request because it does not know which API schema to apply.
