# Meeting Notes - August 18, 2025

## Bridge Vesting Scheme Discussion

### Date: 2025-08-18

### Attendees: Fam, Huck, Ziggy, Bako

### Meeting Type: Tokenomics & Architecture Planning

---

## 🏗️ Vesting Mechanics Discussion

* **Linear Vesting Concern**

  * Huck raised the issue that if both 1-year and 2-year vestors have the same number of tokens available at the 1-year mark, there is no rational reason to choose 1 year.
  * Point: Without differentiation, everyone will choose the maximum duration, which makes shorter options redundant.

* **Reward Distribution Clarification**

  * Fam clarified that rewards are not technically equal. They are divided by staketime, so a 2-year lock earns proportionally more than a 1-year lock.
  * Example: if Alice vests for 1 year and Bob vests for 2 years, Bob receives 2x Alice’s share of the distribution.

* **Curve Requirement**

  * Fam suggested using a curve with a positive second derivative (quadratic or higher) so longer commitments gain disproportionately higher rewards.
  * This avoids the situation where shorter vesting periods appear equally rational.

* **Liquidity Lock-in Perspective**

  * Bako argued that whether participants are motivated by loyalty or greed is irrelevant; the system benefits from tokens being locked into the economy either way.
  * Example given: similar to miners staking more to compete for block production, self-interest can still produce systemic strength.

* **Exit Optionality**

  * The advantage of shorter vesting is the ability to exit the economy earlier.
  * This filters out participants who want to leave quickly and rewards those who commit to staying.

---

## 📊 Broader Tokenomics Considerations

* **Inflation and Supply Concerns**

  * Ziggy emphasized that inflation should be minimal and tied to utility/usage, not arbitrary emissions.
  * If everyone locks for 2 years, emissions become predictable, but if not, initial liquidity can be unpredictable.

* **Control of Liquidity**

  * Fam pointed out that if some holders vest short, they initially control more liquidity.
  * However, with a quadratic or higher curve, shorter vestors are further diluted relative to long-term participants.

* **Treasury Backstop (conceptual)**

  * Discussion touched on the idea that if few people vest, the treasury would hold the unvested tokens by default.
  * This ensures the treasury controls liquidity unless users actively vest.

* **Market Dynamics**

  * Bako noted that valuation is constrained by existing Commune value plus any external investment.
  * Vesting decisions affect the maximum initial supply, which is hard to predict. Therefore, incentives should strongly lean toward vesting to make projections manageable.

---

## 🏗️ Bridging

* **Agreed upon method of bridging**:
  * Ultimately the group agreed upon bridging to Base EVM chain in order to allow existing COM token holder to exit the economy if they so choose and providing a smart contract to allow holders of COM to bridge at the vesting schedule they choose.
  * Technical details were briefly discussed before Bako said he will document the requirements and objectives for implementation.

## 🔑 Strategic Objectives (Consensus)

Bako summarized the group’s goals for the bridge and vesting scheme:

1. **Filter out short-term participants** who want to exit quickly.
2. **Reward conviction-based holders** who believe in the project’s long-term success.
3. **Lock funds into the economy** to provide stability and initial liquidity.
4. **Avoid excessive inflation** or mechanisms that destabilize price at launch.

Fam and others agreed this is best addressed by the current vesting model with a superlinear curve.

## 🧩 Product & Module System

* V1 goal: enable running modules/servers on remote machines.
* Rapid iteration: add a new module/tool daily; aim for MCP compatibility for broad integration.
* Security model: containerized execution with bind-mounted module files to constrain write scope.

## 🛠️ Infrastructure & Compute Notes

* Actively evaluate cheapest Docker-capable compute APIs.
* Current stance: Database Mart is workable; Akash and Polaris considered non-viable for our needs.

## ⏱️ Bridge Timeline

* Target: bridge running on testnet this week.
* Goal: enable bridging in the first week of September, pending testnet results.

## 📝 Action Items

* **Ziggy**: Work on the SDK side of the bridge (aim for testnet readiness this week).
* **Bako**: Document bridge requirements and objectives for implementation (ASAP to support testnet this week).
* **Huck**: Continue development on the front end (support bridge UI/flows as needed).
* **Fam**: Continue development of the module system (V1 enabling remote server execution).
