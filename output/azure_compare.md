# Azure API Comparison

Fill in each section below (2-3 sentences each) after completing the Task 7 steps.

## Auth

Azure API needs authentication with a Bearer token. I got this token from Azure CLI after login. Open-Meteo was easier, because it did not need any token or API key.

## Schema verbosity

Azure response looks more complicated and more nested. Each resource group has fields like id, name, type, location and properties. Open-Meteo response was simpler for me, because the weather data was mostly arrays inside hourly.

## api-version in the URL

Azure needs api-version in the URL, for example `api-version=2024-03-01`. I think this is because Azure has many versions of the same API and wants the client to say which one to use. If I remove it, the request will fail because Azure does not know what API version I want.
