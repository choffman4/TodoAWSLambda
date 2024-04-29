CLS

REM no white-space when setting variables
SET LAMBDA_NAME=Todo2024_PutPerson_ECR
SET IMAGE_NAME=put_person
SET VERSION=1.0
SET ACCTNUM=471112579088
SET REGION=us-west-1
SET ECR_CONTAINER_NAME=sen310todo2024q1
SET LAMBDA_ROLE_NAME=connor-super-lambda-role
SET REQUEST_TYPE=PUT
SET APIHASH=yctz9sw1kc

aws ecr get-login-password --region %REGION% | docker login --username AWS --password-stdin %ACCTNUM%.dkr.ecr.%REGION%.amazonaws.com/%ECR_CONTAINER_NAME%


REM stops and nukes all containers, just to be safe
docker compose down

REM ANY LOCAL DOCKER CLEAN-UP? DON'T REALLY THINK IT'S NECESSARY, DOCKER ALWAYS SEEMS TO REBUILD CLEAN
docker rmi %IMAGE_NAME%:%VERSION%
docker rmi %ACCTNUM%.dkr.ecr.%REGION%.amazonaws.com/%ECR_CONTAINER_NAME%:%IMAGE_NAME%

REM GO CLEAN UP ECR, NUKE PREVIOUS IMAGES, DON'T LEAVE JUNK AROUND
REM nuke the current version of the new one you are trying to push up
aws ecr batch-delete-image --repository-name %ECR_CONTAINER_NAME% --image-ids imageTag=%IMAGE_NAME%


REM YOU CAN BUILD OLD-SCHOOL
REM docker build -t %IMAGE_NAME%:%VERSION% .

REM OR YOU CAN BUILD VIA COMPOSE
docker compose up -d


REM ECR TAG and PUSH docker container image to ECR
docker tag %IMAGE_NAME%:%VERSION% %ACCTNUM%.dkr.ecr.%REGION%.amazonaws.com/%ECR_CONTAINER_NAME%:%IMAGE_NAME%
docker push %ACCTNUM%.dkr.ecr.%REGION%.amazonaws.com/%ECR_CONTAINER_NAME%:%IMAGE_NAME%

REM create a role for your new lambda, if it has already been created previously, no big deal
aws iam create-role --role-name %LAMBDA_ROLE_NAME% --assume-role-policy-document file://awstrustpolicy.json

REM attach two important policies to the lambda role above - no more doing it by hand in AWS!
aws iam attach-role-policy --role-name %LAMBDA_ROLE_NAME%  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name %LAMBDA_ROLE_NAME%  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

REM now finally create the new lambda function in AWS
aws lambda create-function --function-name %LAMBDA_NAME% --package-type Image --code ImageUri=%ACCTNUM%.dkr.ecr.%REGION%.amazonaws.com/%ECR_CONTAINER_NAME%:%IMAGE_NAME% --role arn:aws:iam::%ACCTNUM%:role/%LAMBDA_ROLE_NAME%


REM sometimes aws hasn't yet created the function above, so you have to wait, before you can do the update-function-code below
REM PAUSE 5 > nul
timeout /t 5 >nul


REM if you are doing an update to an already existing function, this will tie your lambda to your 
aws lambda update-function-code --publish --function-name %LAMBDA_NAME% --image-uri  %ACCTNUM%.dkr.ecr.%REGION%.amazonaws.com/%ECR_CONTAINER_NAME%:%IMAGE_NAME%


REM so that your api can invoke your lambda
aws lambda remove-permission --function-name %LAMBDA_NAME% --statement-id %LAMBDA_NAME%-%REQUEST_TYPE%

REM nasty - I had a / at the end of person on this post, and it didn't like that at all - probably cause it's sending data in the json body? got very lucky
REM aws lambda add-permission --function-name %LAMBDA_NAME% --statement-id %LAMBDA_NAME%-%REQUEST_TYPE% --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:us-east-2:215330149056:k404zm8112/*/%REQUEST_TYPE%/person"
aws lambda add-permission --function-name %LAMBDA_NAME% --statement-id %LAMBDA_NAME%-%REQUEST_TYPE% --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:%REGION%:%ACCTNUM%:%APIHASH%/*/%REQUEST_TYPE%/person"


REM see your new lambda in action by calling it from the command-line. watch for the lambda response at the command-line, and open up the out.json file to see the actual json your lambda sent back to you
aws lambda invoke --function-name %LAMBDA_NAME% out.json
type out.json