On the *AWS Free plan* you can earn extra credits ($20 each) for 5 activities: EC2, Budgets, Lambda, RDS and Bedrock. Most of us already got the EC2 one from RoboShop, so that leaves *$80 more* to earn. You can see them in the *Explore AWS* panel on the console home page → Filter: *Earn AWS credits*.

I've attached the bash file and screenshots for your reference :point_down:

*Step 1: Run the script (Budgets, Lambda, RDS)*
The script does these 3 automatically and cleans up after itself (RDS is created and then deleted, so no ongoing cost).
1. Open *CloudShell*: type `CloudShell` in the AWS search bar, or click the `>_` icon in the top bar. Make sure the region is `us-east-1`
2. *Actions → Upload file* → `aws-credits.sh`
3. Run `bash aws-credits.sh` and enter your email for budget alerts
4. The RDS step takes about 5–10 minutes, keep the tab open

*Step 2: Bedrock (do this one by hand)*
The Bedrock activity only counts if you use the console playground, not the script.
1. Type `Bedrock` in the AWS search bar and open *Amazon Bedrock*
2. In the left menu, under *Test*, click *Playground*
3. Set *Mode* to *Chat*, click *Select model*, choose *Amazon → Nova Micro*, then *Apply*
4. Type `hello` in the prompt box and press *Enter* (or click *Run*)
5. Wait for the reply. It costs less than a cent

*Step 3: Check your credits*
Refresh the *Explore AWS* panel. It can take a few minutes to show *5 of 5 completed*.

My credits went from $55 to $135 (+$80) :tada:
Please read the script before running it, and terminate your RoboShop instances after class to save credits!
###########################################################################################################
#!/bin/bash
# Completes the AWS free-plan "explore" activities: Budgets, Lambda, Bedrock, RDS.
# Run in AWS CloudShell (top bar of the AWS console) in us-east-1:
#   bash aws-credits.sh
# Everything it creates is cleaned up at the end, except the budget (keep that one).

REGION="us-east-1"
export AWS_DEFAULT_REGION=$REGION
R="\e[31m"; G="\e[32m"; N="\e[0m"

validate(){
    if [ $1 -ne 0 ]; then echo -e "$2..${R}FAILED${N}"; else echo -e "$2..${G}SUCCESS${N}"; fi
}

read -p "Email for budget alerts: " EMAIL
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# ---------- 1. Budgets ----------
aws budgets create-budget --account-id "$ACCOUNT_ID" \
  --budget '{"BudgetName":"monthly-5-usd","BudgetLimit":{"Amount":"5","Unit":"USD"},"TimeUnit":"MONTHLY","BudgetType":"COST"}' \
  --notifications-with-subscribers "[{\"Notification\":{\"NotificationType\":\"ACTUAL\",\"ComparisonOperator\":\"GREATER_THAN\",\"Threshold\":80,\"ThresholdType\":\"PERCENTAGE\"},\"Subscribers\":[{\"SubscriptionType\":\"EMAIL\",\"Address\":\"$EMAIL\"}]}]"
validate $? "Creating budget (\$5/month, alert at 80%)"

# ---------- 2. Lambda ----------
aws iam create-role --role-name credits-lambda-role \
  --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' >/dev/null
aws iam attach-role-policy --role-name credits-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
validate $? "Creating Lambda role"
sleep 15   # IAM role needs a few seconds before Lambda can use it

mkdir -p /tmp/lambda && cd /tmp/lambda
cat > index.mjs <<'EOF'
export const handler = async () => ({ statusCode: 200, body: "Hello from Lambda" });
EOF
zip -q fn.zip index.mjs
aws lambda create-function --function-name credits-hello --runtime nodejs22.x \
  --handler index.handler --zip-file fileb://fn.zip \
  --role "arn:aws:iam::$ACCOUNT_ID:role/credits-lambda-role" >/dev/null
validate $? "Creating Lambda function"
aws lambda wait function-active --function-name credits-hello
aws lambda invoke --function-name credits-hello /tmp/lambda/out.json >/dev/null
validate $? "Invoking Lambda function"
cd - >/dev/null

# ---------- 3. Bedrock ----------
aws bedrock-runtime converse --model-id amazon.nova-micro-v1:0 \
  --messages '[{"role":"user","content":[{"text":"Say hello in one sentence."}]}]' \
  --query 'output.message.content[0].text' --output text
validate $? "Sending prompt to Bedrock"

# ---------- 4. RDS (create, wait, delete) ----------
aws rds create-db-instance --db-instance-identifier credits-test-db \
  --engine mysql --db-instance-class db.t4g.micro --allocated-storage 20 \
  --master-username admin --manage-master-user-password \
  --no-publicly-accessible --backup-retention-period 0 >/dev/null
validate $? "Creating RDS database"
echo "Waiting for RDS to become available (about 5-10 minutes)..."
aws rds wait db-instance-available --db-instance-identifier credits-test-db
validate $? "RDS database available"

aws rds delete-db-instance --db-instance-identifier credits-test-db \
  --skip-final-snapshot --delete-automated-backups >/dev/null
validate $? "Deleting RDS database"

# ---------- Cleanup Lambda ----------
aws lambda delete-function --function-name credits-hello
aws iam detach-role-policy --role-name credits-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam delete-role --role-name credits-lambda-role
validate $? "Cleaning up Lambda"

echo "Done. Check Billing -> Credits in a few hours to confirm the new credits."
