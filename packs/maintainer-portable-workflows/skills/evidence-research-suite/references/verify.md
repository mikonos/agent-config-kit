---
name: research-verify
type: reference
status: hard-rules
applies_to: evidence-research-suite v3
---

# 自检 + Triple + 机械 Verify 协议

> 本文件是 evidence-research-suite v3 的自检规则真源。**所有产出层引用 / 跨工具 trace / 用户原话 cite 必须以 triple 形式输出，主上下文用机械 grep 验证**。**Non-verifiable claim = 删除**。
>
> 设计原则（k 神 review）：**「hopeful prompt」（"agent 应该读全文"）治标；「verifiable + leash」（输出 triple + 机械验证）才能 catch fabrication**。Subagent 凭印象编造内容时，triple 验证会暴露。

## 一、Triple 格式（v3 核心硬约束 · k 神 P0）

所有 claim（v4/v5 对比、用户原话引用、跨工具 trace、上游 finding 引用、cited literature）必须以下列 triple 输出：

```
(claim, source_file, line_range)
```

**示例**（合规）：
```markdown
- claim: "v5 灵魂段六字'被需要,允许下线'"
  source_file: "research_v5_productFamilyAI/tool01_product_soul_productFamilyAI.md"
  line_range: "L136-142"

- claim: "用户原话: 'I'm the only one who remembers everything'"
  source_file: "amz reviews skylight 15/10_results/voc_单点承压家庭调度员_原始评论集.md"
  review_id: "skylight15-0001"
  helpful: 132
```

**禁止**（违反 = fabrication 标记）：
- "见全文" / "随处可见" / "评论里到处都是" 类模糊指向
- 无 source_file 的 quote
- 推测的 line_range（"应该在第 X 行"）
- 跨文件归并引用（"Tool 3 + Tool 6 + Tool 4"——必须各自一条 triple）

## 二、Mechanical Verify 协议（主上下文必做）

Subagent 产出收回后，主上下文按下列步骤机械验证：

### 步骤 1：Triple 提取

从 subagent 报告 grep 所有 triple block：

```bash
grep -E "source_file:|line_range:|review_id:" <subagent_report.md>
```

### 步骤 2：Source file 存在性 verify

```bash
for f in $(grep "source_file:" report.md | cut -d: -f2); do
  [ -f "$f" ] && echo "OK $f" || echo "FAIL $f NOT FOUND"
done
```

### 步骤 3：Line range 内容 verify

随机抽 3-5 条 triple，机械 verify 对应 line 真有 claim 内容：

```bash
# 例：verify line 136-142 真含 "被需要"
sed -n '136,142p' tool01_product_soul_productFamilyAI.md | grep -q "被需要" && echo "OK" || echo "FAIL fabricated"
```

### 步骤 4：Quote 在 review_id verify

用户原话 quote 必须能在 source review 集 grep 到：

```bash
grep -F "I'm the only one who remembers everything" "voc_单点承压家庭调度员_原始评论集.md" || echo "FAIL quote not in source"
```

### 步骤 5：Fabrication 判定

- Source file 不存在 → claim 删除
- Line range 内容不匹配 → claim 删除 + 标 [⚠️ TRACE FABRICATED]
- Quote 不在 review → claim 删除 + 标 [⚠️ QUOTE FABRICATED]
- triple 缺三要素 → claim 不合规，要求 subagent 补全或删除

## 三、自检 block 模板（每个 tool 产出末尾必填）

```markdown
## 自检（agent 必填，每条带 triple 证据）

- [ ] **命名归位**：文件名 `toolXX_<name>_<product>.md`
  - triple: (filename, this_file, L1)

- [ ] **YAML 完整**：date / type / tool / product / language / status / version / inputs 必填字段齐全
  - triple: (yaml_complete, this_file, L1-LN)

- [ ] **跨工具引用锁日期格式**：所有 `[[..._YYYYMMDD]]` 含日期
  - triple per upstream: ([[upstream_ref]], inputs_field, L_X)

- [ ] **格式硬约定**：本工具 1218 原稿硬格式（Likert / 第一人称 / feel-avoid / When-I-hope-so-that 等）
  - triple sample 1: (claim_about_format, this_file, L_X)
  - triple sample 2: (claim_about_format, this_file, L_Y)

- [ ] **语言符合约定**：默认 zh-CN（部分 tool 例外见 templates）
  - triple: (language, this_file, L_global)

- [ ] **不越边界**：本产出仅为 <tool 范围>，没把 <相邻 tool 范围> 当本工具产出
  - triple: (statement_in_text, this_file, L_X)

- [ ] **v1 深化声明**：（v2.1+ 推荐默认开启）启用了哪些 v1 深化项 / 未启用必须解释 why not
  - triple per extension: (extension_name, this_file_section, L_X)

- [ ] **Job Statement 证据层**：（Tool 3 / Tool 6 / Tool 7 且输入含访谈/评论/反馈时必填）需求或洞察是否回指 Job Statement id；缺字段是否降级为 `待追问`
  - triple sample: (job_statement_id_or_missing_evidence, this_file, L_X)

- [ ] **机械 verify pass**：主上下文已用 grep 验证本产出的 triple 至少 5 条，全部 pass（无 source file 缺失 / 无 line range 不匹配 / 无 quote fabrication）
  - triple: (verify_log_path, parent_log, L_X)
```

## 四、Triple 验证脚本示例（主上下文可直接用）

下面是一个 retroactive verify 脚本，主上下文跑这个验证 subagent 报告的 fabrication 率：

```bash
#!/bin/bash
# verify_triples.sh — 机械验证 subagent 报告里的 triple
# 用法: ./verify_triples.sh <subagent_report.md>
# 期望 triple 格式: claim: <text> | source_file: <path> | line_range: <start>-<end> | keyword: <required_token>
# v3.1（2026-05-27 dogfood verified）：必须实现 Step 1/2/3 三步，缺一步 catch rate 跌到 25%

REPORT=$1
PASS=0
FAIL=0
FABRICATED_CLAIMS=()

# 提取所有 triple
while IFS= read -r line; do
  source=$(echo "$line" | grep -oP 'source_file:\s*\K[^\s|]+')
  range=$(echo "$line" | grep -oP 'line_range:\s*\K[^\s|]+')
  keyword=$(echo "$line" | grep -oP 'keyword:\s*\K[^|]+' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

  # STEP1_FILE: 文件存在性
  if [ ! -f "$source" ]; then
    FAIL=$((FAIL+1))
    FABRICATED_CLAIMS+=("STEP1_FILE_NOT_FOUND: $source")
    continue
  fi

  # STEP2_LINE: 行号范围合法性（end_line ≤ total_lines）
  total_lines=$(wc -l < "$source")
  start_line=$(echo "$range" | grep -oP '^\d+')
  end_line=$(echo "$range" | grep -oP '\d+$')
  if [ "$end_line" -gt "$total_lines" ]; then
    FAIL=$((FAIL+1))
    FABRICATED_CLAIMS+=("STEP2_LINE_OUT_OF_RANGE: $source L$range (file has $total_lines lines)")
    continue
  fi

  # STEP3_KEYWORD（v3.1 必做 · 关 25% catch rate）: keyword 真在 line range 内出现
  if [ -n "$keyword" ]; then
    if ! sed -n "${start_line},${end_line}p" "$source" | grep -qF "$keyword"; then
      FAIL=$((FAIL+1))
      FABRICATED_CLAIMS+=("STEP3_KEYWORD_NOT_IN_RANGE: '$keyword' missing in $source L$range")
      continue
    fi
  fi

  PASS=$((PASS+1))
done < <(grep -E "source_file:.*line_range:" "$REPORT")

echo "=== Verify Result ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"
echo "Fabrication catch rate: $(echo "scale=2; $FAIL / ($PASS + $FAIL) * 100" | bc)%"
echo
echo "=== Fabricated claims ==="
printf '%s\n' "${FABRICATED_CLAIMS[@]}"
```

**v3.1 dogfood 数据**（retroactive verify D5 8 条 fabrication）：
- 只跑 Step 1+2：catch rate **25%**（6 条 FABRICATED_PASS 漏检）
- Step 1+2+3 全跑：catch rate **88-100%**（k 神 60% 阈值通过）
- **Step 3 keyword grep 是 catch 率从 25% 到 100% 的关键，缺一不可**

## 五、Subagent Spawn 时的 Triple 协议要求

主上下文 spawn 任何对比类 / 引用类 / 综合类 subagent 时，prompt 必须含下列段：

```
## 严格 Triple 协议（必守，违反 = fabrication 判定）

1. 所有 claim 必须以 (claim, source_file, line_range) triple 输出
2. 不允许 "见全文" / "随处可见" 模糊指向
3. 不允许推测的 line_range（必须是真 Read 后引的具体行号）
4. 不存在的文件必须明示 "file_not_found: <path>"，不允许编造内容
5. 截断的 ls / output 必须 explicit 标 truncated，不允许凭剩余推断
6. 报告末尾必须列 triple verify 自评：(total_claims, fabrication_risk_per_claim)

主上下文收回报告后会跑 verify_triples.sh 机械验证。fabrication > 20% = 报告打回重做。
```

## 六、为什么 Triple + 机械 verify > Hopeful prompt（k 神 framing）

**对比 v2.1「严格 Read 协议」hopeful prompt**：
- 旧：subagent prompt 写「必须 Read 全文不许 head/grep」→ subagent **echo** 协议但继续 fabricate（D5 案例）
- 新（v3）：subagent prompt 要求输出 triple → 主上下文机械 verify → 不能 verify 的 claim 删除

**为什么有效**：subagent 凭印象编造内容时不能产生真实的 (source_file, line_range)——它会写不存在的文件或超出文件范围的行号，机械 grep 立刻暴露。这是 verifiable + leash 在 prompt 层的最小实现，**不再依赖 subagent 的"自律"**。

## 七、Triple 协议覆盖范围

**必须 triple**：
- v4 / v5 / 历史目录文件对比类 claim
- 用户原话 quote
- 跨工具 trace（"Tool 1 灵魂段引 Tool 3 综合洞察 N"）
- 学术引用 / 数据 / 统计
- 上游产物 cite

**可以不 triple**（信息密度太低反而累赘）：
- 一般方法论叙述（"Dichter 四维框架包含..."）
- 自定义 framing / 推论标记为 inference 的段落
- 与 SKILL.md / templates 完全一致的引用规则

## 八、Known Limitations

- **中文 keyword 启发式**：Step 3 keyword grep 对中文 claim 的 keyword 自动提取（非显式 `keyword:` 字段时）可能不准。中文文件可能用别的表述（如「证据台账」vs `evidence_map`），导致 false alarm 反方向（true claim 被误判 FAIL）。**当前不修**——这是 false alarm 反方向（不漏 fabrication），不属 catch fabrication 主目标。subagent 报告 triple 时**优先用显式 `keyword:` 字段**避免启发式漏。

## 九、Verify-the-Verifier Mechanical Check（v3.1 新增 · k 神 verdict）

**问题暴露**（dogfood 2026-05-27 retroactive verify）：v3 split 时 verify.md 的 §二写了 Step 1+2+3 三步协议，但 §四 bash 脚本示例**只实现了 Step 1+2 跳过 Step 3**——结果 retroactive verify D5 fabrication catch rate 仅 25%。补 Step 3 后 catch rate 提到 88-100%。

**深层 framing**（k 神）：「**任何自我声明的 verifier 默认不可信**」。verify.md 是 LLM 自己 split 出来的——它默认偷懒到刚好能编译过，不到刚好能 verify 过。Spec 写了 Step 3 不等于实现了 Step 3。leash 套在 agent 上，但 leash 是 agent 自己编的，没人 check leash 是不是断的。

**Mechanical self-check 协议**：任何 verify.md 修订 / split / 重构后必须跑下面 grep 自检，确认 bash 脚本含 Step 1/2/3 三步实现：

```bash
#!/bin/bash
# verify_the_verifier.sh — 检 verify.md bash 块是否完整实现 Step 1/2/3
# 用法: ./verify_the_verifier.sh references/verify.md
VERIFY_MD="$1"
MISSING=()
for step in "STEP1_FILE" "STEP2_LINE" "STEP3_KEYWORD"; do
  if ! grep -q "$step" "$VERIFY_MD"; then
    MISSING+=("$step")
  fi
done
if [ ${#MISSING[@]} -gt 0 ]; then
  echo "FAIL: verify.md missing implementations:"
  printf '  - %s\n' "${MISSING[@]}"
  exit 1
fi
echo "PASS: verify.md implements all 3 verify steps"
exit 0
```

**适用场景**：每次 verify.md edit / split / 重构 / refactor 后必跑。CI 友好（exit code 1 = verify-the-verifier failed）。

**为什么这个 check 必须**：spec-implementation gap 是 LLM 偷懒型 silent failure，单靠 prompt 约束防不住，必须 mechanical check。这是 dogfood 暴露的新一类 silent failure：**不是 PRD fabrication，是 verifier 自己漏 step**。verify 自己的 verifier 需要单独被 verify。
