# PEP Store Assistant - Transformation Plan

**Current State:** Hollard Insurance Policy Assistant (RAG Chatbot)  
**Target State:** PEP Store Customer Assistant  
**Branch:** feature/experimental-changes  

---

## About PEP Stores

**PEP (Pepkor Economy Products)** is South Africa's largest single-brand retailer with 2,500+ stores across Southern Africa.

### What PEP Sells:
- Affordable clothing (men, women, children, babies)
- Shoes and accessories
- Cellphones and airtime
- Home textiles (bedding, towels, curtains)
- Basic homeware and kitchenware
- Financial services (PEP Money, insurance)

### Target Market:
- Budget-conscious South African families
- Low to middle-income consumers
- Value-for-money shoppers
- Mass market retail

### Customer Pain Points:
- Finding products in 2,500+ stores
- Understanding PEP Money services (money transfers, bill payments)
- Checking stock availability
- Store hours and locations
- Returns and exchange policies
- Layaway/lay-by information
- Current promotions and specials

---

## Transformation Strategy

### Phase 1: Research & Content Creation (Week 1-2)

**Knowledge Base Documents to Create:**

1. **pep-products-catalog.md** (~3,000 words)
   - Clothing categories (ladies, mens, kids, baby)
   - Footwear range
   - Cellphones and electronics
   - Home textiles
   - Seasonal products
   - Price ranges per category

2. **pep-services-guide.md** (~2,500 words)
   - PEP Money (money transfers, bill payments, prepaid services)
   - PEP Cell (airtime, data, SIM cards)
   - Layaway/lay-by plans
   - Gift vouchers
   - Returns and exchanges policy

3. **pep-store-policies.md** (~2,000 words)
   - Return policy (30 days with slip)
   - Exchange procedures
   - Layaway terms and conditions
   - Payment methods accepted
   - Store credit policies

4. **pep-faqs.md** (~2,000 words)
   - Store location queries
   - Trading hours
   - Product availability
   - Sizing guides
   - Online vs in-store shopping
   - Customer service contact info

5. **pep-promotions.md** (~1,500 words)
   - Current specials and deals
   - Seasonal sales
   - Loyalty programs
   - School uniform specials
   - Back-to-school campaigns

**Total Knowledge Base:** ~11,000 words

---

### Phase 2: UI/UX Rebranding (Week 2)

**Visual Identity Changes:**

**Current (Hollard):**
- Purple theme (#6B1E9E)
- Shield icon 🛡️
- Professional insurance aesthetic
- "Your Policy Knowledge Partner"

**New (PEP):**
- **Primary Color:** Bright Red (#E30613) - PEP's signature red
- **Secondary Color:** White (#FFFFFF)
- **Accent:** Black (#000000)
- **Icon:** 🛍️ or 👕 (shopping/clothing)
- **Tagline:** "Your PEP Shopping Assistant" or "Smart Shopping with PEP"

**Logo:**
- Replace Hollard logo with PEP logo
- Source: Official PEP branding (if accessible)
- Fallback: Text-based "PEP" in brand colors

**Typography:**
- Bold, accessible fonts (appeals to mass market)
- Slightly larger font sizes (readability for all ages)
- High contrast (red/white/black)

---

### Phase 3: Functional Modifications (Week 3)

**1. Handover Mechanism Changes**

**Current Triggers:**
- Insurance quotes
- Policy purchases
- Claims submissions

**New Triggers:**
- Stock availability checks ("Is this in stock at my local store?")
- Specific product inquiries ("Do you have size 10 school shoes?")
- Store directions ("How do I get to PEP Sandton?")
- Account-specific queries ("What's my layaway balance?")
- Complaints and issues

**Handover Contact Options:**
- **Phone:** PEP Customer Care: 0800 73 73 73 (toll-free)
- **WhatsApp:** PEP WhatsApp support line
- **Store Finder:** Link to https://www.pepstores.com/store-locator
- **Email:** customercare@pepstores.com

**2. Welcome Message Updates**

**New Welcome Cards:**
```
🛍️ Product Information
Browse clothing, shoes, homeware

🏪 Store Services
Layaway, PEP Money, returns

📍 Find Stores
2,500+ locations nationwide
```

**3. Chat Personality Adjustment**

**Current:** Professional, formal insurance advisor  
**New:** Friendly, helpful shopping assistant

**Tone Changes:**
- More casual language
- South African colloquialisms (appropriate use)
- Enthusiastic about deals and savings
- Empathetic to budget concerns

**Example Responses:**
- "Great choice! That's one of our best sellers!"
- "Looking for a bargain? Check our current specials..."
- "PEP has your back for affordable fashion!"

---

### Phase 4: Feature Enhancements (Week 4)

**Optional Advanced Features:**

1. **Store Locator Integration**
   - "Find nearest PEP store" button
   - Integration with Google Maps API
   - Store hours for specific locations

2. **Product Availability Status**
   - Integration with inventory API (if available)
   - "Likely in stock" vs "Call store to confirm" guidance

3. **Price Range Filters**
   - "Show me shoes under R200"
   - Budget-based product recommendations

4. **Promotion Alerts**
   - Highlight current deals in responses
   - Weekly specials integration

5. **Multi-language Support**
   - English (primary)
   - Afrikaans
   - Zulu, Xhosa (future phases)

---

## Technical Implementation Plan

### File Changes Required

**1. app.py**
```python
# Line 320: Update page config
st.set_page_config(
    page_title="PEP Store Assistant",
    page_icon="🛍️",
    layout="wide"
)

# Styling function: Replace purple with PEP red
--hollard-purple: #6B1E9E;  →  --pep-red: #E30613;

# Update all references:
- Hollard → PEP
- Policy Assistant → Store Assistant
- Shield icon → Shopping bag icon
```

**2. rag_engine.py**
```python
# Update system prompt (lines 88-127)
# Change from insurance advisor to retail assistant
# Focus on products, services, value-for-money

NEW_PROMPT = """You are a helpful PEP Store Assistant.
PEP is South Africa's largest value retailer with 2,500+ stores.

Your role:
- Help customers find affordable clothing, shoes, and homeware
- Explain PEP services (layaway, PEP Money, returns)
- Guide to store locations and hours
- Share current promotions and deals

When customers need:
- Specific stock checks → handover to store
- Account queries → handover to customer care
- Complaints → handover to support team

Be friendly, enthusiastic, and value-focused.
Use the knowledge base to provide accurate information."""
```

**3. config.py**
- No major changes needed
- Update file paths if renaming document folder

**4. data/documents/**
- Remove all Hollard markdown files
- Add 5 new PEP markdown files (as listed above)
- Update README.md in documents folder

**5. README.md**
- Update project description
- Change screenshots (once available)
- Update deployment URL
- Modify tech stack section (same tools)

**6. DOCUMENTATION.md**
- Update project overview
- Change use case from insurance to retail
- Update knowledge base content description

---

## Content Creation Approach

### Research Sources:
1. **Official PEP Website** (pepstores.com)
   - Products catalog
   - Services information
   - Store policies

2. **PEP Mobile App**
   - User experience patterns
   - Common queries
   - Feature set

3. **Social Media**
   - Facebook/Instagram: pepstores
   - Common customer questions
   - Promotions and campaigns

4. **Competitor Analysis**
   - Ackermans, Jet, Mr Price
   - Similar retail chatbot features
   - Industry best practices

5. **Customer Service FAQs**
   - Common inquiries
   - Pain points
   - Resolution patterns

### Writing Style Guide:
- **Tone:** Friendly, upbeat, accessible
- **Language:** Simple, clear, conversational
- **Length:** Concise answers (customers are usually on mobile)
- **Structure:** Bullet points, short paragraphs
- **Emphasis:** Value, affordability, accessibility

---

## Success Metrics

**How to Measure Success:**

1. **Response Accuracy**
   - Can correctly answer product questions
   - Provides accurate policy information
   - Correctly triggers handover when needed

2. **User Experience**
   - Chat sessions average 3-5 messages
   - Low abandonment rate
   - Successful handovers for complex queries

3. **Coverage**
   - Knowledge base covers 80%+ of common queries
   - Minimal "I don't know" responses
   - Appropriate use of handover mechanism

4. **Technical Performance**
   - Response time <3 seconds
   - Vector search finds relevant info
   - No crashes or errors

---

## Deployment Strategy

**Testing Phase:**
1. Build knowledge base locally
2. Test with sample customer queries
3. Refine responses and handover triggers
4. Get feedback from PEP employees (if possible)

**Production Deployment:**
1. Deploy to Streamlit Community Cloud
2. Custom domain (optional): pep-assistant.streamlit.app
3. Monitor usage and iterate
4. Collect user feedback

**Future Considerations:**
- Integration with PEP's actual systems (inventory, CRM)
- Embed on pepstores.com website
- Mobile app integration
- WhatsApp bot version

---

## Estimated Timeline

| Week | Tasks | Deliverables |
|------|-------|--------------|
| Week 1 | Research PEP, create 3 knowledge docs | 3 markdown files |
| Week 2 | Complete knowledge base, UI rebrand | 5 docs total, new branding |
| Week 3 | Update code, test locally | Working prototype |
| Week 4 | Refinement, testing, deployment | Live MVP |

**Total:** 4 weeks to functional MVP

---

## Risks & Mitigation

**Risk 1: Limited Public Information**
- **Mitigation:** Use general retail knowledge, make assumptions clear, mark as "Demo/POC"

**Risk 2: No Official PEP Partnership**
- **Mitigation:** Label as "Unofficial proof-of-concept" for portfolio purposes

**Risk 3: Outdated Information**
- **Mitigation:** Add disclaimer: "Product availability and prices may vary"

**Risk 4: Brand Guidelines Violation**
- **Mitigation:** Use generic red/white/black, avoid exact logo reproduction

---

## Next Steps (Immediate Actions)

### Step 1: Create Knowledge Base
```bash
# Create new documents
touch data/documents/pep-products-catalog.md
touch data/documents/pep-services-guide.md
touch data/documents/pep-store-policies.md
touch data/documents/pep-faqs.md
touch data/documents/pep-promotions.md

# Remove old Hollard documents
rm data/documents/hollard-*.md
rm data/documents/life-insurance-basics.md
rm data/documents/claims-process.md
rm data/documents/about-hollard.md
```

### Step 2: Update Branding
- Modify `app.py` color scheme
- Update page title and icon
- Change header text and tagline
- Replace logo reference

### Step 3: Update System Prompt
- Modify `rag_engine.py` prompt
- Change from insurance to retail context
- Update handover triggers

### Step 4: Test Locally
- Run with new knowledge base
- Test various customer queries
- Verify handover mechanism
- Check visual appearance

### Step 5: Deploy
- Push to GitHub
- Deploy to Streamlit Cloud
- Test live version
- Gather feedback

---

## Questions to Answer

1. **Scope:** Full transformation or demo/POC?
2. **Timeline:** Rush (1-2 weeks) or quality (4 weeks)?
3. **Content:** How much product detail? (Basic vs comprehensive)
4. **Features:** Basic chat only, or add store locator/promotions?
5. **Deployment:** Personal portfolio or pitch to PEP?

---

**Status:** Planning complete, ready for implementation  
**Decision Needed:** Approve plan and proceed with Phase 1?
