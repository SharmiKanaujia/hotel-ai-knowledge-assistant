# Hotel AI Knowledge Assistant

**A cloud-deployed Retrieval-Augmented Generation (RAG) application built with FastAPI, Amazon Bedrock, Docker, AWS Lambda, and Terraform.**

This project demonstrates how to design, build, test, and deploy a generative AI application that answers hotel-related questions using a document-based knowledge base.

Instead of relying only on predefined answers, the application retrieves relevant hotel information and uses **Amazon Nova Lite** through Amazon Bedrock to generate grounded responses with source-document references.

## Project Highlights

- Python REST API developed with FastAPI
- Hotel FAQ knowledge base and semantic document retrieval
- Retrieval-Augmented Generation (RAG) with FastEmbed
- Generative AI integration using Amazon Bedrock Converse API
- Amazon Nova Lite foundation model
- Docker containerization with a bundled embedding model
- Serverless deployment using AWS Lambda and Lambda Web Adapter
- Amazon API Gateway with AWS IAM authentication
- Infrastructure as Code using Terraform
- Amazon ECR container image storage
- CloudWatch logging and retention
- API throttling and model-specific IAM permissions
- Automated testing with Pytest

## Architecture

```text
        Authenticated Client
                |
                | HTTPS + AWS SigV4
                v
        Amazon API Gateway
                |
                v
             AWS Lambda
          (Docker Container)
                |
                v
          FastAPI Backend
                |
                v
         RAG Orchestration
                |
                v
       Semantic Document Retrieval
          (FastEmbed Model)
                |
                v
       Retrieved Hotel Documents
                |
                v
        Amazon Bedrock
        (Amazon Nova Lite)
                |
                v
        Generated Answer
        + Source References
```

**Infrastructure:** Terraform manages the main application resources, including Lambda, API Gateway, ECR, S3, IAM and CloudWatch.

**Deployment region:** AWS Sydney (`ap-southeast-2`), used as the project's development environment.

## How RAG Works

1. A customer submits a hotel-related question.
2. FastAPI receives and validates the request.
3. The retrieval component searches the hotel's document knowledge base.
4. Relevant information is incorporated into the model prompt.
5. Amazon Bedrock invokes Amazon Nova Lite to generate a response.
6. The API returns the answer with references to the retrieved source documents.

### Example

**Request**

```json
{
  "question": "Where can I leave my car?"
}
```

**Response observed during live AWS testing**

```json
{
  "question": "Where can I leave my car?",
  "answer": "You can leave your car in the parking area provided by the hotel.",
  "sources": ["parking.md"]
}
```

This response was successfully tested through the deployed, IAM-authenticated API Gateway endpoint.

Source references currently identify documents. More precise passage-level citations are planned for a later phase.

## API Endpoints

| Endpoint | Description |
|---|---|
| `POST /ask` | FAQ-based question answering |
| `POST /ask/rag` | Live RAG-powered question answering |
| `GET /chat` | Browser-based chat interface |
| `GET /chat/config` | Chat feature configuration |
| `GET /openapi.json` | OpenAPI specification |

Live RAG is controlled through the `ENABLE_LIVE_RAG` feature flag. Experimental demo RAG can be controlled separately.

## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Backend | FastAPI, Uvicorn |
| AI / LLM | Amazon Bedrock, Amazon Nova Lite |
| Retrieval | RAG, FastEmbed, semantic search |
| AWS SDK | Boto3 |
| Containers | Docker |
| Compute | AWS Lambda, Lambda Web Adapter |
| API | Amazon API Gateway |
| Storage and registry | Amazon S3, Amazon ECR |
| Security | AWS IAM, AWS Signature Version 4 |
| Monitoring | Amazon CloudWatch |
| Infrastructure | Terraform |
| Testing | Pytest |
| Development workflow | Git, GitHub, GitHub Actions |

## Local Development

Clone the repository:

```bash
git clone https://github.com/SharmiKanaujia/hotel-ai-knowledge-assistant.git
cd hotel-ai-knowledge-assistant
```

Create and activate a Python virtual environment.

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python -m uvicorn main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

For local development, use the FAQ endpoint without enabling live Bedrock inference unless AWS credentials and model permissions are configured.

## Running Tests

Run the Python test suite:

```bash
python -m pytest
```

The repository includes tests for backend functionality and RAG behavior. Some feature-gated or experimental scenarios may be intentionally marked as expected failures.

## AWS Deployment

The application is deployed as a Docker-based AWS Lambda function using Amazon ECR and Lambda Web Adapter.

Terraform configuration is located in:

```text
infra/terraform/
```

The infrastructure includes:

- Private ECR repository for the application container
- Lambda execution role and Bedrock invocation policy
- Container-based Lambda function
- API Gateway HTTP API
- API Gateway–Lambda integration and permissions
- CloudWatch log group
- S3 infrastructure resources

Terraform is used to manage changes through its standard formatting, validation, planning and apply workflow.

The repository does not provide public anonymous access to its deployed AI endpoint. AWS authentication is required.

## Security and Operational Safeguards

The development deployment implements several security and operational controls.

**API authentication**

API Gateway uses AWS IAM authorization. An unsigned request to the live RAG endpoint was tested and rejected with HTTP 403.

**Least-privilege Bedrock permissions**

The dedicated Lambda Bedrock policy allows `bedrock:InvokeModel` for the specific Amazon Nova Lite foundation model in `ap-southeast-2`.

**API throttling**

The deployed API Gateway stage uses a throttling rate of 2 requests per second and a burst limit of 5.

**CloudWatch logging**

The Lambda log group uses a seven-day retention policy.

**Lambda configuration**

The deployed function uses 1,024 MB of memory and a 30-second timeout.

**Cost monitoring**

A monthly AWS cost budget is managed by Terraform in `infra/terraform/budget.tf`. It sends an email alert when actual spend passes 50%, 80% and 100% of the monthly limit. The limit and the alert email are Terraform variables (`monthly_budget_limit_usd` and `budget_alert_email`). The email is not stored in the repository: set it in an untracked `terraform.tfvars` file or with the `TF_VAR_budget_alert_email` environment variable.

A separate zero-spend budget, created in the AWS console, sends an alert as soon as any charge appears.

AWS Budgets provides spending notifications rather than a hard spending limit.

These controls are appropriate for an educational proof of concept and do not constitute a complete production security assessment.

## Deployment Verification

The following scenarios have been tested successfully:

| Test | Result |
|---|---|
| Local FastAPI backend functionality | Passed |
| Docker-based application execution | Passed |
| AWS Lambda FAQ invocation | Passed |
| Authenticated API Gateway FAQ request | Passed |
| Anonymous API access rejection | HTTP 403 |
| Bedrock IAM policy inspection | Passed |
| Live Bedrock RAG through direct Lambda invocation | Passed |
| Live Bedrock RAG through authenticated API Gateway | Passed |
| CloudWatch log group and retention | Verified |
| API Gateway throttling configuration | Verified |

## Engineering Challenges

### 1. Lambda Container Image Compatibility

The original Docker image format was incompatible with the Lambda container-image requirements.

The image was rebuilt for Linux AMD64 using a compatible OCI image manifest, resolving the deployment problem.

### 2. Containerized Embedding Model

The semantic retrieval pipeline required embedding-model resources to be available inside the container.

The deployment image was configured to include the model assets needed by the application.

### 3. AWS Authentication and API Authorization

API Gateway uses IAM authentication rather than permitting anonymous calls.

Authenticated API testing required generating AWS Signature Version 4 requests.

### 4. Terraform and AWS Credential Management

Infrastructure changes involved resolving temporary AWS credential expiration and intermittent Terraform AWS provider startup issues.

### 5. Bedrock Model Permissions

Lambda initially needed a dedicated permission to invoke the selected foundation model.

A model-specific IAM policy was added and verified before enabling live RAG.

## Future Improvements — Phase 2

The next phase focuses on production-oriented AI engineering.

Planned enhancements include:

- Automated retrieval and answer-quality evaluations
- Model Context Protocol (MCP) integration for read-only synthetic hotel operations
- Hybrid retrieval using lexical and vector search
- Reranking and improved citation precision
- Prompt-injection testing and hotel-specific data isolation
- Token usage and inference-cost tracking
- Model selection, routing and fallback strategies
- Latency measurement, caching and load testing
- Enhanced monitoring and CI quality gates

**Phase 2 target:** January 15, 2027.

## Project Purpose

This is a hands-on engineering and portfolio project exploring how cloud infrastructure, backend development, retrieval systems, generative AI, deployment automation, and security controls fit together in a single application.

The project uses fictional hotel information and is intended for educational and demonstration purposes.

**Repository:** https://github.com/SharmiKanaujia/hotel-ai-knowledge-assistant
