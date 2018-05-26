# logdna_lambda_cloudwatch
Post cloudwatch logs to LogDNA via lambda function

This is a replacement function for the one recommended by LogDNA at this link:
https://docs.logdna.com/docs/cloudwatch

This modules utilizes python "requests" module instead of "socket"

To set up you can follow all the steps in the link above except...
- Use Code entry type: "Edit Code Inline"
- Copy the code form handler.js
- Set the handler function to handler.lambda_handler

If you're using serverless to deploy your lambda functions and want to stream their logs I recommend using the extension serverless-log-forwarding to automatically set up your lambdas to send their logs to this function then logdna
