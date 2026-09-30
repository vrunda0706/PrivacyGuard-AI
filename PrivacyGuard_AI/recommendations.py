def generate_recommendations(email_findings, phone_findings, breach_findings, ml_risk):
    recs = []
    if breach_findings:
        recs.append("Review affected accounts and change reused passwords; never reuse a password after an exposure.")
    if email_findings:
        recs.append("Reduce public exposure of your email address and remove it from unnecessary public profiles.")
    if phone_findings:
        recs.append("Limit public phone-number visibility and review apps that have access to contacts.")
    recs.append("Enable multi-factor authentication on email, banking, cloud and social accounts.")
    recs.append("Review old accounts and revoke access for services you no longer use.")
    if ml_risk == "HIGH":
        recs.insert(0, "Prioritize the highest-risk accounts first and monitor security alerts closely.")
    return recs[:5]
