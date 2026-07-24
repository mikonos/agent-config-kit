---
name: evidence-research-suite-v1
legacy: true
description: "[ARCHIVED v1] 研究者用户研究方法论套件初版（使用期 2025-12-18 至 2026-05-26）。已被 research-research-suite 取代，仅作档案保留。不要按关键词触发本 skill；若必须比对老流水线产出，先 Read 本文件并明确标注「使用 v1 老版」。新工作请使用 research-research-suite。"
---

> **⚠️ ARCHIVED — v1，已退役**
> 本 skill 是 research-research-suite 的初版，于 2026-05-26 被新版取代。完整产出范本见 `00_收件箱_工作区/projects/代号515/01_research/research/research_v4_日历机/`。
> 仅保留作档案，hook/skill-rules.json 路由不再指向本 skill。如需调用方法论流水线，请使用新版 `research-research-suite`。

# User Research Methodology Suite (v1, archived)

> **Core Mission**: Execute a complete 10-tool user research methodology for any product, producing actionable deliverables from user segmentation to innovation concepts.
> **Operating Model**: Progressive 7-phase execution — each phase builds on previous outputs, then a final independent audit checks evidence, coverage, and process completion.
> **Prompt Strategy**: **Expert-first subagent-per-persona execution** (default). Every persona declared in a tool is run by a readonly subagent, but the prompt starts with the expert identity: `You are [Expert Name]...` / `你现在是[专家名]...`. Only after identity is set, tell the LLM which perspective skill or persona shard to use and what to return. The main agent **does not internalize the persona's lexicon** — it receives the subagent's output and assembles. This protects the main agent's context from cross-persona pollution.

> **Subagent mode taxonomy** (governs all tool steps):
> - **Parallel subagents** — multiple personas need to produce *independent* views simultaneously; main agent merges. Use when perspectives would contaminate each other if sequenced.
> - **Isolated subagent (single or sequential)** — persona has a heavy proprietary lexicon; spawn even for a single persona to keep the main agent's context clean. For chains (A → B → C), each step is its own subagent, main agent ferries the artifact between them without absorbing voice.
> - **In-character (main agent switches voice)** — only when the persona is a thin lens with no proprietary lexicon and the tool is short. Allowed for Tool 2 / Tool 5 (and only those).

> **Persona source legend**（与 AI-PM CLAUDE.md §4 Expert Skill Gate 三态规则对齐）:
> - `🟢 Grounded` — prompt starts by making the LLM become the named expert, then activates the `<name>-perspective` skill via the skill registry.
> - `🟡 Simulated` — prompt starts by making the LLM become the named expert with `simulated, no local skill` clearly stated; the LLM then operates from training data + `references/methodology_foundations.md` anchors. Before producing, it must name ≥2 representative works / core concepts for that persona. If it cannot, downgrade to generic methodology with no persona attribution.

> **Original prompt blocks**: The long Role sections and full source prompt blocks are preserved in `references/original_prompt_blocks.md`. When executing one tool or composing a tool-specific subagent prompt, load only that tool's block and use it as the prompt spine after the expert identity line. `SKILL.md` execution rules and Output Discipline remain higher priority.

## Prerequisites

Before activating this skill, gather the following context:

- [ ] **Product definition**: What is the product? What is its core differentiation?
- [ ] **Market context**: Target market, geography, price range, competitive landscape
- [ ] **Existing data** (if any): User reviews, survey data, JTBD analysis, meeting notes, competitive analysis
- [ ] **Target user hypothesis**: Who do you think the primary users are?
- [ ] **Language requirement**: What language should the deliverables/surveys/interviews be in?

## Execution Protocol

### Phase 1: User Identification (Tools 4 → 7 → 2)

Execute in this order. Each tool's output feeds the next.

#### Tool 4: Target User Identification
- **Method**: JTBD-based user segmentation with 4-quadrant framework + Bull's Eye penetration model
- **Personas (parallel subagents)**:
  - A 🟢 primary — Make the LLM become **Bob Moesta** (`bob-moesta-perspective`) in a readonly subagent; narrate Forces of Progress (Push / Pull / Anxiety / Habit) for each candidate group **before** drawing any quadrant; a group earns a cell only if its forces story reads like a transcript.
  - B 🟢 assist — Make the LLM become **Clayton Christensen** (`christensen-perspective`) in a readonly subagent; pressure-test A's segments via non-consumption / over-serving / under-serving lens.
- **Synthesis**: Main agent merges A's segments + B's stress-test into the final 4-quadrant + Bull's Eye; for groups B challenges but A keeps, attach a one-line rationale.
- **Input**: Product definition + existing data + market context
- **Template**: `templates/tool04_target_users.md`
- **Output**: 4-8 user groups with personas, JTBD statements, dual-axis quadrant chart (complexity + motivation), **two prioritization views**: (1) need-match ranking (who needs us most), (2) Bull's Eye penetration map (who to target first → angel/bull's eye/core/strategic/radiation/symbiotic users) with expansion pathway
- **Downstream-signal append (Rule 14)**: at close, append to the Downstream Signal Ledger the channel / acquisition priority per circle and each group's "when they would actually buy" timing — research won't use these, GTM / channel / media-buying will.
- **Tool 4→Tool 7 handoff (must-include · Rule 16)**：Tool 4 收尾给 Tool 7 的交接清单**必须分两类列全**——① 情境群（situational groups，按场景/情境切分的用户群）；② 横切维度（orthogonal dimensions，跨情境群的人群类别，例：DIY 自建派 / 礼物购买者 / 移民家庭 / 特殊家庭结构等——具体清单由本次 Tool 4 主综合方判定，不同产品不一样）。若 Tool 4 输出里出现了横切维度，**交接表必须把它们和情境群并列写明**，不能只传情境群；否则 Tool 7 会漏掉整组横切人群。详见 Rule 16。

#### Tool 7: Functional Needs
- **Method**: JTBD Functional Jobs using "When I... I want... So that..." format + ODI Desired Outcome metrics
- **Persona (isolated subagent, primary)** 🟢 Make the LLM become **Tony Ulwick** (`tony-ulwick-perspective`) in a readonly subagent — Outcome-Driven Innovation; **every** job statement must carry a desired outcome metric (direction + metric + object + contextual clarifier); refuse jobs that read as feature wishes. Subagent returns the functional-jobs table; main agent does **not** absorb ODI lexicon.
- **Persona (isolated subagent, assist)** 🟢 Make the LLM become **Bob Moesta** (`bob-moesta-perspective`) in a readonly subagent — sanity-check each job reflects a real switching event, not a survey-derived wish. Returns kill-list with switching-event evidence.
- **Synthesis**: Main agent merges Ulwick's outcome-metric table + Moesta's kill-list into the P0/P1/P2 matrix without internalizing either lexicon。 收尾时按 D6 在工具产出文档生成一张「承重假设清单」表，每条承重假设挂失效后果与验证交接目标。
- **Input**: Tool 4 user groups + product features
- **Template**: `templates/tool07_functional_needs.md`
- **Output**: 20-30 functional jobs across 6-8 scenarios, with P0/P1/P2 priority matrix。**每条需求三段**：方向（用户从什么处境走向什么处境）+ 抓手（关键一招）+ 边界（别偏成什么）——三段都要有，正向起头；只有「别偏成什么」=半张地图，不算合格条目。
- **Downstream-signal append (Rule 14)**: at close, append to the Downstream Signal Ledger the hire-type tags surfaced via Moesta's switching check — `[Big Hire / 大雇佣]` signals a positive selling point to state loud and proud; `[Anxiety-blocker / 焦虑阻断器]` signals a worry to defuse quietly — the two demand **opposite** marketing treatments. Also append any demo-flow / GTM-channel / trust-architecture cues. **Do not write marketing copy or selling points here** — Tool 7 is the functional layer; for a B2C product 60% of the selling-point material lives in the emotional / social layer (Tool 6) and the soul layer (Tool 1). Selling points are synthesized only at the Phase 3 close — see below.

#### Tool 2: Jenkins Activity Survey (JAS)
- **Method**: Adapted Jenkins Activity Survey across 3 behavioral dimensions
- **Persona mode**: **In-character** (Jenkins is a measurement protocol, not a personality; Kahneman System 1/2 is a universal mental model without proprietary lexicon — main agent applies both directly without subagent isolation).
- **Persona (primary, in-character)**: Jenkins/Zyzanski/Rosenman 量表本人 — no shard; execute per `references/methodology_foundations.md` Tool 2 entry.
- **Persona (assist, in-character)** 🟡 `personas/tool02_kahneman.md` — tag every item as System 1 (gut/emotion-triggered) or System 2 (deliberation) to keep clusters cleanly separable.
- **Input**: Tool 4 user groups + product context
- **Template**: `templates/tool02_jas_survey.md`
- **Output**: 21-question Likert survey (SI/JI/HDC), scoring method, 5 behavioral clusters

---

### Phase 2: Need Excavation (Tools 6 → 9 → 10)

#### Tool 6: Emotional & Social Needs
- **Method**: JTBD Emotional Jobs (feel/avoid feeling) + Social Jobs (appear as/avoid appearing as), each anchored to a trigger moment
- **Personas (isolated subagents, sequential A → B → optional C)**:
  - A 🟢 primary — Make the LLM become **Alan Klement** (`alan-klement-perspective`) in a readonly subagent — for each emotional / social job, **name the trigger moment** the user said "I can no longer live like this" (Big Hire / Little Hire / Fire framing); if no moment, the job is too generic — rewrite it. Returns the emotional-jobs + social-jobs draft with trigger moments.
  - B 🟢 assist — Make the LLM become **Tony Ulwick** (`tony-ulwick-perspective`) in a readonly subagent — takes A's draft as input, attaches a desired-outcome marker to each emotional job so it remains testable (e.g., "minimize the frequency of feeling X in context Y"). Returns annotated job table.
  - C 🟢 context-conditional subagents (activate only when product domain = family / household / care work, e.g., 代号515):
    - Make the LLM become **Eve Rodsky** (`eve-rodsky-perspective`) in a readonly subagent — CPE ownership, invisible labor, mental load.
    - Make the LLM become **Brigid Schulte** (`brigid-schulte-perspective`) in a readonly subagent — time poverty, ideal-worker myth, leisure shame.
    - Make the LLM become **Laura Vanderkam** (`laura-vanderkam-perspective`) in a readonly subagent — time abundance / ringmaster reframe.
- **Synthesis**: Main agent merges A's trigger moments + B's outcome markers into the canonical job table without internalizing either lexicon. For family products, C subagents return cross-cutting framing the main agent weaves into both emotional and social columns (mental load → emotional job; "look like a together-mom" → social job）。 收尾时按 D6 在工具产出文档生成一张「承重假设清单」表，每条承重假设挂失效后果与验证交接目标。
- **反向需求另起结构（Reverse-direction needs branch off）**：Tool 6 区分两类需求——**正向 demand**（用户想要 X，产品越使劲帮、用户越满意）和**反向 / anxiety 类**（用户怕 X，产品越使劲帮、用户可能反而越紧张）。两类**不共用模板**。正向用「方向 + 抓手 + 边界」三段（见 D2 编排维度 + Tool 6 / 7 条目格式）；反向自己一节，每条至少三段：**怕什么**（具体担心）+ **什么会让这个怕更重**（产品 / 营销 / 服务的哪些动作会触发或加剧）+ **怎么化解**（产品 / 营销 / 服务怎么避免触发或主动化解）。判定测试：一条需求如果「使劲优化」会让用户更不安、不是更满意，它属于反向类，必须另起结构。
- **Input**: Tool 4 user groups + Tool 7 functional needs
- **Template**: `templates/tool06_emotional_social.md`
- **Output**: 15+ emotional jobs, 10+ social jobs, ad creative directions。**正向 demand 类每条三段**：方向（用户从什么处境走向什么处境）+ 抓手（关键一招）+ 边界（别偏成什么）。**反向 / anxiety 类每条三段**：怕什么 + 什么会让这个怕更重 + 怎么化解（见上方「反向需求另起结构」）。
- **Downstream-signal append (Rule 14)**: at close, append to the Downstream Signal Ledger the ad-creative directions and the emotional / social hooks that read as positive selling points vs anxiety-blockers. Tool 6's ad-creative output is a **primary input** to the Phase 3 selling-point / positioning synthesis.

#### Tool 9: In-Depth Interview Questions
- **Method**: Multi-school interview design (flow + probe tree + ethnography + switch timeline)
- **Personas (parallel subagents — three interview schools must produce independently to avoid mutual contamination)**:
  - A 🟢 primary — Make the LLM become **Steve Portigal** (`steve-portigal-perspective`) in a readonly subagent: interview flow + **probe tree**; every primary question carries 2-3 anticipated user responses with the follow-up probe for each; a question without its probe tree is a survey, not an interview.
  - B 🟢 assist — Make the LLM become **Elinor Ochs** (`elinor-ochs-celf-perspective`) in a readonly subagent: for any family / household / care context, add language-socialization + participation-framework dimensions (who initiates, who responds, who is silent, who carries the residual).
  - C 🟢 assist — Make the LLM become **Bob Moesta** (`bob-moesta-perspective`) in a readonly subagent: switch interview timeline questions (first thought → first action → decision → consumption → habituation); ensures purchase / abandonment moments get reconstructed, not just preferences.
- **Synthesis**: Main agent receives three independent question banks and weaves: A owns the 60-min skeleton; B's dimensions slot into Tool 9's categories #2 (Contextual), #4 (Historical), #9 (Social); C's timeline slots into #4 (Historical) + #10 (Frequency). Each question flagged with its lead persona.
- **Input**: All Phase 1 outputs + 3 key validation targets
- **Template**: `templates/tool09_interview_questions.md`
- **Output**: 60-100 interview questions across 20 categories, 60-min interview flow, **probe tree attached to each primary question**

#### Tool 10: Quantitative Survey
- **Method**: Structured questionnaire (knowledge/evaluation/behavior/frequency/psychology) + Tailored Design Method
- **Persona (isolated subagent)** 🟡 Make the LLM become **Don Dillman** (simulated; read `personas/tool10_dillman.md` + methodology anchors) in a readonly subagent — Tailored Design Method; **flag single-question fallacy** per item (no item asks two things); enforce order rule (behavior → attitude → demographics last); apply social-desirability defenses (reverse phrasing / third-party phrasing). Returns full questionnaire + per-item audit log; main agent does **not** internalize Tailored Design lexicon (would pollute Tool 1 / 3 / 3b downstream if any post-survey iteration occurs).
- **Pricing method (no persona)**: Van Westendorp PSM is a method, not a persona — main agent applies its four price questions natively, with Dillman's social-desirability phrasing layered (subagent returns the phrasing-overlay alongside main deliverable).
- **Input**: Phase 1 outputs + 2-3 innovation concepts to test
- **Template**: `templates/tool10_survey_design.md`
- **Output**: 40-50 closed-ended questions, 6 modules, analysis framework with key metrics, **per-item single-question-fallacy audit log**

---

### Phase 3: Insight Analysis (Tools 3 → 1)

#### Tool 3: Four-Lens Deep Insight
- **Method**: Four-Lens Framework (Patterns / Contradictions / Feelings / Shortcuts)
- **Personas (parallel subagents, lens-specific — each lens must be analyzed without contamination from neighbors)**:
  - Primary 🟢 Make the LLM become **Teresa Torres** (`teresa-torres-perspective`) in a readonly subagent — owns Lens 1 (Patterns) + cross-lens synthesis insight + design implications: every insight = an assumption that earned its place via cross-source evidence; refuse data-restatement disguised as insight.
  - Lens 2 (Contradictions) 🟢 Make the LLM become **Clayton Christensen** (`christensen-perspective`) in a readonly subagent — non-consumption / over-serving / under-serving as the structural source of contradictions.
  - Lens 3 (Feelings) + Lens 4 (Shortcuts) 🟢 Make the LLM become **Indi Young** (`indi-young-perspective`) in a readonly subagent — apply inner thinking / emotional reactions / guiding-principles slicing (mental model skyline); refuse single-row "behavior only" descriptions; pull problem-space listening framing over solution validation.
- **Synthesis**: Main agent receives four lens artifacts (Primary's Lens 1, Christensen's Lens 2, Indi Young's Lens 3+4), then writes the cross-lens synthesis paragraph. Main agent does **not** internalize any lens persona (especially important since Indi Young's mental-model lexicon would contaminate Tool 3b downstream)。 收尾时按 D6 在工具产出文档生成一张「承重假设清单」表，每条承重假设挂失效后果与验证交接目标。
- **Input**: All existing user data (reviews, interviews, surveys) + competitive analysis
- **Template**: `templates/tool03_four_lens.md`
- **Output**: Cross-validated insights per lens, synthesis insight, design implications

#### Tool 1: Product Soul (Soul of Product)
- **Method**: Ernest Dichter's 4-dimensional brand psychology framework
- **Personas (isolated subagents, sequential — Dichter's motivational-research lexicon must NOT pollute main agent before Tool 3b innovation)**:
  - A 🟢 primary — Make the LLM become **Ernest Dichter** (`dichter-perspective`) in a readonly subagent — motivational research; surface the motivation the user would deny in public but secretly hire the product for; if the soul statement could be read aloud in a boardroom without anyone wincing, it's not deep enough — rewrite. Returns four-dimension analysis + soul statement.
  - B 🟢 assist (cross-cultural) — Make the LLM become **Clotaire Rapaille** (`clotaire-rapaille-perspective`) in a readonly subagent — for the "National Culture" dimension, apply Culture Code + reptilian / limbic / cortex three-brain weighting + on-code/off-code product judgment; required when target market ≠ China. Returns National Culture section.
  - C 🟢 assist (slogan) — Make the LLM become **Steve Jobs** (`jobs-perspective`) in a readonly subagent — for the three emotional-resonance slogans, apply 极简取舍 + 隐喻力测试; kill any slogan that survives only by adding words. Returns three slogans + kill log.
- **Synthesis**: Main agent assembles A's analysis + B's culture section + C's slogans into the final deliverable. Main agent reads none of these SKILL.md files itself。 收尾时按 D6 在工具产出文档生成一张「承重假设清单」表，每条承重假设挂失效后果与验证交接目标。
- **Input**: Four-Lens synthesis insight + emotional needs + market culture
- **Template**: `templates/tool01_product_soul.md`
- **Output**: Core psychology analysis, product soul statement, 3 emotional resonance slogans

#### Phase 3 Close: Selling-Point & Positioning Synthesis（营销卖点/定位综合 — 上市收口环）

This is the **handoff bridge** from research deliverables to launch-executable material. research is a user-**research** suite — its tools end at research insight; the gap between "research output" and "go-to-market executable" is closed by exactly two things: the Downstream Signal Ledger (D5) and this synthesis step.

- **When**: only after Tool 6 (ad-creative directions) **and** Tool 1 (product soul + slogans) are both complete — never earlier. For a B2C product the majority of selling-point material lives in the emotional / social / soul layers; the functional layer (Tool 7) alone cannot carry it.
- **Inputs**: the Downstream Signal Ledger + Tool 6 ad-creative directions + Tool 1 soul statement & slogans.
- **Persona mode**: **In-character** — main agent synthesizes directly (the inputs are already persona-produced; this step assembles, it does not introduce a new proprietary lexicon).
- **Action**: produce a single selling-point / positioning synthesis — separate the **positive selling points to state loud** from the **anxiety-blockers to defuse quietly** (the `[Big Hire]` vs `[Anxiety-blocker]` split from the Ledger), align them to channel / timing signals, and frame the positioning language.
- **Output**: a selling-point & positioning synthesis appended as the closing section of the Downstream Signal Ledger (or its own doc `上市与营销信号台账_{product}.md` final section).
- **Boundary**: this synthesis is the **last station inside research**. Campaign planning, landing-page build, channel execution, and PRD writing are downstream work — research hands off the Ledger + synthesis to them and stops there.

---

### Phase 4: Product Innovation (Tool 3 Round 2)

#### Tool 3b: Four-Lens Innovation Output
- **Method**: Translating insights into tangible innovation concepts
- **Personas (isolated subagents, sequential — three-gate funnel)**:
  - A 🟡 primary — Make the LLM become **Bill Buxton** (simulated; read `personas/tool03b_buxton.md` + methodology anchors) in a readonly subagent — sketch-first design; every new form / feature / ritual must be sketchable in ≤30 seconds; kill anything that needs paragraphs to explain. Returns concept sketches.
  - B 🟢 badass-test gate — Make the LLM become **Kathy Sierra** (`kathy-sierra-perspective`) in a readonly subagent — receives A's sketches; every concept must answer: "what badass thing can the user do or say afterward?" If neither, kill the concept; minimize cognitive leaks. Returns surviving sketches + kill list.
  - C 🟢 hero-concept gate — Make the LLM become **Steve Jobs** (`jobs-perspective`) in a readonly subagent — receives B's survivors; for the single "Hero Concept" deliverable, apply 极简 + 拒绝平庸 + 隐喻力测试. Returns hero concept + slogan-level metaphor.
- **Synthesis**: Main agent assembles A's sketches + B's kills + C's hero into the final innovation deliverable. Failed concepts at any gate go into an "Anti-Portfolio" section with reason。 收尾时按 D6 在工具产出文档生成一张「承重假设清单」表，每条承重假设挂失效后果与验证交接目标。
- **Input**: All Phase 3 outputs + functional/emotional needs
- **Template**: `templates/tool03b_innovation.md`
- **Output**: 2-3 new product forms, 3-4 new features, 3-4 new rituals/scenarios, 1 hero concept, **anti-portfolio of killed concepts**

---

### Phase 5: Ecosystem Design (Tool 8)

#### Tool 8: Product Ecosystem
- **Method**: JTBD Consumption Chain + Platform Strategy (collaborative + co-creation dual ecosystem)
- **Personas (isolated subagents, sequential)**:
  - A 🟡 primary — Make the LLM become **Sangeet Paul Choudary** (simulated; read `personas/tool08_choudary.md` + methodology anchors) in a readonly subagent — **define the single core interaction** (producer / consumer / value unit / filter) before drawing any map; every product / integration must enable or amplify it; chicken-and-egg cold-start pattern must be chosen explicitly. Returns core interaction statement + ecosystem skeleton.
  - B 🟡 assist (service side) — Make the LLM become **Jim Spohrer** (simulated; read `personas/tool08_spohrer.md` + methodology anchors) in a readonly subagent — receives A's skeleton; applies service-dominant logic for the "Service Out" market integrations. Returns annotated service layer.
  - C 🟢 assist (positioning) — Make the LLM become **April Dunford** (`april-dunford-perspective`) in a readonly subagent — positions the ecosystem against the user's real competitive alternatives, not abstract categories. Returns positioning rewrites for the ecosystem narrative.
- **Synthesis**: Main agent assembles A's spine + B's service layer + C's positioning into the ecosystem deliverable, without internalizing platform / service-science / positioning lexicons.
- **Input**: All previous outputs + partnership context + technology stack
- **Template**: `templates/tool08_ecosystem.md`
- **Output**: Collaborative ecosystem map, co-creation platform design, product roadmap, **explicit core-interaction statement**
- **Downstream-signal append (Rule 14)**: at close, append to the Downstream Signal Ledger the partnership / channel cues and Dunford's positioning rewrites — these feed GTM channel choice and the Phase 3 positioning synthesis.

---

### Phase 6: Continuous Learning (Tool 5)

#### Tool 5: Literature Direction
- **Method**: Academic paper reading framework — research direction planning
- **Persona mode**: **In-character** (Stokes Pasteur's Quadrant + Luhmann Anschlussfähigkeit are meta-method lenses without proprietary lexicon — main agent may switch voice directly without subagent isolation).
- **Persona (primary, in-character)** 🟡 `personas/tool05_stokes.md` — Pasteur's Quadrant; **tag each direction Bohr / Pasteur / Edison** and justify why this product needs research from that quadrant, not the cheaper one. Reject directions that can't earn a quadrant.
- **Persona (assist, in-character)** 🟢 use the `luhmann-perspective` skill — apply Anschlussfähigkeit / 稀疏指针 view: which directions create durable Zettelkasten nodes vs one-shot consumption.
- **Synthesis**: Stokes ranks for product-decision urgency; Luhmann ranks for long-term knowledge-network value; main agent presents both rankings side-by-side when they diverge.
- **Input**: Core insights + product differentiation + unresolved questions
- **Template**: `templates/tool05_literature.md`
- **Output**: 4-6 research directions with keywords, recommended journals, expected insights, **per-direction quadrant tag + durability tag**

---

### Phase 7: Independent Quality Audit (Subagent Gate)（and Phase 7.5 Expert Panel Review · v5.10）

After all 11 deliverables are drafted, run the audit personas below as an independent readonly panel. The main agent must not self-certify the research.

**Audit personas (parallel subagents, lean 2-panel)**:
- A 🟢 Make the LLM become **Marty Cagan** (`marty-cagan-perspective`) in a readonly subagent — four big risks (value / usability / feasibility / business viability): does the suite let a PM judge each risk for the product?
- B 🟢 Make the LLM become **Bob Moesta** (`bob-moesta-perspective`) in a readonly subagent — evidence grounding: every insight / persona / job traces to a real switching story, user quote, or marked `[HYPOTHESIS]`.

**Synthesis + checklist + PDSA (main audit agent, no further subagent)**:
1. Merge A's risk findings + B's evidence findings into a single P0/P1/P2 list with `Coverage Matrix` + `Evidence Boundary Notes`.
2. **Gawande checklist completeness** — main agent enforces against the Coverage Matrix directly (no separate checklist subagent; the matrix itself IS the checklist).
3. **Deming PDSA closing section (mandatory)** — main agent writes "what hypothesis about this skill itself was tested this round, what to change in the next." Main agent has the most context across the whole suite, so this stays in-band rather than delegated. Without this section the audit is incomplete.

**Rationale for lean panel**: Cagan covers 80% of product-level failure modes (four risks); Moesta covers the remaining major failure mode (evidence grounding). Gawande/Deming as separate subagents added rigor at high token cost; their function (checklist + PDSA) is structural and can be enforced by main agent. 研究者/Dichter audit dimensions are absorbed into A and B's framings.

**Audit scope**:
- **Evidence grounding**: every insight, persona, need, product-soul claim, innovation concept, and ecosystem recommendation traces back to user quotes, review data, interviews, surveys, or clearly marked `[HYPOTHESIS]`.
- **Coverage**: all 6 phases and all 10 tools are present; expected 11 tool deliverables exist, plus the running Downstream Signal Ledger with its Phase 3 selling-point/positioning synthesis section.
- **Cross-phase integrity**: later outputs explicitly use earlier outputs instead of inventing disconnected conclusions.
- **Research-to-action chain**: insights connect to innovation concepts, ecosystem roadmap, and literature directions without unsupported jumps.

**Subagent output**:
- `VERDICT: PASS / PASS_WITH_FIXES / BLOCKED`
- `问题清单`: P0/P1/P2, with deliverable path/section, evidence gap, and repair action.
- `Coverage Matrix`: Phase/tool × deliverable × status.
- `Evidence Boundary Notes`: claims that must be downgraded to `[HYPOTHESIS]` or backed with additional data.

**Main agent follow-up**:
- P0/P1 must be repaired before the suite is considered complete.
- P2 can be recorded as follow-up.
- Write the audit report as `quality_audit_{product_name}.md` next to the suite outputs, and add a short audit summary to the final handoff.

---

### Phase 7.5: Expert Panel Review（流派合规二审 · v5.10 新增）

Phase 7 是产品级风险与证据接地审查（Cagan 4 风险 + Moesta 切换证据），覆盖产品级失败模式。但**方法论流派内的术语合规**（Dichter 4 维骨架是否齐 / ODI 句法是否被压成人话 / Christensen 三类结构是否落到表 / core interaction 是否逐项回接 / Indi 三层心智是否压缩成情绪标签）只能由**该 tool 的专家本人 panel** 抓出来。

**协议真源**：`references/expert_panel_review.md`（完整 panel 构成、输出格式、合议规则、与 Phase 7 / prd-audit 的接口）。

**触发条件（hard required，不许跳）**：

- 任一 tool 从 `synthesized` 升 `final`，且会被**下游 tool 引用** / 被**营销台账 append** / 被 **Phase 3 close** 综合使用之前
- tool 出现「非共识裁决」（D3 三段裁决）
- tool 涉及术语 cascade（v1.x 锚点替换、戏剧角色改名、文化代码改字、用户群命名改字）

**触发条件（可跳过）**：

- 纯 typo / 格式修复
- 仅追加新内容（无新承重假设、无新非共识裁决、无术语 cascade）

**panel 构成**：该 tool 在 SKILL.md 中声明的所有 persona + 1 个跨流派挑战者；全部走 readonly subagent，不许 in-character。详细组合表见 `references/expert_panel_review.md` § 2。

**合议规则**：

- **primary panelist BLOCKED → 整体 BLOCKED**（Tool 3 Torres 是 primary，她 BLOCKED 决定整体 BLOCKED）
- **任一 panelist BLOCKED + tool 进入跨 tool cascade 角色 → 整体 BLOCKED**
- 整体 BLOCKED：tool YAML status 强制降回 `synthesized`；修复完成前不允许下游使用；修复后必须重跑相关 panelist，不许只 main agent 自评

**与 Phase 7 关系**：两者不替代，互补。dogfood 实证（2026-05-21 research 家庭Agent美国市场）显示 Phase 7 PASS_WITH_FIXES 后 Phase 7.5 仍能判 BLOCKED——Phase 7 抓不到流派合规层。时序：Phase 7 在全 tool synthesized 后跑一次；Phase 7.5 在每个 tool synthesized → final 升档前跑。

**输出归位**：`review{N}_tool{NN}_{tool_name}_expert_panel.md` 顶部段（main agent 合议）+ `_subagent_views/review{N}_tool{NN}_{persona}_view.md`（各 panelist）。

---

## Output Discipline（产出纪律）

> Applies to **every deliverable this skill produces** — each tool's output document and every subagent's raw persona draft. It does **not** apply to this SKILL.md itself (a methodology protocol, not a research deliverable). **D1–D6 below are hard output specs the main agent MUST embed into every tool-execution subagent's prompt from its first instruction** (see the `产出可读性 6 项自检 checklist` at the end of this section).

### D1. Reader-Language Rule（产出语言纪律）

- **All deliverables default to the target reader's native language**. Confirm that language at the **Prerequisites** stage (it is already a Prerequisites checkbox) and propagate it into every subagent prompt.
- **"Plain-language" standard**: methodology descriptions must be rewritten into sentences any target reader understands at a glance. The **subject of every sentence must be a concrete person or thing** (e.g., the mom / the husband / the kid / the AI / the device) — **never** an abstract methodology token (执行者 / 中转者 / 触发瞬间 / 结果指标 and the like) as a sentence subject. A methodology term may be glossed in parentheses on first use only; do not stack jargon in body prose.
- **Keep source-language text only for these 7 categories**: ① product / brand / company names ② person names ③ work titles (add a translation on first use) ④ verbatim user quotes (keep the original + an interpretive translation, as interview / review evidence) ⑤ dataset field names (technical readers must be able to search them) ⑥ industry-standard abbreviations (gloss on first use) ⑦ ID codes, product-category names, file paths. Every ordinary word outside these 7 categories goes into the target reader's language.
- **Front-load it**: every subagent prompt (for any tool) MUST carry this language standard from the first instruction. Do not produce first and translate / simplify later.

### D2. Single-File Tool Deliverable（单文件产出）

Each tool produces **one file**, named `tool{NN}_{tool_name}_{product}.md`. Do not split conclusions and reasoning into separate files.

The single tool document must contain:

- **结论与行动**：这个工具裁决了什么、优先级是什么、下一步该交给谁。
- **读懂结论所必需的 why**：跨镜 / 跨方法调和的核心理由、承重假设的人话失效后果、跨文档引用的「为什么相关」一句话。
- **推断与证据**：深证据、反方完整论证、方法学差异对照、阈值推导、`[HYPOTHESIS]` tags 的完整推断链、未采纳内容透明记录、合成策略推断。
- **反驳条件**：哪些新证据会推翻当前判断。

**6 条落地规则（强制）**：

1. **检验标准**：不熟悉项目的人能不能只读这份工具文档，就看懂这个工具裁决了什么？答否就重写。这条压倒一切其他细则——一切 D2 决策最终回到这句话。
2. **代号纪律**：概念第一次出现时**用人话讲一句**，代号放括号里作 traceability。例：写「E-G3.4『让她的付出被这个家看见』（demand 第一名，机会分 17）」，不是写「E-G3.4 抓手命门」。任何只有内部人看得懂的代号串（P1-P9 / M1-M10 / T1-T12 / HI-1-12 / LB-1-12 等）单独出现 = 违规。
3. **跨文档引用纪律**：引用上游文档时**带「为什么相关」一句话**，不只是路径指针。例：写「Tool 6 §1.1 把 E-G3.4 排第一名（理由：跨多组数据反复出现）」，不是「见 Tool 6 §1.1」。
4. **跨镜 / 跨方法的矛盾调和**：工具文档要保留「两方各说了什么 + 为什么这样裁决」的**核心**。不能只写「采纳了 A」一句话——读者无法独立复核。
5. **承重假设清单**：每条假设的失效后果要写**人话**——「若 X 被推翻 → Y 抓手作废 + Z 营销主语失效」，而不是「Tool 6 §2 G3.10b 修正塌一半」这种内部黑话概括。一条失效后果读者读完应该立刻明白「啊那这件事就不能做了」。
6. **专家术语翻译**：Lens / persona 的方法学词汇（outcome-opportunity-assumption / non-consumption / over-serving / under-serving / thinking-reaction-guiding-principle / mental model skyline / Anschlussfähigkeit 等）可以放在「推断与证据」节；面向决策的结论段必须翻译成产品语言。

**D2 自检 checklist（写完工具文档强制自查 3 件事，缺一项不算交付）**

写完工具产出文档后，每条承重假设、每条跨文档引用、每个隐喻 / 抽象判断写完后，subagent 必须停下来自问：

1. **这条假设要是错了，会让哪条产品决定作废 / 营销改方向 / 排序变动？写清楚了吗？**
   - 反例：「Tool 7 §4c 自动化档位红线整段重写」← 只有内部人看懂
   - 正例：「Tool 7 §4c 自动化档位红线整段重写 → 这意味着档 2（设备替你想好、你同意才执行）这个产品路线失效，要改成档 0（只列选项让你自己挑），G3 妈妈完全用不了」

2. **这条上游引用，读者凭什么知道它和当前结论有关？带「为什么相关」的一句话了吗？**
   - 反例：「见 Tool 6 §1.1」← 只有路径
   - 正例：「Tool 6 §1.1 把 E-G3.4 排第一名（理由：跨多组数据反复出现 + 机会分 17）」

3. **这个隐喻 / 抽象判断后面，有没有至少 1 个具体场景 / 例子 / 数字撑住？**
   - 反例：「产品扮演的是一面如实的镜子」← 镜子怎么照、照成什么样不知道
   - 正例：「产品扮演的是一面如实的镜子——每周给她一份『你这周默默扛了哪些决定 / 信息 / 协调』的清单（比如 27 条决定 / 14 条群消息分拣 / 6 次接送时间协调），把"我这么累"翻译成"我这周扛了 47 件事"」

**通过门槛**：3 件事**全过**才算工具产出文档合格。任意一件不过，补更多附录也救不回——读者需要在同一份文档里看懂这些基本翻译。

**实施时机**：subagent 在 phase 收口前自查；synthesizer agent 在合成工具文档后再过一遍；主 agent（小P）在交付前抽查 3 处。

**D2 编排维度——按用户实际处境编排，不按产品方案编排（强制）**：发现类工具的工具文档（Tool 6 / Tool 7 / Tool 3 / Tool 6 ad-creative）默认按用户处境（她是谁 / 在什么情境里 / 被什么事触发 / 想从哪走向哪）组织，**不**按产品方案（哪个 feature / 哪个抓手 / 哪个交互）组织。常见 drift：subagent 默认会把需求按「产品要建的东西」聚类，看起来整洁，但读者读完不知道用户的处境是什么——产品视图遮蔽了用户视图。**判定测试**：随手挑工具文档里一节，节标题读上去是「用户在某处境里要从 A 走向 B」，还是「产品要做 X 抓手 / X 模块」？是后者就 drift 了，重写。**产品视图不是禁止**——可以作为附录或二级视图存在，但**主结构必须是用户处境**。

**D2 分拣纪律（强制）**：单文件不等于把细节删掉。常见错误：① 高杠杆的「产品该怎么做」被当成「待试设想」丢进附录；② 工具的完整发现清单被压缩掉，只剩高优先级摘要；③ 后来补充 / 修正的条目被留成脚注，没放回主清单。**正确做法**：拿不准也放进工具文档，挂 `[假设]` / `[HYPOTHESIS]` 标签标证据等级即可；深证据、反方论证、推断链可以放在同文件的「推断与证据」节。下面四条规则把分拣做对：

- **D2-1 分拣颗粒度——拆到「清单 vs 估算方法」「结论 vs 推断链」这一层**：当一张表、一节里把「发现」（是什么）和「这个发现怎么来的」（为什么/怎么估出来的）混在一起，**必须先拆开再放进同一个文件**。发现本身（需求名/洞察结论/打法）放在主线，推断链、估分依据、证据来源放在「推断与证据」节。整捆流放=错。
- **D2-2 判定测试——「拿掉它读者还知不知道这个工具得出了什么结论」**：对每一块内容问这句话。读者拿掉它就不知道这个工具结论是什么 → 它属于主线；拿掉后结论仍完整、缺的只是「为什么这么判」 → 它属于同文件的「推断与证据」节。
- **D2-3 分拣键是「对读者是否必要」，证据等级只是标签**：验证状态（已验证 / 假设 / 推断）只给条目挂标签，不决定它是否出现。一条还没验证的「是什么 / 怎么做」，只要它是结论级判断，照样放进工具文档、挂 `[假设]` / `[HYPOTHESIS]` 标签。
- **D2-4 发现类工具的工具文档必须含完整发现清单**：发现类工具（如需求发现 Tool 7、洞察 Tool 3、情感社会需求 Tool 6 这类「产出一份清单」的工具）的工具文档，必须包含**全部条目的完整清单**（每条至少有名字），不能只放高优先级摘要。分层展开——完整清单 + 高优先级条目详解——可以，但完整清单本身要在工具文档露出。

### D3. Traceable, Falsifiable Adjudication（非共识裁决可追溯）

When personas / subagents diverge during Synthesis, the main agent's **every non-consensus adjudication** must be recorded in **three parts** in the tool document's rationale/evidence section:

- **Theory engine** — which school / framework / method this adjudication relies on.
- **Reasoning chain** — 3-5 reproducible lines of reasoning (include historical analogy or data evidence where relevant).
- **What it would take to refute it** — explicitly state the evidence required to overturn this call, so the adjudication is falsifiable rather than dogma.

A one-line "adopted / decided" verdict is not acceptable — it forces downstream readers to trust the main agent with no path to independent review.

> **Terminology-consistency cross-pointer**: when multiple parallel subagents each produce a draft, the same concept will get different translations / terms (parallel subagents are independent by design). Before the final tool document is complete, the main agent MUST run the dedicated terminology-consistency pass — see `Execution Rules` Rule 11.

### D4. Self-Contained Documents（文档自包含）

Each deliverable must be readable **without opening any other document**:

- **Open every deliverable with a `速查` (quick-reference) section** — inline, near the top, a one-pass gloss of every ID system, group / category code, and key abbreviation the document uses (e.g., `I-03 = 第 3 号洞察`, `R-02 = 第 2 号风险`, `BE = Bull's Eye 用户`). When the reader hits a code in the body, the meaning is already on the page.
- **Expand compressed judgments in place**: any sentence that reads correctly only if the reader already memorized an ID or code ("即使知道编号也得脑补才懂") must be rewritten into a self-contained sentence that carries its own meaning.
- Effect: a decision-maker or reviewer can pick up any single deliverable cold and understand it — no cross-document archaeology.

### D5. Downstream Signal Ledger（下游信号台账）

Every tool's output buries a class of signal that **research itself will not use, but the downstream go-to-market / marketing / channel / positioning / PRD stages will need** — e.g., Tool 4 buries channel priority per circle and per-group buy-timing; Tool 7 buries hire-type tags (`[Big Hire]` = a positive selling point to state loud / `[Anxiety-blocker]` = a worry to defuse quietly — opposite marketing treatments), demo flow, GTM-channel and trust-architecture cues. Left scattered across long documents, these signals are lost by the time all 10 tools finish — the downstream owner neither notices nor finds them.

- **One running ledger, accumulated suite-wide**: maintain a single standalone document — suggested name `上市与营销信号台账_{product}.md` — that runs **alongside** the 11 tool deliverables (it is the **12th deliverable**, see Quick Start).
- **Append at every tool's close**: when a tool finishes, beyond its handoff to the next tool, do one extra step — extract from that tool's output every signal that is "useful for downstream launch / marketing / channel / positioning / PRD but not for the research stage" and append it to the ledger. Tools 4 / 6 / 7 / 8 carry an explicit `Downstream-signal append` line in their Execution Protocol step; any other tool that surfaces such a signal appends it too.
- **Typical sections** (reference set — adjust per product): channel & acquisition priority / media-buying timing & marketing triggers / positive selling points / anxiety-blockers (worries to defuse) / demo & landing-page structure / positioning language / trust factors.
- **The ledger is not the selling points themselves**: it is the raw downstream-signal store. Selling points / positioning are produced once at the **Phase 3 Close: Selling-Point & Positioning Synthesis**, using `ledger + Tool 6 ad-creative + Tool 1 soul/slogans`. Do not synthesize selling points at the functional-needs stage (Tool 7).
- **Boundary**: research is a user-**research** suite. It ends at research insight (Tool 8 ecosystem / Tool 5 literature). The ledger plus the Phase 3 selling-point synthesis are research's **only** bridge from research output to launch-executable material; everything past that bridge — campaign planning, landing-page build, channel execution, PRD writing — is downstream work research hands off and does not perform.

### D6. 承重假设的失效后果（Load-Bearing Assumption Failure Map）

当一条 `[假设]` / `[HYPOTHESIS]` 挂在工具产出文档主清单上，**而且下游有产品动作依赖它**（某条抓手 / 某个方向 / 某段定位 / 某条 PRD 条款），它就是一条**承重假设（load-bearing assumption）**。承重假设的标签必须**带一句失效后果**，写明：「若此假设被推翻 → 哪条具体动作 / 抓手 / 方向作废」。例：`[假设·承重] 用户愿意为 X 付溢价 → 若错，整个 premium 定价策略和 Tool 1 soul statement §3 作废`。

**作用**：
- 把假设从免责声明升级成下次验证的具体目标。
- 把承重假设清单直接喂给 Tool 9 / Tool 10 作为验证优先级输入。

**不强制每个 `[假设]` 都做**——只承重的做，普通假设挂普通标签即可。**判定测试**：拿掉这条假设，下游某个具体动作还成不成立？不成立 = 承重。

**落地位置**：每个相关工具（Tool 6 / 7 / 3 / 1 / 3b / 8）的 Synthesis 步骤收尾时，在工具产出文档单列一张「承重假设清单」表，**强制使用 `templates/_d6_load_bearing.md` 标准表头**（v5.10 新增的统一表模板），表头列：`ID | 假设 | 证据等级 | 失效后果（人话）| 建议验证方式（Tool 9/10 交接）`。

**标准表细节**（强制约束）：

- ID 用 `LB-N` 前缀（Load-Bearing），跨 tool 引用加 tool 前缀（如 Tool 6 的 LB-3 在台账写 `T6-LB-3`）
- 证据等级四档：A（一手访谈实证）/ B（二手数据）/ C（方法论推断）/ H（[HYPOTHESIS]）；与 `00_证据可信度台账_{product}.md` 口径一致
- 失效后果**必须写人话三段**：「若 X 被推翻 → Y 抓手作废 + Z 营销/路线图后果」；不许写「Tool X §Y 整段重写」这种内部黑话
- 验证方式**必须可直接喂**给 Tool 9 访谈题 / Tool 10 问卷题 / 工程预研 / 法务 audit（Rule 18 类）；不写「之后验证」「待 Tool 9/10」

完整模板与示例：`templates/_d6_load_bearing.md`。所有 tool 模板的 D6 段必须引用此模板，不重复定义。

---

### 产出可读性 6 项自检 checklist（强制）

These 6 standards are the distilled output spec. **The main agent MUST paste them, verbatim or as a reusable standard block, into the prompt of every tool-execution subagent (primary and assist) — from the subagent's first instruction.** Each subagent self-checks against them before returning its draft; the main agent re-checks them during Synthesis and again before emitting the tool document.

| # | 标准 | 通过判据 | 真源 |
|---|---|---|---|
| 1 | **读者母语** | 工具产出文档 + 每个 subagent 原始视角稿全用目标读者母语；语言已在 Prerequisites 与用户确认（访谈/问卷面向目标市场用户时用当地语言）。 | D1 |
| 2 | **说人话** | 每句主语是具体人物/事物（妈妈/孩子/AI/设备…），不是抽象方法论词（执行者/中转者/触发瞬间/结果指标）；方法论术语首次出现可括号注一次，正文不堆术语。 | D1 |
| 3 | **保留原文仅限 7 类** | 7 类之外的普通词一律用读者母语。7 类 = ① 产品/品牌/公司名 ② 人名 ③ 作品名（首次加译名）④ 用户原话引语（原文 + 意译）⑤ 数据集字段名 ⑥ 业界通用缩写（首次加注）⑦ 编号 / 产品品类名 / 文件路径。 | D1 |
| 4 | **跨文件术语一致** | 综合阶段已跑专门的术语一致性扫描，同一概念译名/术语全套件统一。 | Rule 11 |
| 5 | **文档自包含** | 每份产出文档开头有 `速查` 小节就近释义编号/代号/缩写；正文无「需脑补编号才懂」的压缩判断。 | D4 |
| 6 | **计数对齐** | 文档内每一个「N 条」都能对上对应明细表的实际行数——标题、汇总表、各表头、上下游引用全部和明细表一致；明细表是计数唯一真源。 | Rule 15 |
| 7 | **方法论语法保留**（v5.10 新加）| ODI 句、Job Story 句、Forces of Progress 标签、Big Hire / Little Hire / Fire / [Anxiety-blocker] 标签、Christensen 非消费 / 过度满足 / 供给不足三类结构等专家术语，**在主稿不能被压缩成纯人话**；必须保留原句（或原 schema）再加人话翻译列。例：Tool 7 每条 functional job 必须保留 ODI 原句（`direction + metric + object + context`）+ 人话翻译列；Tool 6 每条 emotional/social job 必须带 trigger moment + outcome marker + Forces of Progress 标签。判定测试：拿掉术语原句，下游验证工具（Tool 9 probe tree / Tool 10 outcome metric）还知不知道怎么设计？不知道 = 违反 checklist 7。| D2 + Rule 17 + Rule 18 |

---

## Execution Rules

1. **Expert-first Subagent-per-Persona (highest precedence)**: For every persona declared in a tool — whether primary or assist, whether parallel or sequential — run a readonly subagent whose first instruction is the expert identity: `You are [Expert Name]...` / `你现在是[专家名]...`. For 🟢 personas, activate the named perspective skill after the identity line. For 🟡 personas, state `simulated, no local skill`, use training data + `references/methodology_foundations.md` anchors, and tag output `Now operating as [Name] (simulated, no local skill) — [one-line stance]`. The main agent ferries artifacts between subagents and assembles, but **does not internalize any persona's lexicon** (exception: in-character mode for Tool 2 / Tool 5). The main agent's `Synthesis` section explains how the artifacts were merged. Two subagent modes (declared per tool): `parallel` (independent views) vs `isolated sequential` (chain A→B→C with main agent as message bus, no voice absorption). 🟡 simulated subagents must self-test ≥2 representative works / core concepts of the persona before producing; if they cannot, they downgrade to generic methodology framing and drop the persona attribution.
2. **Progressive Disclosure**: Execute tools in phase order. Do NOT jump to Phase 3 before completing Phase 1-2.
3. **Evidence Grounding**: Every insight must trace back to real data (user quotes, review data, survey results). Mark assumptions clearly as `[HYPOTHESIS]`.
4. **Cross-Reference**: When executing Tool N, explicitly reference outputs from Tools 1 through N-1.
5. **Language Awareness**: Surveys and interview questions for international markets should be written in the target market's language.
6. **Existing Data Integration**: Always scan the user's knowledge base for existing research (JTBD analyses, meeting notes, market reports) BEFORE generating new outputs.
7. **Output Naming Convention**: Each tool output file is named `tool{NN}_{tool_name}_{product_name}.md`. Evidence, rationale, hypotheses, and adjudication live inside that same file.
8. **Audit Gate**: The suite is not complete until Phase 7 is performed by an independent readonly subagent panel and all P0/P1 findings are handled.
9. **Output-Spec Front-Loading (highest output-discipline precedence)**: The main agent MUST embed the full `产出可读性 6 项自检 checklist` (reader-language / plain-language / 7-category source-text whitelist / cross-file terminology consistency / self-contained documents / count alignment) into **every tool-execution subagent's prompt — primary and assist — from its first instruction**, as a reusable standard block. Confirm deliverable language at Prerequisites. Never produce first and translate / de-jargon / self-contain later. See `Output Discipline` (D1–D6 + checklist).
10. **Single-File Output**: Every tool emits one self-contained tool document with conclusions, rationale, evidence, hypotheses, and refutation criteria — see `Output Discipline` D2.
11. **Terminology-Consistency Pass (Synthesis step) + Cross-tool Cascade SOP（v5.10 扩展）**: 单 tool synthesis 收口时，主综合方 MUST 跑术语一致性扫描——sweep every deliverable so each concept's translation / term is identical suite-wide (parallel subagents inevitably diverge, e.g. 大雇佣 vs Big Hire, DIY 难民 vs DIY 自建派, 主 agent vs 主综合方). This step is mandatory and cannot be skipped. **v5.10 扩展**：当 **Tool 1（灵魂/术语真源）或 Tool 4（用户群定义真源）改版**后，下游 Tool 6/7/8 + 营销台账 + 证据台账 + quality_audit 必须**整套**走 cascade SOP——`references/cascade_sop.md` 定义完整范围（必扫文件列表）、kill log 强制要求、执行顺序、grep + set 双验证、cascade 失败处置。cascade 不彻底 = D5 状态冲突 = blocked 进 Phase 7.5 expert panel review。Cascade 执行责任人是主综合方（小P），不许下放给 subagent；审核责任人是 Phase 7.5 panel，不许由主综合方自审。
12. **Traceable Adjudication**: Every non-consensus Synthesis call is recorded three-part (theory engine / reasoning chain / what would refute it) in the tool document — see `Output Discipline` D3.
13. **Self-Contained Documents**: Every deliverable opens with a `速查` section glossing its ID systems, group / category codes, and key abbreviations; no body sentence relies on the reader having memorized a code — see `Output Discipline` D4.
14. **Downstream Signal Ledger (running deliverable)**: maintain one standalone `上市与营销信号台账_{product}.md` across the whole suite — the 12th deliverable. At every tool's close, append the signals that are useful for downstream launch / marketing / channel / positioning / PRD but not for research. research is a user-research suite and stops at research insight; the ledger + the `Phase 3 Close: Selling-Point & Positioning Synthesis` (ledger + Tool 6 + Tool 1) are the only bridge from research output to launch-executable material. Never synthesize selling points at Tool 7 — see `Output Discipline` D5.
15. **Count Drift Guard（计数漂移防呆）**：**明细条目表是计数的唯一真源**。任何往明细表增删条目的动作，必须**同步当场**更新所有引用该计数的地方——本节表头、汇总表/总表、章节标题、文档内其它提及条数的句子、以及上下游文档里引用这个条数的地方。补完条目不算完成，所有计数对齐了才算完成。**同一原则纵向延伸**：光对得上总数不够，要对清单本身——上一步判过的条目，在下一步对应表里必须能找到，或当场写明为什么被丢。只看 count 看不出来掉的条目，要看 set。哪些步骤值得做 set check，由使用者按风险判断，不规定必查。
16. **Tool 4→Tool 7 Handoff SOP（横切维度必须交接）**：Tool 4 输出经常同时含两类人群划分——**情境群**（situational groups，按场景/情境切分）和**横切维度**（orthogonal dimensions，跨情境群的人群类别，例：DIY 自建派 / 礼物购买者 / 移民家庭 / 特殊家庭结构等）。Tool 4 收尾给 Tool 7 的交接清单**必须把这两类并列列全**，不能只传情境群。否则 Tool 7 在做需求展开时会漏掉整组横切人群。**判定责任**：本次 Tool 4 是否产生了横切维度、产生了哪些，由 Tool 4 主综合方判定——不同产品的横切维度不一样，本规则不规定具体清单。**接收方义务**：Tool 7 拿到交接清单时若发现只有情境群、没有横切维度声明，应回查 Tool 4 输出确认是「确实没有」还是「漏传了」。
17. **度量设计不进需求稿（Measurement Stays Out of Demand Docs）**：需求 / 痛点 / 洞察 / 情感工作类工具（Tool 6 / Tool 7 / Tool 3）的工具文档**禁止**包含「衡量 / 指标 / KPI / 测量方法 / 验证落点」这类列。这类列一旦存在，主综合方和 subagent 会被拖去给每条需求设计度量，把「这条需求该怎么帮到用户」的判断挤掉。**度量设计属于验证工具的活**——量化测量去 Tool 10（问卷），行为观测去 Tool 9（访谈），承重假设的失效条件去 D6。**例外**：Tool 7 的 ODI outcome metric 是 outcome 表达的一部分（例如「最小化在情境 X 下感受到 Y 的频率」），不是独立 KPI 列，照常保留。**判定测试**：一列里如果大半条目读上去像「装个传感器测它」「定个数字目标」，这列就该删，搬去验证工具。
18. **承重技术能力独立体检（Load-Bearing Capability Gate）**：当某条需求 / 抓手 / 方向**依赖一项尚未充分验证的技术能力**（AI 模型在特定任务上的准确率、设备传感器精度、第三方 API 的 SLA、外部数据源的可用性等），不能把这种依赖埋在需求条目里假装能用——必须在工具文档单立一节「承重能力体检」，每项列出：(a) **理论上能做什么**（in principle）——该能力理论上限是什么；(b) **眼下实际到哪一格**（in practice）——已知的最新基准 / 已知失败案例 / 距离可用还差什么。**触发条件**：只有当某条抓手依赖这项能力、且这项能力当下水平直接影响该抓手能否成立时才触发——不是每个工具都做、不是每条需求都做。**作用**：避免把「等模型变强就能做」这类假设藏在结论里；把它显化成下次验证的具体技术目标，喂给 Tool 9 / Tool 10 或工程预研。**判定测试**：删掉这条能力假设，对应的抓手还成不成立？不成立 = 这项能力是承重的，必须体检。**适用产品类型**：AI Agent 类 / 传感器 / IoT 类 / 机器人类 / 需要外部数据或 API 的产品；纯 UI / 服务 / 内容类产品通常不触发。**与 D6 的关系**：D6 管承重「需求 / 行为 / 心理假设」的失效后果；Rule 18 管承重「技术能力」的当下成熟度——两者互补，不重复。
19. **Original Prompt Block Loading（原始长提示词按需加载）**：执行某个工具、写该工具 subagent prompt、或发现输出开始变薄时，必须读取 `references/original_prompt_blocks.md` 中对应工具的完整提示词块。使用顺序是：① 先写专家身份第一句（Rule 1）；② 放入对应原始提示词块作为方法骨架；③ 加入本次产品 / 用户 / 数据上下文；④ 放入「产出可读性 6 项自检 checklist」；⑤ 要求单文件产出并内嵌「推断与证据」。不要把全部 10 个长块一次性塞进所有 subagent；只加载当前工具需要的块。若原始块与本文件规则冲突，以本 `SKILL.md` 为准。

## Quick Start

To execute the full suite:

```
1. Gather prerequisites (product def, market context, existing data, **deliverable language**)
2. Execute Phase 1 → Phase 2 → Phase 3 (incl. selling-point/positioning synthesis at close) → Phase 4 → Phase 5 → Phase 6 → Phase 7 audit
3. Each tool produces one self-contained tool document (Output Discipline D2); at every tool's close, append downstream signals to the running Signal Ledger (Output Discipline D5 / Rule 14)
4. Total output: 11 tool documents + 1 Downstream Signal Ledger + 1 independent audit report
5. Estimated execution: can be done in a single autonomous session
```

## Reference Materials

- `references/methodology_foundations.md` — Theoretical foundations for each tool (used as fallback when a `🟡 pending` persona shard is missing)
- `references/original_prompt_blocks.md` — Original long Role sections and full prompt spines; load only the active tool section when composing tool / subagent prompts
- `references/execution_tips.md` — Lessons learned from real executions
- `examples/product_execution/` — Complete example execution for an AI-native family calendar machine
- `personas/` — Per-tool persona shards (🟡 markers in this SKILL.md indicate files pending distillation). See `personas/README.md` (if present) for distillation status.

## Persona Roster (quick map)

| Tool | Subagent mode | Persona(s) | Status |
|---|---|---|---|
| 4 Target Users | **Parallel subagents** | Bob Moesta + Christensen | 🟢🟢 |
| 7 Functional Needs | **Isolated subagents (seq)** | Tony Ulwick + Bob Moesta | 🟢🟢 |
| 2 JAS | **In-character** (thin lens, no proprietary lexicon) | Jenkins protocol + Kahneman split | —🟡 |
| 6 Emotional & Social | **Isolated subagents (seq A→B, +conditional C)** | Klement + Ulwick + (Rodsky/Schulte/Vanderkam for family ctx) | 🟢🟢🟢 |
| 9 Interview | **Parallel subagents** | Portigal + Ochs + Moesta | 🟢🟢🟢 |
| 10 Survey | **Isolated subagent** | Don Dillman | 🟡 |
| 3 Four-Lens Insight | **Parallel subagents (lens-specific)** | Teresa Torres + Christensen + Indi Young | 🟢🟢🟢 |
| 1 Product Soul | **Isolated subagents (seq)** | Dichter + Rapaille + Jobs | 🟢🟢🟢 |
| 3b Innovation | **Isolated subagents (seq)** | Buxton + Kathy Sierra + Jobs | 🟡🟢🟢 |
| 8 Ecosystem | **Isolated subagents (seq)** | Choudary + Spohrer + Dunford | 🟡🟡🟢 |
| 5 Literature | **In-character** (meta-method, no lexicon pollution) | Stokes + Luhmann | 🟡🟢 |
| 7 Audit | **Parallel subagents (lean 2)** | Cagan + Moesta（checklist + PDSA 主 agent 自做） | 🟢🟢 |

**Reading guide**:
- **Parallel subagents** = perspectives must produce independent views simultaneously (mutual contamination harms quality)
- **Isolated subagents (sequential)** = personas have heavy proprietary lexicons; main agent ferries artifacts between subagents without absorbing voices
- **In-character** = persona is a thin lens; main agent may switch voice directly (only Tool 2 / Tool 5)
