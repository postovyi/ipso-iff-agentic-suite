# Shared Conventions for ipso-iff Detective Specialists

Read by `ipso-reader`, `ipso-analyst`, and `ipso-source` before they start work. Defines the
DISARM technique tables each role tags against, the session-folder report convention, and
the tool-usage rules shared by the two tool-backed specialists.

## DISARM Reference (curated)

Curated subset of the DISARM Red Framework (source:
https://github.com/DISARMFoundation/DISARMframeworks,
`generated_pages/techniques_index.md`). IDs are stable DISARM identifiers — never use an ID
that is not listed in the table for your role. If nothing there genuinely fits a finding,
omit the finding — never invent an ID, never force a fit, and never tag `none`.

### Reader Techniques

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

### Source Techniques

Distribution, amplification, and coordination techniques detectable through outlet/channel
lookups.

| ID | Name | Summary |
|----|------|---------|
| T0049 | Flood Information Space | Overwhelm the information space with high-volume content to drown out other voices. |
| T0049.002 | Flood Existing Hashtag | Push high volumes of content into an existing hashtag to hijack or dilute it. |
| T0049.003 | Bots Amplify via Automated Forwarding and Reposting | Use automated accounts to mechanically reshare content at scale. |
| T0049.005 | Conduct Swarming | Coordinate a burst of accounts to act on the same target simultaneously. |
| T0049.007 | Inauthentic Sites Amplify News and Narratives | Use non-genuine websites to republish and amplify narratives. |
| T0060 | Continue to Amplify | Sustain repeated amplification of content already in circulation. |
| T0084.002 | Plagiarise Content | Republish someone else's content as if it were original. |
| T0084.004 | Appropriate Content | Take existing content and repurpose it for a different narrative. |
| T0092 | Build Network | Assemble a network of accounts, channels, or sites for coordinated use. |
| T0093.002 | Acquire Botnets | Obtain a network of automated accounts for amplification. |
| T0096 | Leverage Content Farms | Use existing content-farm infrastructure to produce or spread content. |
| T0096.001 | Create Content Farms | Establish new content-farm infrastructure. |
| T0098 | Establish Inauthentic News Sites | Set up outlets designed to look like genuine news sources. |
| T0098.001 | Create Inauthentic News Sites | Build a new fake news outlet from scratch. |
| T0098.002 | Leverage Existing Inauthentic News Sites | Reuse an already-established fake outlet. |
| T0118 | Amplify Existing Narrative | Boost the reach of a narrative already in circulation. |
| T0119 | Cross-Posting | Post the same content across multiple platforms or groups to widen reach. |
| T0002 | Facilitate State Propaganda | Coordinate paid or volunteer groups to push state-aligned messaging. |
| T0091.003 | Enlist Troll Accounts | Recruit accounts whose purpose is to harass or disrupt discourse. |
| T0018 | Purchase Targeted Advertisements | Buy ads targeted at a specific audience to spread the narrative. |

### Analyst Techniques

Fabrication, synthetic/manipulated media, and persona/fact-distortion techniques
detectable through corroboration lookups.

| ID | Name | Summary |
|----|------|---------|
| T0086.002 | Develop AI-Generated Images (Deepfakes) | Produce synthetic images via AI to depict something that did not happen. |
| T0086.003 | Deceptively Edit Images (Cheap Fakes) | Edit real images (crop, splice, caption) to misrepresent them, without AI synthesis. |
| T0087.001 | Develop AI-Generated Videos (Deepfakes) | Produce synthetic video via AI to depict something that did not happen. |
| T0087.002 | Deceptively Edit Video (Cheap Fakes) | Edit real video to misrepresent it, without AI synthesis. |
| T0088.001 | Develop AI-Generated Audio (Deepfakes) | Produce synthetic audio via AI to depict something that was not said. |
| T0088.002 | Deceptively Edit Audio (Cheap Fakes) | Edit real audio to misrepresent it, without AI synthesis. |
| T0023 | Distort Facts | Twist or exaggerate real facts to support a misleading conclusion. |
| T0023.001 | Reframe Context | Present real content in a false or misleading context. |
| T0129.006 | Deny Involvement | Explicitly deny responsibility or involvement in an event despite evidence. |
| T0143.002 | Fabricated Persona | Invent a person or organization that does not exist. |
| T0143.003 | Impersonated Persona | Pose as a real, specific person or organization without authorization. |
| T0143.004 | Parody Persona | Use an exaggerated or satirical persona that can be mistaken for genuine. |
| T0144 | Persona Legitimacy Evidence | Fabricate supporting evidence (bios, photos, history) to make a persona appear real. |
| T0149.003 | Lookalike Domain | Register a domain designed to be mistaken for a legitimate outlet's domain. |
| T0140.001 | Defame | Make false statements damaging to a person's or organization's reputation. |

## Session Folder Convention

You will be given a session folder path (e.g. `artifacts/<session_id>/`). After producing
your findings, write them to `<session folder>/<your report filename>.md` using the Write
tool, in addition to returning them to your caller. Each role's own spec states its exact
report filename.

## Tool Usage Convention

Use any MCP tool actually available to you for lookups — general web search, WebFetch, and
platform-specific Apify actors alike. The config dict tells you which Apify actors are
configured for platform-specific lookups; never guess or discover an actor for a platform
missing from that dict — but general web search is always fair game regardless of the config
dict. If a tool is slow, hangs, or errors, don't block on it — use another available tool
instead.

Use only MCP tool(s) already available to you for external lookups — never install,
configure, authenticate, or enable a new MCP server or tool yourself, and never turn on a
platform that isn't already enabled in the config dict. Do not use file or shell tools for
anything except the session-folder report save described above.
