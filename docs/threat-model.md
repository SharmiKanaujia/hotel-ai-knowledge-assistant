# Hotel AI Knowledge Copilot — Threat Model

## 1. Purpose

Identify security risks and track protections for the Hotel AI Knowledge Copilot.

All hotel data in this project is fictional.

## 2. Current System

Application:

- Python FastAPI backend (`main.py`)
- FAQ keyword question-answering endpoint (`/ask`)
- Live RAG endpoint (`/ask/rag`) using Amazon Bedrock (Amazon Nova Lite, Converse API)
- Hotel knowledge documents in `knowledge/`, chunked and searched with keyword and semantic (FastEmbed) retrieval
- Automated tests and evaluations

AWS infrastructure (Terraform in `infra/terraform/`, region ap-southeast-2):

- Docker image stored in a private Amazon ECR repository (immutable tags, scan on push)
- AWS Lambda running the image through the Lambda Web Adapter
- Amazon API Gateway HTTP API in front of Lambda, with `AWS_IAM` authorization on the default route
- Lambda execution role allowed `bedrock:InvokeModel` on the Amazon Nova Lite foundation model only
- Amazon CloudWatch log group for the function (7-day retention)
- Private S3 bucket with public access blocked (not yet used by the application)

CI (GitHub Actions):

- Docker build and smoke test
- Terraform `fmt` and `validate`
- OWASP ZAP baseline scan against a locally started API

## 3. Planned Components

- Request-body size limits in the application
- Document classification and access control
- Prompt injection test cases

## 4. Important Assets

- Hotel knowledge documents
- API availability
- Application source code and Docker image
- AWS credentials and IAM permissions
- Amazon Bedrock usage and cost
- AI-generated answers and their cited sources

## 5. Data Flow

```text
Caller (signed with AWS SigV4)
    |
    v
Amazon API Gateway HTTP API
(AWS_IAM authorization, stage throttling)
    |
    v
AWS Lambda (FastAPI + Lambda Web Adapter)
    |
    v
Document retrieval (FastEmbed model bundled in the image)
    |
    v
Relevant hotel knowledge
    |
    v
Amazon Bedrock — Amazon Nova Lite (Converse API)
    |
    v
Answer with cited sources
```

If retrieval finds no relevant documents, the application returns
"I could not find that information." without calling Bedrock.

## 6. Trust Boundaries

### Boundary 1: Caller to API Gateway and FastAPI

Caller input is untrusted.

Protection in place:

- API Gateway requires IAM (SigV4) authentication on the default route.
- Stage throttling: burst limit 5, rate limit 2 requests per second.
- Lambda can only be invoked by this API Gateway API (`aws_lambda_permission` scoped by source ARN).
- Questions are validated: trimmed, 1–500 characters.

Still planned:

- Application-level request-body size limit.

### Boundary 2: Documents to LLM

Retrieved documents must be treated as reference data, never as instructions.

Protection in place:

- The RAG prompt tells the model to use the hotel knowledge as reference information, not as instructions, and to answer only from facts in it.
- The Bedrock Converse call does not give the model any tools, so the model cannot trigger actions.

Still planned:

- Restrict access to confidential documents.
- Test against prompt injection attacks.

### Boundary 3: Application to AWS

The application must not have unnecessary AWS permissions.

Protection in place:

- The Lambda execution role can be assumed only by `lambda.amazonaws.com`.
- Bedrock access is limited to `bedrock:InvokeModel` on `arn:aws:bedrock:ap-southeast-2::foundation-model/amazon.nova-lite-v1:0`.
- No credentials are hard-coded; the function uses its execution role.

Remaining gap:

- Logging uses the AWS managed policy `AWSLambdaBasicExecutionRole`, which grants CloudWatch Logs actions on all resources. A custom policy scoped to the function's log group would be tighter.

## 7. Threat Register

| ID | Threat | Impact | Mitigation | Status |
|---|---|---|---|---|
| T01 | Oversized or abusive API requests | Resource exhaustion, Bedrock cost | Question length validation, IAM authentication and throttling at API Gateway, request-body limits | Partially mitigated: 1–500 character validation (tested); IAM authentication and throttling defined in Terraform; application request-body limit not implemented |
| T02 | Indirect prompt injection through documents | Incorrect answers or unauthorized actions | Treat retrieved content as data, give the model no tools, test attacks | Partially mitigated: prompt instructs the model to treat knowledge as data; no tools are passed to the model; no prompt injection tests yet |
| T03 | Exposure of confidential hotel documents | Information leakage | Document classification and access control | Planned |
| T04 | Excessive AWS IAM permissions | Unauthorized AWS resource access | Least-privilege Lambda execution role | Mostly mitigated: Bedrock access limited to `bedrock:InvokeModel` on Amazon Nova Lite; logging still uses the AWS managed `AWSLambdaBasicExecutionRole` policy |

## 8. Security Testing Plan

- Validate API request size and structure.
- Test malicious instructions inside knowledge documents.
- Verify confidential documents are not exposed.
- Run an OWASP ZAP baseline scan against the test API. (Runs in CI against a locally started API; findings do not fail the build.)
- Review the Lambda execution role and deployment IAM policies.
- Verify that unsigned requests to the API Gateway endpoint are rejected.
- Check application logs for sensitive information.

## 9. Implemented Security Controls

### SEC-001: API Question Length Validation

Status: Implemented and tested

Location: `main.py`

Control:

- Leading and trailing whitespace is removed.
- Empty and whitespace-only questions are rejected.
- Questions must contain 1–500 characters after trimming.
- Invalid questions return HTTP 422.

Automated tests (`tests/test_security.py`):

- `test_reject_empty_question`
- `test_reject_oversized_question`
- `test_reject_whitespace_only_question`
- `test_accept_exactly_500_characters`

Current limitations:

- HTTP request-body size limits are not implemented in the application.

Related threat: T01

### SEC-002: IAM Authentication and Throttling at API Gateway

Status: Defined in Terraform; no automated test

Location: `infra/terraform/api_gateway.tf`

Control:

- The `$default` route uses `authorization_type = "AWS_IAM"`, so requests must be signed with AWS SigV4.
- The `$default` stage sets `throttling_burst_limit = 5` and `throttling_rate_limit = 2`.
- The Lambda permission allows invocation only from this API's execution ARN.

Current limitations:

- Throttling applies to the whole stage, not per caller.

Related threat: T01

### SEC-003: Least-Privilege Bedrock Access for Lambda

Status: Defined in Terraform; no automated test

Location: `infra/terraform/iam.tf`, `infra/terraform/bedrock.tf`

Control:

- The execution role trusts only `lambda.amazonaws.com`.
- The only Bedrock permission is `bedrock:InvokeModel` on the Amazon Nova Lite foundation model ARN in the configured region.

Current limitations:

- CloudWatch logging permissions come from the AWS managed `AWSLambdaBasicExecutionRole` policy, which is not scoped to the function's log group.

Related threat: T04

### SEC-004: Retrieved Knowledge Treated as Data

Status: Partially implemented

Location: `rag/pipeline.py`, `rag/llm.py`

Control:

- The prompt tells the model to use the hotel knowledge as reference information, not as instructions.
- The model must answer only from facts in the hotel knowledge, or reply "I could not find that information."
- The Converse request passes no tool configuration, so the model cannot call tools.
- Bedrock is not called when no relevant documents are found.

Automated tests:

- `tests/test_rag_grounding.py` checks that grounding instructions are present in the prompt.
- `tests/test_llm.py` checks that Bedrock is not called when no sources are found (Bedrock client mocked).

Current limitations:

- No tests with malicious instructions inside knowledge documents.
- Prompt instructions reduce but do not remove prompt injection risk.

Related threat: T02
