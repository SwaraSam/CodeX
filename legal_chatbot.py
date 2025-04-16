import re

# --- Knowledge Base ---
knowledge_base = {
    ("contract", "agreement"): {
        "info": """## Contract Law
        
A contract is a legally enforceable agreement between two or more parties that creates mutual obligations.

### Key Elements:
1. Offer and acceptance
2. Consideration (something of value exchanged)
3. Legal intent to create binding relations
4. Legal capacity of parties
5. Genuine consent (no fraud, duress, or undue influence)

### Common Contract Types:
- Written contracts
- Oral contracts (verbal agreements)
- Implied contracts
- Express contracts
- Unilateral and bilateral contracts

### Contract Breach Remedies:
- Damages (compensatory, punitive, liquidated)
- Specific performance
- Rescission (contract cancellation)""",
        "resources": [
            "https://en.wikipedia.org/wiki/Contract",
            "https://www.law.cornell.edu/wex/contract",
            "https://www.americanbar.org/groups/business_law/publications/blt/"
        ]
    },
    ("divorce", "separation", "marriage", "custody"): {
        "info": """## Divorce Law
        
Divorce is the legal dissolution of a marriage by a court or other competent body.

### Divorce Process:
1. Filing a petition
2. Temporary orders (if needed)
3. Discovery (financial/asset disclosure)
4. Negotiation/mediation
5. Trial (if settlement isn't reached)
6. Judgment of divorce

### Common Issues in Divorce:
- Asset and debt division
- Child custody and visitation
- Child support
- Spousal support/alimony
- Tax considerations

### Types of Divorce:
- No-fault divorce
- Fault-based divorce
- Uncontested divorce
- Contested divorce
- Collaborative divorce
- Mediated divorce""",
        "resources": [
            "https://en.wikipedia.org/wiki/Divorce",
            "https://www.americanbar.org/groups/family_law/",
            "https://www.findlaw.com/family/divorce.html"
        ]
    },
    ("alimony", "spousal support", "maintenance"): {
        "info": """## Alimony/Spousal Support
        
Alimony is court-ordered financial support paid by one ex-spouse to the other after separation or divorce.

### Types of Alimony:
1. Temporary (during divorce proceedings)
2. Rehabilitative (until recipient becomes self-sufficient)
3. Permanent (until death or remarriage)
4. Lump-sum (one-time payment)
5. Reimbursement (repayment for expenses like education)

### Factors Courts Consider:
- Length of marriage
- Age and health of both parties
- Income and earning capacity of each spouse
- Standard of living during marriage
- Contributions to marriage (including homemaking)
- Tax implications""",
        "resources": [
            "https://en.wikipedia.org/wiki/Alimony",
            "https://www.findlaw.com/family/divorce/spousal-support-alimony-basics.html",
            "https://www.nolo.com/legal-encyclopedia/alimony-what-you-need-know-30081.html"
        ]
    },
    ("property", "assets", "ownership", "real estate", "land"): {
        "info": """## Property Law
        
Property law governs the various forms of ownership and tenancy in real property (land) and personal property.

### Types of Property:
1. Real property (land and attached structures)
2. Personal property (movable possessions)
3. Tangible property (physical items)
4. Intangible property (non-physical assets like stocks)

### Property Rights:
- Right to use and enjoy
- Right to exclude others
- Right to transfer ownership
- Right to possess

### Common Property Issues:
- Boundary disputes
- Easements and rights of way
- Adverse possession
- Zoning regulations
- Eminent domain
- Liens and encumbrances
- Landlord-tenant disputes""",
        "resources": [
            "https://en.wikipedia.org/wiki/Property_law",
            "https://www.law.cornell.edu/wex/property",
            "https://www.americanbar.org/groups/real_property_trust_estate/"
        ]
    },
    ("tax", "income tax", "irs", "revenue", "taxation"): {
        "info": """## Tax Law
        
Tax law encompasses the rules and policies that govern taxation by various government authorities.

### Types of Taxes:
1. Income tax (personal and business)
2. Property tax
3. Sales tax
4. Capital gains tax
5. Estate and gift tax
6. Payroll tax
7. Excise tax

### Tax Compliance Issues:
- Filing requirements and deadlines
- Record-keeping obligations
- Tax audits and appeals
- Tax evasion vs. tax avoidance
- Tax credits and deductions
- International taxation

### Tax Planning Strategies:
- Income shifting
- Tax deferral
- Tax-advantaged investments
- Charitable contributions
- Business entity selection""",
        "resources": [
            "https://en.wikipedia.org/wiki/Tax_law",
            "https://www.irs.gov/",
            "https://www.americanbar.org/groups/taxation/"
        ]
    },
    ("criminal", "crime", "felony", "misdemeanor"): {
        "info": """## Criminal Law
        
Criminal law deals with crimes and their punishment, addressing behaviors that are prohibited by statute and considered harmful to society.

### Types of Crimes:
1. Felonies (serious crimes with prison sentences over one year)
2. Misdemeanors (less serious crimes with sentences under one year)
3. Infractions (minor violations often punishable by fines)

### Elements of a Crime:
- Criminal act (actus reus)
- Criminal intent (mens rea)
- Concurrence (act and intent occurring together)
- Causation
- Harm

### Criminal Procedure:
- Investigation
- Arrest
- Charging
- Arraignment
- Plea bargaining
- Trial
- Sentencing
- Appeals""",
        "resources": [
            "https://en.wikipedia.org/wiki/Criminal_law",
            "https://www.law.cornell.edu/wex/criminal_law",
            "https://www.americanbar.org/groups/criminal_justice/"
        ]
    },
    ("murder", "homicide", "killing", "manslaughter"): {
        "info": """## Homicide Law
        
Homicide refers to the killing of one person by another, which may be classified as criminal or non-criminal depending on circumstances.

### Types of Homicide:
1. Murder (intentional killing with malice aforethought)
   - First-degree murder (premeditated)
   - Second-degree murder (intentional but not premeditated)
   
2. Manslaughter (killing without malice aforethought)
   - Voluntary manslaughter (heat of passion)
   - Involuntary manslaughter (unintentional, from negligence)
   
3. Justifiable homicide (self-defense, law enforcement)

### Defenses to Homicide Charges:
- Self-defense
- Defense of others
- Insanity
- Duress
- Accident
- Alibi""",
        "resources": [
            "https://en.wikipedia.org/wiki/Murder",
            "https://en.wikipedia.org/wiki/Manslaughter",
            "https://www.law.cornell.edu/wex/homicide"
        ]
    },
    ("copyright", "intellectual property", "ip", "trademark", "patent"): {
        "info": """## Intellectual Property Law
        
Intellectual property (IP) law protects creations of the mind, giving creators exclusive rights to their work.

### Main Types of IP:
1. Copyright (protects original creative works)
   - Books, music, art, software, etc.
   - Protection length: creator's life + 70 years (typically)
   
2. Trademark (protects brand identifiers)
   - Names, logos, slogans, etc.
   - Protection length: renewable every 10 years (indefinitely)
   
3. Patent (protects inventions)
   - Utility patents: 20 years
   - Design patents: 15 years
   
4. Trade Secrets (confidential business information)
   - Protection length: as long as kept secret

### IP Infringement:
- Direct infringement
- Contributory infringement
- Vicarious infringement
- Fair use and other exceptions""",
        "resources": [
            "https://www.wipo.int",
            "https://www.uspto.gov/",
            "https://copyright.gov/",
            "https://www.law.cornell.edu/wex/intellectual_property"
        ]
    },
    ("act", "statute", "legislation", "law", "bill"): {
        "info": """## Legislative Process
        
Legislation refers to laws or acts passed by a legislative body like Congress, Parliament, or state legislatures.

### Legislative Process:
1. Bill drafting and introduction
2. Committee review and hearings
3. Floor debate and amendments
4. Voting in both legislative chambers
5. Executive approval (President/Governor signing)
6. Implementation and enforcement

### Types of Legislation:
- Public laws (apply to general public)
- Private laws (apply to specific individuals/entities)
- Statutes (written laws passed by legislative bodies)
- Regulations (rules created by administrative agencies)

### Legal Research Tips:
- Identify the jurisdiction (federal, state, local)
- Find the relevant code or statute
- Check for amendments and current status
- Review related case law interpretations""",
        "resources": [
            "https://www.congress.gov/",
            "https://www.legislation.gov.uk",
            "https://www.law.cornell.edu/wex/legislation"
        ]
    },
    ("employment", "labor", "workplace", "worker", "employee"): {
        "info": """## Employment Law
        
Employment law governs the relationship between employers and employees, covering rights and obligations in the workplace.

### Key Employment Law Areas:
1. Hiring and firing practices
2. Workplace safety and health
3. Wages and hours
4. Benefits and leave
5. Discrimination and harassment
6. Workers' compensation
7. Unions and collective bargaining

### Worker Rights:
- Minimum wage and overtime pay
- Safe working conditions
- Freedom from discrimination
- Family and medical leave
- Reasonable accommodations for disabilities
- Right to organize and bargain collectively

### Common Employment Issues:
- Wrongful termination
- Workplace harassment
- Wage and hour violations
- Employment classification (employee vs. contractor)
- Non-compete agreements
- Whistleblower protection""",
        "resources": [
            "https://www.dol.gov/",
            "https://www.eeoc.gov/",
            "https://www.osha.gov/",
            "https://www.americanbar.org/groups/labor_law/"
        ]
    },
    ("immigration", "visa", "citizenship", "alien", "naturalization"): {
        "info": """## Immigration Law
        
Immigration law concerns the legal status of people entering and remaining in a country they are not citizens of.

### Immigration Categories:
1. Temporary visitors (tourists, students, business)
2. Employment-based immigration
3. Family-sponsored immigration
4. Humanitarian programs (asylum, refugee status)
5. Diversity visa lottery

### Key Immigration Processes:
- Visa applications
- Green card (permanent residency) process
- Naturalization (citizenship)
- Deportation/removal proceedings
- Immigration appeals

### Common Immigration Issues:
- Visa overstays
- Unauthorized employment
- Criminal convictions affecting immigration status
- Changes in immigration policies
- Documentation requirements""",
        "resources": [
            "https://www.uscis.gov/",
            "https://www.ice.gov/",
            "https://www.americanimmigrationcouncil.org/",
            "https://www.ailalawyer.com/"
        ]
    },
    ("will", "estate", "trust", "probate", "inheritance"): {
        "info": """## Estate Planning & Probate
        
Estate planning involves arranging for the management and disposal of a person's estate during their life and after death.

### Estate Planning Documents:
1. Last Will and Testament (directs distribution of assets)
2. Trusts (hold and manage assets)
3. Power of Attorney (financial and legal decisions)
4. Healthcare Directive (medical decisions)
5. Beneficiary Designations

### Probate Process:
- Filing the will with probate court
- Inventorying assets
- Paying debts and taxes
- Distributing remaining assets
- Closing the estate

### Types of Trusts:
- Revocable living trusts
- Irrevocable trusts
- Special needs trusts
- Charitable trusts
- Spendthrift trusts""",
        "resources": [
            "https://www.americanbar.org/groups/real_property_trust_estate/resources/estate_planning/",
            "https://www.nolo.com/legal-encyclopedia/wills-trusts-estates",
            "https://www.findlaw.com/estate.html"
        ]
    },
    ("bankruptcy", "debt", "insolvency", "creditor", "debtor"): {
        "info": """## Bankruptcy Law
        
Bankruptcy is a legal process designed to help individuals and businesses eliminate or repay debts under the protection of the bankruptcy court.

### Types of Bankruptcy:
1. Chapter 7 (Liquidation)
   - Discharge of most unsecured debts
   - Sale of non-exempt assets to pay creditors
   
2. Chapter 13 (Reorganization for Individuals)
   - Repayment plan over 3-5 years
   - Keep most assets while repaying debts
   
3. Chapter 11 (Business Reorganization)
   - Allows businesses to continue operating
   - Restructuring of debts

### Bankruptcy Process:
- Credit counseling requirement
- Filing petition and schedules
- Meeting of creditors
- Discharge of eligible debts
- Closure of case

### Bankruptcy Effects:
- Automatic stay (stops collections)
- Impact on credit score
- Potential loss of assets
- Relief from overwhelming debt""",
        "resources": [
            "https://www.uscourts.gov/services-forms/bankruptcy",
            "https://www.americanbar.org/groups/business_law/resources/business_bankruptcy/",
            "https://www.nolo.com/legal-encyclopedia/bankruptcy"
        ]
    },
    ("personal injury", "tort", "liability", "negligence", "damages"): {
        "info": """## Personal Injury Law
        
Personal injury law allows individuals to seek compensation when they're harmed due to someone else's negligence or intentional acts.

### Common Personal Injury Cases:
1. Car accidents
2. Slip and fall incidents
3. Medical malpractice
4. Product liability
5. Workplace injuries
6. Dog bites
7. Defamation (libel/slander)

### Elements of Negligence:
- Duty of care
- Breach of duty
- Causation
- Damages

### Types of Damages:
- Economic (medical bills, lost wages, property damage)
- Non-economic (pain and suffering, emotional distress)
- Punitive (to punish egregious behavior)

### Important Considerations:
- Statute of limitations (time limits to file)
- Comparative/contributory negligence
- Insurance coverage
- Settlement negotiations""",
        "resources": [
            "https://www.americanbar.org/groups/tort_trial_insurance_practice/",
            "https://www.alllaw.com/articles/nolo/personal-injury.html",
            "https://www.nolo.com/legal-encyclopedia/accident-law"
        ]
    }
}

# --- Helper Function ---
def find_response(user_input):
    user_input_lower = user_input.lower()
    
    # Check for greetings or intro questions
    greetings = ["hi", "hello", "hey", "greetings", "howdy"]
    if any(greeting == user_input_lower.strip() for greeting in greetings) or "what can you" in user_input_lower:
        return {
            "info": """Hello! I'm your legal assistant chatbot. I can provide information on various legal topics including:

1. Contract law
2. Divorce and family law
3. Property law
4. Criminal law
5. Tax law
6. Intellectual property
7. Employment law
8. Immigration law
9. Estate planning
10. Bankruptcy
11. Personal injury

Ask me about any of these topics by typing questions like "Tell me about contracts" or "How does bankruptcy work?"
""",
            "resources": []
        }
    
    # Check for "thank you" messages
    if any(thanks in user_input_lower for thanks in ["thank you", "thanks", "thx"]):
        return {
            "info": "You're welcome! Feel free to ask if you have any other legal questions.",
            "resources": []
        }
    
    # Check knowledge base for matching topics
    for keywords, data in knowledge_base.items():
        if any(keyword in user_input_lower for keyword in keywords):
            return data

    # Special Act name detection
    match = re.search(r"(?:the\s+)?([\w\s]+?)\s+(act|law|statute)(?:\s+of\s+(\d{4}))?", user_input_lower)
    if match:
        act_name = match.group(1).strip().title()
        act_type = match.group(2)
        year = match.group(3) if match.group(3) else ""
        # Find the legislation section
        legislation_info = None
        for keywords, data in knowledge_base.items():
            if "act" in keywords or "law" in keywords or "statute" in keywords or "legislation" in keywords:
                legislation_info = data
                break
        
        if legislation_info:
            return {
                "info": f"""## {act_name} {act_type.title()} {year}

I don't have specific information about the {act_name} {act_type.title()} {year}. Here are some suggestions:

1. Search for the full text on government legislation websites
2. Look for legal analyses on legal research platforms
3. Check for summaries on legal education websites
4. Consult with a lawyer who specializes in the relevant area of law""",
                "resources": legislation_info['resources']
            }

    # If no match found
    return {
        "info": """I don't have specific information about that legal topic yet. Here are some suggestions:

1. Try rephrasing your question with more specific legal terms
2. Ask about one of these topics: contracts, divorce, property, criminal law, tax, intellectual property, employment, immigration, estate planning, bankruptcy, or personal injury
3. For specialized legal advice, consider consulting with a qualified attorney""",
        "resources": [
            "https://www.americanbar.org/groups/legal_services/flh-home/flh-free-legal-help/",
            "https://www.findlaw.com/",
            "https://www.nolo.com/legal-encyclopedia"
        ]
    }