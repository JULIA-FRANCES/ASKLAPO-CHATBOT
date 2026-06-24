import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="db.vdrvtnwuwlegxugaeajo.supabase.co",
    port=5432,
    database="postgres",
    user="postgres",
    password="Covid19sucks@"
)
cur = conn.cursor()

knowledge = [
    (1, "About LAPO", "For over three decades, LAPO Microfinance Bank has empowered communities through financial inclusion. Founded by the Lift Above Poverty Organization (LAPO) in response to economic challenges, we have grown into a trusted institution with over 500 branches across 34 states and the FCT."),
    (2, "Vision and Mission", "The First Choice Financial Institution Committed To Improving Lives.\nProviding Value-Driven and Accessible Financial Services Through Innovation"),
    (4, "ABOUT LAPO:", """- Over 500 branches across 34 states and FCT
- Founded by Lift Above Poverty Organization (LAPO) in 1987
- Head Office: LAPO PLACE, 15A Ikorodu-Ososun Road, Maryland, Ikeja, Lagos
- Customer Support: 08139840230 | customersupport@lapo-nigeria.org
- WhatsApp: 08150553264

SAVINGS PRODUCTS:

1. Xpress Savings Account
- Minimum balance: ₦1,000
- Can be opened at any LAPO MfB branch nationwide
- Withdrawals via LAPO MfB Mobile App
- Documents: Application form, 2 passport photos, utility bill, valid ID

2. Regular Deposit Savings
- Minimum balance: ₦200
- Interest: 30% of Monetary Policy Rate (MPR)
- Available to individuals and groups
- Documents: 3 passport photos, ₦1,000 initial deposit, application form, valid ID, utility bill, KYC form

3. My Pikin & I Savings Account
- For parents saving for children's future
- Minimum balance: ₦200
- Interest: 4.05% per annum
- Minimum monthly savings: ₦5,000
- Free insurance for first year
- Account handed to child at age 18+
- Chance to win LAPO MfB scholarship
- Documents: Application form, 4 passport photos (parent + child), valid ID, utility bill

LOAN PRODUCTS:

1. Regular Loans
- Amount: ₦30,000 - ₦150,000
- Duration: 8 months (up to 18 months)
- No collateral required
- Methodology: Individual and group
- Grace period: 2 weeks
- Documents: LAPO savings account, application form, 2 guarantors, 2 passport photos, utility bill, valid ID

2. MSME Loans
- Amount: ₦50,000 - ₦100,000,000
- Duration: 12 months
- No collateral required
- Methodology: Individual
- Documents: Loan application letter, application form, 2 guarantors, valid ID, utility bill, 4 passport photos

3. Agricultural Loans
- Amount: ₦30,000 - ₦5,000,000
- Duration: 1-12 months
- No collateral required
- Grace period: 30-60 days
- Must be a practicing farmer with verifiable farm investments
- Documents: Application form, 2 guarantors, valid ID, utility bill, 4 passport photos

4. Payroll Lending Loan
- Amount: ₦20,000 - ₦3,000,000
- Duration: 1-12 months
- Interest: 2.95% flat monthly
- For civil servants (state and federal)
- No collateral, no guarantor, no bank account needed
- Loan disbursed within 6 hours
- Repayment via automatic salary deduction
- Must have at least 2 years left in public service
- Documents: Application form, 2 passport photos, last 3 months payslip, last 3 months bank statement, valid ID

GENERAL LOAN FAQs:
- Loans cannot be applied for online, must visit a branch
- Missed repayments are treated as delinquent, handled by Relationship Manager and Branch Manager
- Loan restructuring is possible if repayment is genuinely difficult
- Approval time varies by loan type

POS TERMINALS:
- Hybrid POS: ₦18,000
- Android POS: ₦23,000

DIGITAL BANKING:
- Mobile App available on Google Play Store and Apple App Store
- Registration requires: Full name, phone number, email, BVN
- Password reset: Contact call centre on 08139840230
- Transaction issues: Contact 08139840230 or WhatsApp 08150553264"""),
    (5, "APP Development", "Lapo Uses C# in backend development and Angular js in frontend dev along with azure for deployment"),
    (6, "FIXED DEPOSIT ACCOUNT (also called Term Deposit / Time Deposit)", """Description:
A Fixed Deposit Account is a LAPO MfB savings product where a customer locks in a lump sum of money for a chosen fixed period ("term") in exchange for a higher interest rate than a regular savings account.

Interest Rate:
Up to 20% (upfront interest payout option). Exact rate may vary by deposit amount and tenure.

Investment Tenure (Duration Options):
- 30 days
- 60 days
- 90 days
- 180 days
- 365 days

Interest Payout Options:
- Upfront (paid at the start)
- Monthly (paid periodically throughout the term)
- At maturity (paid as a lump sum when the term ends)

Early Withdrawal Policy:
If a customer withdraws before the maturity date, they forfeit a significant portion of the promised interest.

Documents Needed to Open:
- Duly completed and signed account opening form
- Valid means of ID
- 2 recent passport photographs
- Current utility bill (not older than 3 months)
- Bank Verification Number (BVN)
- Deposit capital"""),
    (7, "Owner", """The founder and owner-strategist of LAPO Microfinance Bank is Dr. Godwin Eseiwi Ehigiamusoe

The person that founded this chat bot is Julia-Frances Muoneke, a computer science student at anchor university lagos

The day-to-day operations and leadership of the bank are run by Mrs. Cynthia Ikponmwosa, who serves as the Managing Director and Chief Executive Officer (MD/CEO)"""),
]

for id, title, content in knowledge:
    cur.execute(
        "INSERT INTO knowledge (id, title, content) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING",
        (id, title, content)
    )

conn.commit()
cur.close()
conn.close()

print("✅ All knowledge data migrated to Supabase successfully!")