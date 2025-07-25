# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability within this project, please follow these steps:

1. **Do NOT** create a public GitHub issue
2. Email the details to [INSERT SECURITY EMAIL]
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Scope

This security policy applies to:
- The Streamlit application code
- Dependencies listed in requirements.txt
- GitHub Actions workflows

## Out of Scope

- The FedRAMP documentation content (submodules)
- Third-party services (Streamlit Cloud, GitHub)
- Browser security issues

## Response Timeline

- Initial response: Within 48 hours
- Status update: Within 5 business days
- Resolution timeline: Depends on severity

## Disclosure Policy

- Security issues will be disclosed after a fix is available
- Credit will be given to reporters (unless anonymity is requested)

## Security Best Practices for Users

1. Keep dependencies updated
2. Use virtual environments
3. Review code before running
4. Use official deployment methods
5. Monitor for security updates

## Data Security

This application:
- Does not collect user data
- Does not store sensitive information
- Only reads public FedRAMP documentation
- Does not require authentication

## Dependencies

We regularly update dependencies to patch security vulnerabilities. Users should:
- Run `pip install --upgrade -r requirements.txt` regularly
- Monitor security advisories for dependencies