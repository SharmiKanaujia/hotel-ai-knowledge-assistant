\# Hotel AI Knowledge Copilot — Threat Model



\## 1. Purpose



Identify security risks and plan protections

for our Hotel AI Knowledge Copilot.



\## 2. Current System



\- Python FastAPI backend

\- FAQ question-answering API

\- Hotel knowledge documents

\- Document chunking

\- Keyword and semantic retrieval

\- Automated tests and evaluations



\## 3. Planned Components



\- Large Language Model (LLM)

\- Docker container

\- AWS ECS Fargate

\- Amazon ECR

\- Application Load Balancer

\- Terraform

\- GitHub Actions

\- Amazon CloudWatch



\## 4. Important Assets



\- Hotel knowledge documents

\- API availability

\- Application source code

\- AWS credentials and permissions (future)

\- AI-generated answers (future)



\## 5. Data Flow



Guest question

&#x20;   |

&#x20;   v

FastAPI backend

&#x20;   |

&#x20;   v

Document retrieval

&#x20;   |

&#x20;   v

Relevant hotel knowledge

&#x20;   |

&#x20;   v

LLM (future)

&#x20;   |

&#x20;   v

Answer to guest



\## 6. Trust Boundaries



\### Boundary 1: Guest to FastAPI

Guest input is untrusted.



Protection:

\- Validate request data

\- Limit input size

\- Apply rate limiting where appropriate



\### Boundary 2: Documents to LLM (Planned)

Retrieved documents are untrusted instructions.



Protection:

\- Treat documents as reference data

\- Restrict access to confidential documents

\- Test against prompt injection attacks



\### Boundary 3: Application to AWS (Planned)

The application must not have unnecessary AWS permissions.



Protection:

\- Use least-privilege IAM roles

\- Avoid hardcoded credentials

\- Monitor suspicious activity



\## 7. Threat Register



| ID | Threat | Impact | Planned Mitigation | Status |

|---|---|---|---|---|

| T01 | Oversized or abusive API requests | Resource exhaustion | Question length validation, request-body limits, rate limiting | Partially implemented: 1–500 character validation |

| T02 | Indirect prompt injection through documents | Incorrect answers or unauthorized actions | Treat retrieved content as data, restrict tools, test attacks | Planned |

| T03 | Exposure of confidential hotel documents | Information leakage | Document classification and access control | Planned |

| T04 | Excessive AWS IAM permissions | Unauthorized AWS resource access | Least-privilege ECS task roles | Planned |



\## 8. Security Testing Plan



\- Validate API request size and structure.

\- Test malicious instructions inside knowledge documents.

\- Verify confidential documents are not exposed.

\- Run an OWASP ZAP baseline scan against our test API.

\- Review ECS task and deployment IAM policies.

\- Check application logs for sensitive information.



\## 9. Implemented Security Controls



\### SEC-001: API Question Length Validation



Status: Implemented and tested



Location: main.py



Control:

\- Questions must contain at least 1 character.

\- Questions cannot exceed 500 characters.

\- Invalid questions return HTTP 422.



Automated tests:

\- test\_reject\_empty\_question

\- test\_reject\_oversized\_question



Current limitations:

\- Whitespace-only questions are not yet rejected.

\- HTTP request-body size limits are not implemented.

\- Rate limiting is not implemented.



Related threat: T01

