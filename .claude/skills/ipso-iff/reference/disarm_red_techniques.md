# DISARM Red Technique Reference (curated)

Curated subset of the DISARM Red Framework (source:
https://github.com/DISARMFoundation/DISARMframeworks,
`generated_pages/techniques_index.md`). IDs are stable DISARM identifiers — never use an ID
that is not listed in this file. If nothing here fits a finding, tag it `none`.

## Reader Techniques

Text/rhetoric techniques detectable from wording and structure alone.

| ID | Name | Summary |
|----|------|---------|
| T0016 | Create Clickbait | Create attention-grabbing headlines (outrage, doubt, humour) required to drive traffic and engagement. |
| T0022 | Leverage Conspiracy Theory Narratives | Use or build on existing conspiracy theory narratives to frame the message. |
| T0023 | Distort Facts | Twist or exaggerate real facts to support a misleading conclusion. |
| T0023.001 | Reframe Context | Present real content in a false or misleading context. |
| T0040 | Demand Insurmountable Proof | Demand a standard of proof for an opposing claim that can never realistically be met. |
| T0042 | Seed Kernel of Truth | Build a false narrative around a small grain of verifiable truth to make it more credible. |
| T0048 | Harass | Direct hostile, repeated messaging at a target person or group. |
| T0076 | Distort | Skew presentation of information to mislead about its meaning or significance. |
| T0077 | Distract | Draw attention away from an inconvenient topic toward an unrelated one. |
| T0082 | Develop New Narratives | Create an original narrative to advance an operation's goals. |
| T0083 | Integrate Target Audience Vulnerabilities into Narrative | Shape a narrative around a target audience's known fears, grievances, or biases. |
| T0129.006 | Deny Involvement | Explicitly deny responsibility or involvement in an event despite evidence. |
| T0135.004 | Polarise | Push a topic toward two opposed extremes to deepen division. |
| T0138.002 | Provoke | Deliberately trigger an emotional or hostile reaction in the audience. |
| T0140.003 | Spread Hate | Promote hateful content targeting a person or group. |
| T0004 | Develop Competing Narratives | Advance a narrative that contradicts or competes with another to sow confusion. |
| T0136.002 | Justify Action | Provide a rationalizing justification for an otherwise indefensible action. |

## Source Techniques

Distribution, amplification, and coordination techniques detectable through outlet/channel
lookups.

| ID | Name | Summary |
|----|------|---------|
| T0049.007 | Inauthentic Sites Amplify News and Narratives | Use non-genuine websites to republish and amplify narratives. |
| T0084.002 | Plagiarise Content | Republish someone else's content as if it were original. |
| T0084.004 | Appropriate Content | Take existing content and repurpose it for a different narrative. |
| T0096 | Leverage Content Farms | Use existing content-farm infrastructure to produce or spread content. |
| T0098 | Establish Inauthentic News Sites | Set up outlets designed to look like genuine news sources. |
| T0098.001 | Create Inauthentic News Sites | Build a new fake news outlet from scratch. |
| T0098.002 | Leverage Existing Inauthentic News Sites | Reuse an already-established fake outlet. |

## Analyst Techniques

Fabrication, synthetic/manipulated media, and persona/fact-distortion techniques
detectable through corroboration lookups.

| ID | Name | Summary |
|----|------|---------|
| T0023 | Distort Facts | Twist or exaggerate real facts to support a misleading conclusion. |
| T0023.001 | Reframe Context | Present real content in a false or misleading context. |
| T0129.006 | Deny Involvement | Explicitly deny responsibility or involvement in an event despite evidence. |
| T0143.002 | Fabricated Persona | Invent a person or organization that does not exist. |
| T0143.003 | Impersonated Persona | Pose as a real, specific person or organization without authorization. |
| T0143.004 | Parody Persona | Use an exaggerated or satirical persona that can be mistaken for genuine. |
| T0144 | Persona Legitimacy Evidence | Fabricate supporting evidence (bios, photos, history) to make a persona appear real. |
| T0140.001 | Defame | Make false statements damaging to a person's or organization's reputation. |
