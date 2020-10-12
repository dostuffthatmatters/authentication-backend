[![Maintainability](https://api.codeclimate.com/v1/badges/87b6138295fbf87fab46/maintainability)](https://codeclimate.com/github/fastsurvey/authentication-backend/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/87b6138295fbf87fab46/test_coverage)](https://codeclimate.com/github/fastsurvey/authentication-backend/test_coverage)

# Authentication API

We actually wanted to use an OAuth2 authentication service rather than build these features ourselves - yet again.

However most of the tools we have stumbled accross had on or more of the following issues:

-   Very narrow documentation only suited for specific usecases
-   Rather shitty documentation ...
-   Deep integration with the other services of that provider -> strong dependence on that company
-   Somewhat untrustworthy regarding data security

That is why we are reinventing the wheel yet again :)

Feel free to reuse it in your project if you also don't want to copy and paste the same functionality with every new project.
