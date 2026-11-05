"""
Generates an expanded, enterprise-grade SYNTHETIC regulatory rulebook PDF
designed for testing and demonstrating AuditAgent.

Contains 12 comprehensive compliance domains with realistic statutory language,
clause identifiers (e.g., Section 1.1, Section 2.1), and explicit requirements.
"""
from pathlib import Path
import pymupdf

OUTPUT_DIR = Path("data/synthetic_corpus")
OUTPUT_PDF = OUTPUT_DIR / "synthetic_enterprise_rulebook.pdf"

SYNTHETIC_NOTICE = "[SYNTHETIC REGULATORY TEXT - FOR AUDITAGENT TESTING AND EVALUATION ONLY]"

RULEBOOK_SECTIONS = [
    (
        "Section 1.1 Access Log Retention",
        "Synthetic Rule R-101: All computer system access logs, authentication records, and administrative activity logs must be retained for a minimum of 90 days in active storage and archived for a minimum duration of 365 days. Log tampering prevention mechanisms must be enabled.",
        1
    ),
    (
        "Section 1.2 User Data Deletion Timelines",
        "Synthetic Rule R-102: Validated user deletion requests under privacy mandates must be permanently fulfilled and purged across all production and backup datastores within 30 calendar days of initial identity verification.",
        1
    ),
    (
        "Section 2.1 Cryptographic Controls at Rest",
        "Synthetic Rule R-201: All confidential, financial, and personal identifiable information (PII) at rest must be encrypted using AES-256 or an approved equivalent cryptographic algorithm. Unencrypted storage of credentials or tokens is strictly prohibited.",
        2
    ),
    (
        "Section 2.2 Network Encryption in Transit",
        "Synthetic Rule R-202: All external data transmissions across public networks must be secured using Transport Layer Security (TLS) protocol version 1.3 or higher. Deprecated protocols including SSL 3.0, TLS 1.0, and unencrypted HTTP are strictly prohibited.",
        2
    ),
    (
        "Section 3.1 Geographic Data Sovereignty and Residency",
        "Synthetic Rule R-301: Customer personal data belonging to residents of Region Alpha must be stored exclusively on physical servers located within Region Alpha. Trans-border replication to Region Beta without bilateral regulatory certification is strictly prohibited.",
        3
    ),
    (
        "Section 4.1 Security Incident Notification Timelines",
        "Synthetic Rule R-401: Any confirmed security breach involving unauthorized disclosure or compromise of sensitive customer records must be formally notified to the regulatory oversight committee within 72 hours of initial discovery.",
        3
    ),
    (
        "Section 5.1 Multi-Factor Authentication Requirements",
        "Synthetic Rule R-501: Multi-factor authentication (MFA) is strictly mandatory for all interactive employee access to internal enterprise networks, administrative consoles, and remote cloud infrastructure.",
        4
    ),
    (
        "Section 5.2 Access Rights and Privilege Review",
        "Synthetic Rule R-502: Privileged user accounts and elevated administrative access rights must be audited and formally reviewed by department supervisors at least once every 90 days.",
        4
    ),
    (
        "Section 6.1 Vulnerability Remediation SLAs",
        "Synthetic Rule R-601: Critical severity software vulnerabilities with a CVSS base score of 9.0 or greater must be remediated or mitigated through compensating controls within 14 calendar days of public release.",
        5
    ),
    (
        "Section 7.1 Employee Offboarding Access Revocation",
        "Synthetic Rule R-701: All digital, logical, and physical access credentials for terminating employees or contractors must be permanently deactivated within 24 hours of employment conclusion.",
        5
    ),
    (
        "Section 8.1 Disaster Recovery and Backup Frequency",
        "Synthetic Rule R-801: Automated database backups must be performed daily, cryptographically verified, and replicated to a geographically distinct secondary facility with a target Recovery Point Objective (RPO) of under 4 hours.",
        6
    ),
    (
        "Section 9.1 Third-Party Vendor Risk Auditing",
        "Synthetic Rule R-901: Third-party cloud service providers processing enterprise confidential data must possess an active SOC 2 Type II certification and undergo an annual security compliance assessment.",
        6
    ),
]


def generate_enterprise_rulebook(output_path: Path = OUTPUT_PDF) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open()

    # Cover Page
    cover = doc.new_page()
    cover.insert_textbox(
        pymupdf.Rect(50, 80, 545, 200),
        "ENTERPRISE REGULATORY COMPLIANCE FRAMEWORK\n(SYNTHETIC TEST SPECIFICATION v2.0)",
        fontsize=15,
    )
    cover.insert_textbox(
        pymupdf.Rect(50, 220, 545, 650),
        "Published for Automated AI Compliance Auditing & Verification\n\n"
        "TABLE OF DOMAINS:\n"
        "- Domain 1: Information Lifecycle & Log Retention (Sections 1.1 - 1.2)\n"
        "- Domain 2: Cryptographic Controls & Transit Security (Sections 2.1 - 2.2)\n"
        "- Domain 3: Data Residency & Jurisdictional Sovereignty (Section 3.1)\n"
        "- Domain 4: Incident Response & Breach Notification (Section 4.1)\n"
        "- Domain 5: Identity Governance & MFA Controls (Sections 5.1 - 5.2)\n"
        "- Domain 6: Vulnerability & Patch Management (Section 6.1)\n"
        "- Domain 7: Human Resource Security & Offboarding (Section 7.1)\n"
        "- Domain 8: Continuity & Immutable Backups (Section 8.1)\n"
        "- Domain 9: Vendor Management & Supply Chain (Section 9.1)\n\n"
        f"{SYNTHETIC_NOTICE}\n"
        "Notice: This document contains synthetic benchmarks for testing AuditAgent.",
        fontsize=11,
    )

    # Content Pages
    pages = {}
    for heading, text, page_idx in RULEBOOK_SECTIONS:
        if page_idx not in pages:
            pages[page_idx] = []
        pages[page_idx].append((heading, text))

    for p_idx in sorted(pages.keys()):
        page = doc.new_page()
        y_cursor = 60
        for heading, body in pages[p_idx]:
            content = f"{heading}\n{body}\n"
            rect = pymupdf.Rect(50, y_cursor, 545, y_cursor + 180)
            page.insert_textbox(rect, content, fontsize=11)
            y_cursor += 190

        # Footer
        page.insert_text(
            pymupdf.Point(50, 800),
            f"Page {p_idx + 1} | Synthetic Rulebook v2.0 | {SYNTHETIC_NOTICE}",
            fontsize=8,
        )

    doc.save(str(output_path))
    doc.close()
    return output_path


if __name__ == "__main__":
    out = generate_enterprise_rulebook()
    print(f"Successfully generated: {out.resolve()} ({out.stat().st_size} bytes)")
