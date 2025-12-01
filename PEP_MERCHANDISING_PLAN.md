# PEP Merchandising Department Assistant - Specialized Plan

**Target Users:** PEP Merchandising, Buying & Selling Teams  
**Purpose:** Internal tool for buyers, planners, and merchandisers  
**Branch:** feature/experimental-changes  

---

## Department Overview

### PEP Merchandising & Buying Teams

**Key Roles:**
- **Buyers** - Source products, negotiate with suppliers, manage vendor relationships
- **Merchandisers** - Plan product assortments, analyze sales data, manage inventory
- **Planners** - Forecast demand, allocate stock to stores, optimize distribution
- **Category Managers** - Oversee product categories, pricing strategies, margins

**Daily Activities:**
- Vendor negotiations and purchase orders
- Sales performance analysis
- Stock level monitoring
- Pricing and markdown decisions
- Seasonal planning and ranging
- Competitor analysis
- Margin management

---

## Use Case: Internal Merchandising Assistant

Instead of customer-facing retail assistant, create an **internal tool** that helps merchandising teams with:

### 1. Quick Reference Information
- Vendor contact details
- Product specifications and codes
- Pricing matrices and margin calculations
- Seasonal buying calendars
- Category performance benchmarks

### 2. Policy & Procedure Guidance
- Purchase order approval workflows
- Markdown authorization processes
- Vendor payment terms
- Quality control standards
- Stock allocation rules

### 3. Data Insights
- "What was last season's sell-through rate for winter jackets?"
- "Which suppliers deliver school uniforms?"
- "What's our standard margin for footwear?"

### 4. Compliance & Standards
- Ethical sourcing requirements
- Product safety standards
- Labeling regulations
- Import/export documentation

---

## Knowledge Base Structure

### Document 1: **pep-vendor-directory.md** (~3,000 words)

**Content:**
- Major clothing suppliers (South African and international)
- Footwear manufacturers
- Textile mills and fabric suppliers
- Cellphone and electronics vendors
- Homeware suppliers
- Contact details, lead times, payment terms
- Preferred vendor lists by category
- Vendor performance ratings

**Example Queries:**
- "Who supplies our ladies' denim?"
- "What's the lead time for school shoes from Supplier X?"
- "Show me our top 5 clothing vendors"

---

### Document 2: **pep-buying-procedures.md** (~2,500 words)

**Content:**
- Purchase order creation process
- Approval hierarchies and sign-off limits
- Sample evaluation procedures
- Costing and pricing formulas
- Negotiation guidelines
- Contract management
- Payment terms (30/60/90 days)
- Dispute resolution processes

**Example Queries:**
- "How do I create a PO for new supplier?"
- "What's the approval limit for a senior buyer?"
- "Explain the sample approval workflow"

---

### Document 3: **pep-merchandising-guidelines.md** (~3,000 words)

**Content:**
- Category planning principles
- Assortment planning frameworks
- Size curve ratios by category
- Color and style mix guidelines
- Seasonal buying calendars (back-to-school, winter, summer, festive)
- Store grading and allocation rules
- Markdown policies and timing
- End-of-season clearance procedures

**Example Queries:**
- "What's the standard size curve for men's pants?"
- "When should I start buying for back-to-school?"
- "Explain the markdown authorization process"

---

### Document 4: **pep-pricing-margins.md** (~2,500 words)

**Content:**
- Target margin percentages by category
- Pricing tiers (value, core, premium)
- Markup calculations and formulas
- Cost price components (landed cost, duties, freight)
- Promotional pricing guidelines
- Markdown percentage limits
- Competitive pricing strategies
- Price change procedures

**Example Queries:**
- "What's our target margin for ladies' tops?"
- "How do I calculate landed cost?"
- "What's the maximum markdown for footwear?"

---

### Document 5: **pep-performance-benchmarks.md** (~2,000 words)

**Content:**
- Sales KPIs by category
- Stock turn targets
- Sell-through rate benchmarks
- Gross margin return on investment (GMROI)
- Supplier performance metrics
- Quality standards and acceptable defect rates
- Customer return rate thresholds
- Historical sales data (seasonal trends)

**Example Queries:**
- "What's a good stock turn for clothing?"
- "What was last year's back-to-school performance?"
- "Show me quality standards for footwear"

---

### Document 6: **pep-compliance-standards.md** (~2,000 words)

**Content:**
- South African product safety regulations
- Labeling requirements (fiber content, care instructions)
- Ethical sourcing policy
- Factory audit standards
- Environmental compliance
- Import/export documentation
- Country of origin rules
- Restricted substances list

**Example Queries:**
- "What info is required on clothing labels?"
- "Explain our ethical sourcing policy"
- "What documents needed for importing from China?"

---

## Total Knowledge Base: ~15,000 words (6 documents)

---

## UI/UX Customization for Internal Users

### Branding Adjustments

**Color Scheme:**
- Keep PEP red (#E30613) for brand consistency
- Add **professional blue** (#1E3A8A) for corporate feel
- Gray tones for data/numbers (#4B5563)
- Clean, dashboard-like aesthetic

**Icon:** 
- 📊 (chart/data) or 📦 (inventory box) instead of shopping bag
- Represents analytics and supply chain

**Tagline:**
- "Your Merchandising Knowledge Hub"
- "PEP Buying & Planning Assistant"

**Page Title:**
- "PEP Merchandising Assistant" (instead of Store Assistant)

---

### Functional Differences from Customer Version

#### 1. **No Handover Mechanism Needed**
- Internal users = authenticated employees
- Remove session-ending handover
- Instead: "Contact [Department] for more details"
- Link to internal systems or colleagues

**Replace handover with:**
```
Need more details?
📞 Buying Manager: Ext 2401
📧 merchandising@pep.co.za
💼 Check PEP Intranet: [link]
```

#### 2. **Tone & Language**
**Customer Version:** Friendly, casual, enthusiastic  
**Internal Version:** Professional, precise, data-focused

**Example Differences:**
- Customer: "Great choice! That's a best seller!"
- Internal: "Historical data shows 87% sell-through rate in Q3"

- Customer: "We have amazing deals!"
- Internal: "Recommended markdown: 30% based on age of stock"

#### 3. **Response Style**
- Include specific numbers, percentages, codes
- Reference internal systems (ERP, WMS)
- Use industry terminology freely
- Provide calculation formulas when relevant

---

## System Prompt Modifications

### New System Prompt for Merchandising Context:

```
You are an internal assistant for PEP's Merchandising, Buying, and Planning teams.

Your role is to provide quick access to:
- Vendor information and contacts
- Buying procedures and workflows
- Merchandising guidelines and best practices
- Pricing strategies and margin calculations
- Performance benchmarks and KPIs
- Compliance standards and regulations

Users are PEP employees in:
- Buying (sourcing products, vendor management)
- Merchandising (assortment planning, inventory management)
- Planning (forecasting, allocation, distribution)

Response Guidelines:
- Be professional and precise
- Include specific data, percentages, and formulas when available
- Use retail/merchandising terminology
- Reference internal policies and procedures
- For complex calculations or system-specific tasks, direct to appropriate department or tool

When information requires:
- Real-time data access → "Check [System Name] for current figures"
- Manager approval → "Requires sign-off from [Role]"
- System functionality → "Use [Software] to complete this task"

Maintain confidentiality - this is internal company information.
```

---

## Welcome Screen for Internal Users

```markdown
### 👔 Welcome to PEP Merchandising Assistant

Quick access to buying, planning, and merchandising information

📊 **Performance Data**
KPIs, benchmarks, sales trends

📦 **Vendor Information**  
Contacts, lead times, terms

📋 **Procedures & Policies**
Buying workflows, approvals

💰 **Pricing & Margins**
Calculations, guidelines, targets
```

---

## Sample Query Types & Responses

### Query Type 1: Vendor Information
**User:** "Who supplies our school uniforms?"

**Response:**
```
PEP's main school uniform suppliers:

1. **Supplier A (Pty) Ltd**
   - Contact: John Smith, 011-555-1234
   - Lead time: 60 days
   - Payment terms: 60 days from delivery
   - Categories: Shirts, pants, dresses
   - Rating: 4.5/5 (quality & delivery)

2. **Supplier B Manufacturing**
   - Contact: Mary Jones, 021-555-5678
   - Lead time: 45 days
   - Payment terms: 30 days from delivery
   - Categories: Jerseys, blazers, ties
   - Rating: 4.2/5

For current pricing and availability, check PO System.
Need to onboard new supplier? Contact Buying Manager (Ext 2401).
```

---

### Query Type 2: Procedure Question
**User:** "How do I get approval for a markdown?"

**Response:**
```
PEP Markdown Approval Process:

**Step 1: Analysis**
- Stock age: >90 days
- Current stock level vs. forecast
- Competitor pricing check

**Step 2: Proposal**
- Recommended markdown %
- Expected sell-through impact
- Margin impact calculation

**Step 3: Approval Hierarchy**
- Up to 20%: Category Manager approval
- 20-40%: Buying Manager approval
- Over 40%: Head of Merchandising approval

**Step 4: Implementation**
- Submit via Pricing System
- Schedule activation date
- Communicate to stores via Store Ops

**Important:** Markdown must align with seasonal calendar.
Peak markdown periods: End Jan, End June, Nov-Dec.

Need urgent approval? Email markdown.approvals@pep.co.za
```

---

### Query Type 3: Technical Calculation
**User:** "How do I calculate landed cost?"

**Response:**
```
Landed Cost Calculation Formula:

**Landed Cost = FOB Cost + Freight + Duties + Other Costs**

Where:
- FOB Cost: Ex-factory price from supplier
- Freight: Sea/air shipping to SA
- Duties: Import tax (varies by HS code)
- Other: Insurance, clearance, warehousing

**Example Calculation:**
FOB Cost: R50.00 per unit
Freight: R5.00 per unit
Duty (20%): R11.00 (20% of R55.00)
Insurance: R1.00 per unit
**Total Landed Cost: R67.00**

**To determine sell price:**
Landed Cost × Target Margin % = Retail Price
R67.00 ÷ 0.60 (40% margin) = R111.67
Rounded retail: R119.99

Use PEP Costing Tool for automated calculations.
Need duty rates? Check SARS Import Schedule or ask Compliance team.
```

---

## Technical Implementation

### Code Changes Needed

**1. app.py - Update Configuration**
```python
st.set_page_config(
    page_title="PEP Merchandising Assistant",
    page_icon="📊",
    layout="wide"
)
```

**2. Remove Handover Logic**
```python
# Remove or simplify check_handover_needed()
# Replace show_handover_end() with internal contact info

def show_internal_contacts():
    st.info("""
    **Need Additional Help?**
    
    📞 Buying Manager: Ext 2401
    📞 Merchandising Head: Ext 2405
    📧 Email: merchandising@pep.co.za
    💼 Intranet: [internal link]
    """)
```

**3. Update Color Scheme**
```css
/* Professional internal tool aesthetic */
:root {
    --pep-red: #E30613;
    --pep-blue: #1E3A8A;
    --pep-gray: #4B5563;
}
```

**4. Authentication Consideration**
```python
# Optional: Add simple password protection
# Or integrate with company SSO (advanced)

if "authenticated" not in st.session_state:
    password = st.text_input("Enter access code:", type="password")
    if password == "pep_internal_2025":  # In production: use proper auth
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.error("Invalid access code")
    st.stop()
```

---

## Deployment Considerations

### Option 1: Company Intranet Deployment
- Host on internal servers
- Requires VPN access
- Integrated with company SSO
- Access to internal databases

### Option 2: Secure Cloud Deployment
- Streamlit Cloud with password protection
- Limited to knowledge base only (no live data)
- Proof of concept / training tool
- No sensitive real-time data

### Option 3: Local Network Only
- Run on company network
- No external access
- Most secure option
- May require IT setup

**Recommendation for POC:** Option 2 (secure cloud) with disclaimer that it's a knowledge reference tool, not connected to live systems.

---

## Success Metrics for Internal Tool

**Usage Metrics:**
- Number of queries per day
- Most asked questions
- User feedback ratings

**Efficiency Metrics:**
- Time saved vs. manual lookups
- Reduction in "how-to" emails
- Faster onboarding of new buyers

**Accuracy Metrics:**
- Correct answers to test queries
- User satisfaction scores
- Number of escalations to managers

---

## Content Creation Strategy

### Information Sources:

1. **Internal Documentation**
   - Existing procedure manuals
   - Buying guidelines
   - Training materials
   - Policy documents

2. **Subject Matter Experts**
   - Interview experienced buyers
   - Shadowing merchandising team
   - Capture tribal knowledge

3. **System Screenshots & Guides**
   - Annotated workflows
   - Decision trees
   - Calculation examples

4. **Industry Best Practices**
   - Retail merchandising standards
   - South African regulations
   - Benchmarking data

### Writing Approach:
- **Precise** - Exact numbers, codes, formulas
- **Actionable** - Step-by-step procedures
- **Referenced** - Link to source documents
- **Updated** - Version control for policy changes

---

## Comparison: Customer vs. Internal Version

| Aspect | Customer Assistant | Merchandising Assistant |
|--------|-------------------|------------------------|
| **Users** | General public | PEP employees only |
| **Tone** | Friendly, casual | Professional, technical |
| **Content** | Products, services, returns | Procedures, vendors, analysis |
| **Data** | General info | Specific metrics, formulas |
| **Handover** | To customer service | To relevant department |
| **Security** | Public | Password/auth protected |
| **Language** | Simple, accessible | Industry terminology |
| **Purpose** | Sales & support | Efficiency & knowledge sharing |

---

## Implementation Timeline

**Week 1: Research & Content**
- Gather internal documentation
- Interview 3-5 buyers/merchandisers
- Draft vendor directory
- Draft buying procedures document

**Week 2: Complete Knowledge Base**
- Finish remaining 4 documents
- Technical review by department heads
- Add calculations and examples
- Create sample query library

**Week 3: Development**
- Update UI/branding
- Modify system prompt
- Add/remove features (handover, auth)
- Local testing with sample team

**Week 4: Pilot & Refinement**
- Deploy to 10-15 pilot users
- Gather feedback
- Refine responses
- Add missing content
- Go-live decision

---

## Risk Mitigation

**Risk: Confidential Information Exposure**
- **Mitigation:** Password protect, disclaimer, no real-time data

**Risk: Outdated Information**
- **Mitigation:** Quarterly review process, version dating, change log

**Risk: Over-reliance on Tool**
- **Mitigation:** Position as "reference assistant" not decision-maker

**Risk: Lack of Adoption**
- **Mitigation:** Training sessions, champion users, management buy-in

---

## Next Steps

**Option A: Full Internal Tool**
- Requires company partnership
- Access to real documentation
- 4-6 week development
- Potential production deployment

**Option B: Demo/Portfolio Version**
- Generic merchandising knowledge
- Industry best practices
- Sample data only
- 2-3 week development
- Portfolio showcase piece

**Which approach should we take?**

---

**Status:** Specialized plan complete  
**Branch:** feature/experimental-changes  
**Decision Point:** Customer-facing retail OR internal merchandising tool?
