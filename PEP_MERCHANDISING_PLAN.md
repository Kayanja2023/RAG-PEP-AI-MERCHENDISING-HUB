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

**Status:** Implementation plan ready  
**Branch:** feature/experimental-changes  
**Decision Point:** Customer-facing retail OR internal merchandising tool?

---

# IMPLEMENTATION PLAN: PEP Merchandising Assistant

## Executive Summary

**Project Goal:** Transform Hollard Policy Assistant into internal PEP Merchandising Assistant  
**Timeline:** 4 weeks to pilot deployment  
**Effort:** ~60-80 hours development + content creation  
**Branch Strategy:** feature/experimental-changes → feature/pep-merchandising  

---

## Phase 1: Foundation & Research (Week 1)

### Day 1-2: Environment Setup
**Tasks:**
- [ ] Create new sub-branch: `feature/pep-merchandising`
- [ ] Backup current experimental branch state
- [ ] Document baseline (Hollard version metrics)
- [ ] Set up local testing environment

**Commands:**
```bash
git checkout feature/experimental-changes
git checkout -b feature/pep-merchandising
git push -u origin feature/pep-merchandising
```

**Deliverables:**
- Clean branch for merchandising implementation
- Baseline documentation
- Development environment ready

---

### Day 3-5: Knowledge Base Content Creation

**Document 1: pep-vendor-directory.md** (~3,000 words)
- [ ] Research South African clothing/footwear suppliers
- [ ] Structure: Category → Suppliers → Contact details
- [ ] Include: Lead times, payment terms, MOQs
- [ ] Add performance ratings framework
- [ ] Create sample vendor profiles (5-10 realistic examples)

**Document 2: pep-buying-procedures.md** (~2,500 words)
- [ ] Map purchase order workflow (flowchart)
- [ ] Define approval hierarchies by amount
- [ ] Document sample evaluation process
- [ ] Include costing formulas
- [ ] Create negotiation guidelines
- [ ] Add contract templates/checklists

**Time Allocation:** 16-20 hours content creation

**Quality Check:**
- [ ] Technical accuracy review
- [ ] Language appropriate for buyers/merchandisers
- [ ] Includes actionable procedures
- [ ] Contains specific examples and calculations

---

### Day 6-7: Remaining Knowledge Base Documents

**Document 3: pep-merchandising-guidelines.md** (~3,000 words)
- [ ] Assortment planning frameworks
- [ ] Size curve matrices by category
- [ ] Seasonal buying calendars
- [ ] Markdown policies and timing
- [ ] Store grading methodology

**Document 4: pep-pricing-margins.md** (~2,500 words)
- [ ] Target margins by category (tables)
- [ ] Markup vs. margin explanations
- [ ] Landed cost calculation examples
- [ ] Promotional pricing guidelines
- [ ] Competitive positioning strategies

**Document 5: pep-performance-benchmarks.md** (~2,000 words)
- [ ] KPI definitions (stock turn, GMROI, sell-through)
- [ ] Industry benchmarks by category
- [ ] Historical performance templates
- [ ] Quality standards and thresholds

**Document 6: pep-compliance-standards.md** (~2,000 words)
- [ ] SA product safety regulations
- [ ] Labeling requirements (SABS standards)
- [ ] Ethical sourcing policy framework
- [ ] Import/export documentation guide
- [ ] Restricted substances list

**Time Allocation:** 20-24 hours

**Quality Check:**
- [ ] All 6 documents completed
- [ ] Consistent formatting across documents
- [ ] Cross-references between documents work
- [ ] Total word count: ~15,000 words
- [ ] Ready for FAISS indexing

---

## Phase 2: UI & Branding (Week 2)

### Day 8-9: Visual Design Updates

**app.py Modifications:**

**Task 1: Update Page Configuration**
```python
st.set_page_config(
    page_title="PEP Merchandising Assistant",
    page_icon="📊",
    layout="wide"
)
```

**Task 2: Color Scheme Rebrand**
- [ ] Change primary color: Hollard purple → PEP red (#E30613)
- [ ] Add secondary: Corporate blue (#1E3A8A)
- [ ] Update CSS variables in add_styling()
- [ ] Modify button colors, borders, highlights

**Task 3: Header Redesign**
- [ ] Replace Hollard logo/text with "PEP Merchandising Assistant"
- [ ] Update tagline: "Your Merchandising Knowledge Hub"
- [ ] Change icon from 🛡️ to 📊
- [ ] Adjust sizing for professional dashboard feel

**Task 4: Welcome Screen Customization**
- [ ] Rewrite welcome message for internal users
- [ ] Update card icons and titles:
  - 📊 Performance Data
  - 📦 Vendor Information
  - 📋 Procedures & Policies
  - 💰 Pricing & Margins
- [ ] Remove customer-facing language

**Estimated Changes:** 150-200 lines in app.py

**Testing Checklist:**
- [ ] All colors updated (no purple remnants)
- [ ] Responsive design maintained
- [ ] Professional corporate aesthetic
- [ ] Icons render correctly
- [ ] Welcome cards display properly

---

### Day 10-11: Functional Modifications

**Task 5: Remove Handover Mechanism**
- [ ] Delete or comment out `check_handover_needed()` function
- [ ] Remove `show_handover_end()` function
- [ ] Delete handover trigger detection from chat loop
- [ ] Clean up session state variables (handover_triggered)

**Task 6: Add Internal Contacts Section**
```python
def show_internal_contacts():
    st.info("""
    **Need Additional Support?**
    
    📞 Buying Manager: Ext 2401
    📞 Merchandising Head: Ext 2405
    📞 Planning Director: Ext 2410
    📧 Email: merchandising@pep.co.za
    💼 PEP Intranet: [Internal Link]
    """)
```
- [ ] Add to sidebar or footer
- [ ] Style consistently with new theme
- [ ] Make contacts easily accessible

**Task 7: Authentication (Optional)**
- [ ] Implement simple password check
- [ ] Add session state for authenticated users
- [ ] Create access code validation
- [ ] Design login screen
- [ ] Add disclaimer about demo/POC status

**Sample Implementation:**
```python
if "authenticated" not in st.session_state:
    st.title("🔐 PEP Merchandising Assistant")
    st.info("**Demo Version** - Internal Knowledge Base")
    password = st.text_input("Enter access code:", type="password")
    
    if password == "pep_merch_2025":  # Production: use secure auth
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.error("Invalid access code")
    st.stop()
```

**Testing Checklist:**
- [ ] Handover logic completely removed
- [ ] No session-ending behavior
- [ ] Internal contacts visible and styled
- [ ] Authentication works (if implemented)
- [ ] No errors in console

---

## Phase 3: RAG Engine & System Prompt (Week 3)

### Day 12-13: Knowledge Base Integration

**Task 8: Clear Old Knowledge Base**
```bash
# Backup Hollard documents
mkdir -p data/documents_backup/hollard
cp data/documents/*.md data/documents_backup/hollard/

# Remove old documents
rm data/documents/hollard-*.md
rm data/documents/life-insurance-basics.md
rm data/documents/claims-process.md
rm data/documents/about-hollard.md
```

**Task 9: Add New PEP Documents**
- [ ] Move 6 new .md files to `data/documents/`
- [ ] Verify file naming consistency (pep-vendor-directory.md, etc.)
- [ ] Update README.md in documents folder
- [ ] Check file permissions

**Task 10: Rebuild FAISS Index**
```bash
# Delete old index
rm -rf data/faiss_store/

# Run Python script to rebuild
python
>>> from rag_engine import build_knowledge_base
>>> build_knowledge_base()
```

**Testing:**
- [ ] FAISS index rebuilt successfully
- [ ] New embeddings generated
- [ ] Index size appropriate (~15,000 words)
- [ ] Test retrieval with sample query

---

### Day 14-16: System Prompt Transformation

**rag_engine.py Modifications:**

**Task 11: Replace System Prompt**

**Current (Hollard):**
```
You are a friendly and knowledgeable insurance assistant...
representing Hollard South Africa...
```

**New (PEP Merchandising):**
```python
system_prompt = """
You are an internal assistant for PEP's Merchandising, Buying, and Planning teams.

**Your Role:**
Provide quick, accurate answers about:
- Vendor information and supplier contacts
- Buying procedures and approval workflows
- Merchandising guidelines and best practices
- Pricing strategies, margins, and calculations
- Performance benchmarks and KPIs
- Compliance standards and regulatory requirements

**Your Users:**
- Buyers (sourcing products, negotiating with suppliers)
- Merchandisers (assortment planning, inventory management)
- Planners (demand forecasting, stock allocation)
- Category Managers (strategy, pricing, margins)

**Response Guidelines:**
1. Be professional and precise
2. Include specific numbers, percentages, formulas when available
3. Use retail/merchandising terminology appropriately
4. Reference internal policies and procedures from the knowledge base
5. For calculations, show formulas and worked examples
6. When information requires real-time data: "Check [System] for current figures"
7. When approval needed: "Requires sign-off from [Role/Manager]"
8. For system tasks: "Use [Software] to complete this action"

**Tone:** Professional, data-focused, technically accurate
**Context:** Internal PEP company tool - users are authenticated employees
**Confidentiality:** All information is internal company knowledge

When you don't have specific information, acknowledge gaps and direct users to:
- Relevant department contacts
- Company intranet resources
- Appropriate manager for approval
"""
```

**Task 12: Remove Handover Detection**
- [ ] Delete handover trigger keywords list
- [ ] Remove handover detection logic from response processing
- [ ] Clean up related helper functions

**Task 13: Update Response Post-Processing**
- [ ] Remove "would you like to speak to an agent" additions
- [ ] Keep technical, factual responses only
- [ ] Add internal contact references where appropriate

**Testing:**
- [ ] System prompt loaded correctly
- [ ] Responses are professional and technical
- [ ] No handover suggestions appear
- [ ] Tone matches internal user expectations

---

### Day 17: Query Testing & Refinement

**Task 14: Test Query Scenarios**

**Vendor Queries:**
- [ ] "Who supplies our school uniforms?"
- [ ] "What's the lead time for footwear from Supplier X?"
- [ ] "Show me contact details for ladies' clothing vendors"

**Expected Response Quality:**
- Specific vendor names
- Contact details (phone, email)
- Lead times in days
- Payment terms
- Performance ratings

**Procedure Queries:**
- [ ] "How do I create a purchase order?"
- [ ] "What's the approval limit for senior buyers?"
- [ ] "Explain the markdown authorization process"

**Expected Response Quality:**
- Step-by-step workflows
- Approval hierarchies
- Specific thresholds/limits
- System names referenced

**Calculation Queries:**
- [ ] "How do I calculate landed cost?"
- [ ] "What's our target margin for footwear?"
- [ ] "Show me markup formula"

**Expected Response Quality:**
- Formulas clearly stated
- Worked examples with numbers
- Component breakdowns
- Industry context

**Performance Queries:**
- [ ] "What's a good stock turn rate?"
- [ ] "Show me KPIs for clothing category"
- [ ] "What was last season's sell-through?"

**Expected Response Quality:**
- Specific benchmarks
- Historical context
- Category-specific data
- Calculation methods

**Compliance Queries:**
- [ ] "What info is required on clothing labels?"
- [ ] "Explain ethical sourcing policy"
- [ ] "What documents needed for importing?"

**Expected Response Quality:**
- Regulatory requirements
- Specific standards (SABS, etc.)
- Documentation lists
- Compliance procedures

**Task 15: Response Refinement**
- [ ] Identify gaps in knowledge base
- [ ] Add missing information to documents
- [ ] Adjust system prompt if needed
- [ ] Fine-tune retrieval parameters (top_k, similarity threshold)

---

## Phase 4: Testing & Deployment (Week 4)

### Day 18-19: Comprehensive Testing

**Task 16: Functional Testing**
- [ ] Test all major query types (20+ queries)
- [ ] Verify accurate retrieval from knowledge base
- [ ] Check response quality and tone
- [ ] Test edge cases (unknown questions, gibberish)
- [ ] Validate internal contacts display
- [ ] Test authentication (if implemented)
- [ ] Check "Clear Chat" functionality
- [ ] Verify no handover behavior

**Task 17: UI/UX Testing**
- [ ] Cross-browser testing (Chrome, Edge, Firefox)
- [ ] Mobile responsiveness check
- [ ] Color contrast validation (accessibility)
- [ ] Loading times acceptable
- [ ] No console errors
- [ ] Proper error handling

**Task 18: Content Accuracy Review**
- [ ] Have SME review sample responses (if available)
- [ ] Verify calculations are correct
- [ ] Check terminology accuracy
- [ ] Validate procedure descriptions
- [ ] Ensure no misleading information

**Testing Documentation:**
- [ ] Create test case spreadsheet
- [ ] Document bugs/issues found
- [ ] Track resolution of issues
- [ ] Prepare user acceptance testing plan

---

### Day 20-21: Deployment Preparation

**Task 19: Documentation Updates**

**README.md:**
- [ ] Update project title and description
- [ ] Change use case from insurance to merchandising
- [ ] Update screenshot (if applicable)
- [ ] Revise installation instructions
- [ ] Update environment variable section
- [ ] Add authentication details (if implemented)
- [ ] Change deployment context

**DOCUMENTATION.md:**
- [ ] Update technical overview
- [ ] Revise architecture description
- [ ] Update knowledge base structure
- [ ] Change user personas
- [ ] Modify use cases and examples
- [ ] Update testing section

**requirements.txt:**
- [ ] Verify all dependencies current
- [ ] Remove unused packages
- [ ] Add any new dependencies
- [ ] Test fresh install

**Task 20: Add Disclaimers**
- [ ] Add "Demo/POC" notice to UI
- [ ] Include data accuracy disclaimer
- [ ] Note it's not connected to live systems
- [ ] Add "for reference only" messaging

**Example Disclaimer:**
```python
st.warning("""
**⚠️ Demo Version**  
This is a proof-of-concept knowledge base assistant. 
It is not connected to live PEP systems or real-time data.
For production use, verify all information with official sources.
""")
```

---

### Day 22: Deployment

**Task 21: Choose Deployment Strategy**

**Option A: Streamlit Cloud (Public with Password)**
```bash
# Create .streamlit/secrets.toml
[general]
OPENAI_API_KEY = "sk-..."
ACCESS_CODE = "pep_merch_2025"
```

Steps:
- [ ] Create Streamlit Cloud account
- [ ] Connect GitHub repository
- [ ] Select branch: feature/pep-merchandising
- [ ] Add secrets (API key, access code)
- [ ] Configure custom subdomain
- [ ] Deploy and test

**Option B: Local Network (Company Deployment)**
- [ ] Prepare deployment package
- [ ] Create installation guide for IT team
- [ ] Document server requirements
- [ ] Provide configuration instructions
- [ ] Include troubleshooting guide

**Option C: Docker Container (Portable)**
- [ ] Create Dockerfile
- [ ] Build and test container
- [ ] Document docker-compose setup
- [ ] Provide deployment instructions

**Task 22: Post-Deployment Verification**
- [ ] Test deployed version thoroughly
- [ ] Verify API key working
- [ ] Check authentication (if applicable)
- [ ] Test all major features
- [ ] Monitor for errors
- [ ] Performance check (response times)

---

### Day 23-24: Pilot Testing & Refinement

**Task 23: Pilot User Testing**
- [ ] Identify 5-10 pilot users (if possible)
- [ ] Provide access credentials
- [ ] Create feedback form/survey
- [ ] Monitor usage patterns
- [ ] Collect qualitative feedback
- [ ] Track common queries

**Feedback Areas:**
- Response accuracy (1-5 scale)
- Response completeness (1-5 scale)
- Ease of use (1-5 scale)
- Tone appropriateness (1-5 scale)
- Missing information (open text)
- Improvement suggestions (open text)

**Task 24: Iteration Based on Feedback**
- [ ] Analyze feedback themes
- [ ] Prioritize improvements
- [ ] Update knowledge base documents
- [ ] Refine system prompt
- [ ] Fix bugs/issues
- [ ] Improve response quality

**Task 25: Final Documentation**
- [ ] Create user guide (how to use)
- [ ] Document common queries
- [ ] Provide troubleshooting tips
- [ ] Include feedback mechanism
- [ ] Add FAQ section

---

## Phase 5: Handover & Maintenance (Post-Week 4)

### Task 26: Project Handover Package

**Deliverables:**
- [ ] Complete source code (GitHub repository)
- [ ] Knowledge base documents (6 .md files)
- [ ] Technical documentation (README, DOCUMENTATION)
- [ ] User guide
- [ ] Test cases and results
- [ ] Deployment guide
- [ ] Maintenance procedures

**Documentation Structure:**
```
/docs
  /user-guide.md          # How to use the assistant
  /admin-guide.md         # How to update knowledge base
  /deployment-guide.md    # How to deploy/configure
  /maintenance-plan.md    # Update schedule, procedures
  /troubleshooting.md     # Common issues and fixes
```

---

### Task 27: Maintenance Plan

**Monthly Tasks:**
- [ ] Review usage analytics
- [ ] Check for outdated information
- [ ] Update vendor contact details
- [ ] Refresh performance benchmarks
- [ ] Add new procedures as needed

**Quarterly Tasks:**
- [ ] Major knowledge base review
- [ ] Update with new policies
- [ ] Refine system prompt based on usage
- [ ] Performance optimization
- [ ] Security review

**Annual Tasks:**
- [ ] Complete content audit
- [ ] Major version upgrade
- [ ] Competitive analysis
- [ ] User satisfaction survey
- [ ] ROI assessment

---

## Resource Requirements

### Development Time Estimate

| Phase | Tasks | Hours |
|-------|-------|-------|
| Phase 1: Foundation & Research | Setup + 6 KB documents | 36-44h |
| Phase 2: UI & Branding | Design + Functional changes | 12-16h |
| Phase 3: RAG Engine | System prompt + Testing | 8-12h |
| Phase 4: Testing & Deployment | QA + Deployment | 12-16h |
| **Total Development** | | **68-88h** |

**Timeline:** 4 weeks (assuming 20h/week) = 80 hours total

---

### Technical Resources

**Required:**
- Python 3.11+ environment
- OpenAI API access (GPT-4)
- Git/GitHub account
- Streamlit Cloud account (for deployment)
- Code editor (VS Code)

**Optional:**
- Docker (for containerization)
- Company network access (for intranet deployment)
- SME access (for content validation)

---

### Budget Estimate

| Item | Cost |
|------|------|
| OpenAI API Usage (development + testing) | ~$20-40 |
| Streamlit Cloud Hosting (free tier) | $0 |
| Domain/SSL (if custom) | $10-20/year |
| **Total Development Budget** | **$20-60** |

**Note:** Production deployment may require:
- Company infrastructure (internal cost)
- Ongoing API usage (varies by volume)
- Maintenance time allocation

---

## Risk Management

### Risk 1: Content Accuracy
**Risk:** Information may not reflect actual PEP procedures  
**Impact:** High - Users may make incorrect decisions  
**Mitigation:**
- Add clear disclaimers (demo/POC status)
- Include version dates on all documents
- Recommend verification with official sources
- Partner with PEP for production version

### Risk 2: Lack of Real Data
**Risk:** Generic benchmarks may not match PEP specifics  
**Impact:** Medium - Reduced usefulness  
**Mitigation:**
- Use industry-standard benchmarks
- Clearly label as "typical" or "industry average"
- Offer to customize with real data if access granted
- Position as training/reference tool

### Risk 3: Authentication Security
**Risk:** Simple password may be bypassed  
**Impact:** Low (for demo), High (for production)  
**Mitigation:**
- Use strong password for demo
- Recommend SSO/proper auth for production
- Add logging of access attempts
- Regular password rotation

### Risk 4: API Cost Overruns
**Risk:** Unexpected high usage during pilot  
**Impact:** Low-Medium - Budget exceeded  
**Mitigation:**
- Set OpenAI usage limits
- Monitor daily API costs
- Implement rate limiting
- Cache common queries

### Risk 5: Low Adoption
**Risk:** Users don't find tool useful  
**Impact:** Medium - Wasted development effort  
**Mitigation:**
- Involve users early (pilot testing)
- Collect and act on feedback quickly
- Provide training/demos
- Show clear value proposition

---

## Success Criteria

### Functional Success
- [ ] All 6 knowledge base documents created (15,000+ words)
- [ ] UI fully rebranded (PEP colors, professional aesthetic)
- [ ] Handover mechanism removed
- [ ] Internal contacts displayed
- [ ] System prompt updated for merchandising context
- [ ] Authentication implemented (if required)
- [ ] Deployed and accessible

### Quality Success
- [ ] 90%+ response accuracy on test queries
- [ ] Average response time < 5 seconds
- [ ] No critical bugs or errors
- [ ] Positive feedback from pilot users (4+/5 rating)
- [ ] Professional tone maintained in all responses
- [ ] Technical terminology used correctly

### Documentation Success
- [ ] Complete technical documentation
- [ ] User guide created
- [ ] Deployment guide provided
- [ ] Maintenance plan documented
- [ ] Test results recorded

### Business Success
- [ ] Time saved vs. manual lookups (measurable)
- [ ] User satisfaction (survey results)
- [ ] Potential for production deployment (stakeholder interest)
- [ ] Portfolio-ready demonstration piece

---

## Next Actions

**Immediate (This Week):**
1. [ ] Review and approve this implementation plan
2. [ ] Decide: Demo version OR pursue PEP partnership
3. [ ] Create feature/pep-merchandising branch
4. [ ] Begin Phase 1: Knowledge base content creation

**Decision Point:**
- **Option A:** Build demo with generic industry data (2-3 weeks)
- **Option B:** Partner with PEP for authentic version (4-6 weeks + partnership)
- **Option C:** Build both customer-facing AND merchandising tools (6-8 weeks)

**Recommended:** Start with **Option A (Demo)** to validate concept, then approach PEP with working prototype.

---

**Status:** Implementation plan complete  
**Next Step:** User decision on approach + begin Phase 1  
**Estimated Completion:** 4 weeks from start date
